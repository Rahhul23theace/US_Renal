
from flask import Flask, request, redirect, url_for, render_template, flash
from werkzeug.utils import secure_filename
from flask import send_from_directory
from builtins import zip
import os
import torch
import torch.nn as nn
from torchvision import transforms, models
from util_cpu import load_models, ensemble_prediction, load_image_from_file
from genAI_feedback import generate_feedback

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png', 'gif'}
app.jinja_env.globals.update(zip=zip)

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)
        files = request.files.getlist('files[]')
        if not files or files[0].filename == '':
            flash('No selected file')
            return redirect(request.url)

        name = request.form.get('name')
        scholar_id = request.form.get('scholar_id')

        filenames = []
        predicted_classes = []

        for i, file in enumerate(files):
            if file and allowed_file(file.filename):
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(file_path)

                data_transforms = transforms.Compose([
                    transforms.Resize((224, 224)),
                    transforms.ToTensor(),
                    transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
                ])
                image = load_image_from_file(file, transform=data_transforms)

                try:
                    model_1, model_2 = load_models("resnet50.pt", "resnext50_32x4d.pt")
                    device = torch.device("cpu")
                    inputs = image.unsqueeze(0).to(device)
                    outputs = ensemble_prediction(model_1, model_2, inputs)
                except Exception as e:
                    app.logger.error(f"Error in model loading or prediction: {str(e)}")

                class_labels = ['Artefact', 'Incorrect_Gain', 'Incorrect_Position', 'Optimal', 'Wrong']

                predicted_labels = (outputs > 0.5).squeeze().detach().cpu().numpy().astype(int)
                if sum(predicted_labels) == 0:
                    top_prob_index = outputs.squeeze().detach().cpu().numpy().argmax()
                    predicted_label = f"{class_labels[top_prob_index]}"
                else:
                    predicted_label = ", ".join([class_labels[i] for i in range(len(predicted_labels)) if predicted_labels[i] == 1])

                predicted_classes.append(predicted_label)

                predicted_label = predicted_label.replace(" ", "_")
                filename = secure_filename(f"{name}_{scholar_id}_{predicted_label}_{file.filename}")
                os.rename(file_path, os.path.join(app.config['UPLOAD_FOLDER'], filename))
                filenames.append(filename)

        feedback_messages = generate_feedback(predicted_classes)
        file_urls = [url_for('uploaded_file', filename=f) for f in filenames]

        return render_template('index.html', predicted_classes=predicted_classes, feedback_messages=feedback_messages, file_urls=file_urls, feedback_data=zip(files, feedback_messages))

    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))



from flask import Flask, request, redirect, url_for, render_template, flash
from werkzeug.utils import secure_filename
from flask import send_from_directory
import os
import torch
import torch.nn as nn
from torchvision import transforms, models
from util_cpu import load_models, ensemble_prediction, load_image_from_file, generate_feedback
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE
from email import encoders

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png', 'gif'}
app.jinja_env.globals.update(zip=zip)

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def send_email_with_attachments(to, subject, text, files):
    from_address = "deepmachine007@gmail.com"
    password = "Rahul@12345"

    msg = MIMEMultipart()
    msg["From"] = from_address
    msg["To"] = COMMASPACE.join([to])
    msg["Subject"] = subject
    msg.attach(MIMEText(text))

    for file in files:
        part = MIMEBase("application", "octet-stream")
        with open(file, "rb") as f:
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(file)}")
        msg.attach(part)

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(from_address, password)
    server.sendmail(from_address, to, msg.as_string())
    server.quit()

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

        # Send email with attachments
        email_subject = "Uploaded Images and Predictions"
        email_body = "\n".join([f"{files[i].filename}: {predicted_classes[i]}" for i in range(len(files))])
        attached_files = [os.path.join(app.config['UPLOAD_FOLDER'], f) for f in filenames]
        send_email_with_attachments("rahul123@hku.hk", email_subject, email_body, attached_files)

        return render_template('index.html', predicted_classes=predicted_classes, feedback_messages=feedback_messages, file_urls=file_urls, feedback_data=zip(files, feedback_messages))

    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
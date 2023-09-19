







import openai
import os
import requests
import json
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())


openai.api_type = os.getenv('api_type')
openai.api_base = os.getenv('api_base')
openai.api_version = os.getenv('api_version')
openai.api_key = os.getenv('OPENAI_API_KEY')




def get_completion(prompt, engine="chatgpt"):
    messages = [{"role": "user", "content": prompt}]

    headers = {
        "Content-Type": "application/json",
        "api-key": openai.api_key,
        "Cache-Control": "no-cache"
    }

    payload = {
        "model": engine,
        "messages": messages,
        "max_tokens": 8000,
        "temperature": 0.7,
    }

    response = requests.post('https://api.hku.hk/openai/deployments/chatgpt/chat/completions?api-version=2023-03-15-preview', headers=headers, data=json.dumps(payload))
    response_data = response.json()
    return response_data['choices'][0]['message']['content']




def generate_feedback(predicted_classes):
    feedback = []
    label_information = '''

1. Artefact:  There are artefacts on the image. These could be due to acoustic shadowing
from the ribs (having the kidneys in the upper retroperitoneum) or ring-down 
artefacts from gas bubbles in the colon. If you are interested in reading more on 
ultrasound artefacts, please refer to explanation on Moodle MBBS Clinical Skills
Platform under Radiological, Ultrasound Section I 2.3. 
You can avoid these arfefacts from the ribs by asking the subject to take a deep 
inspiration, which will lower the diaphragm and hence the position of the kidney away 
from the ribcage, or by positioning the probe in between the ribs to avoid the artefact. 
To overcome ring-down artefacts, having the subject fasted will help or gently applying
pressure to displace the gas away from the area (but sometimes even with these efforts,
nothing work!). 

2. Incorrect Gain/Inappropriate gain:  The image is either too "bright" or too "dark". 
The Gain controls the brightness of the image (see Moodle MBBS Clinical Skills Platform 
under Radiological, Ultrasound Section I 3.5). Another good reference for explanation can 
be found on:

 https://123sonography.com/blog/ultrasound-101-part-5-gain-and-time-gain-compensation#:~:text=What%20is%20gain%3F,much%20each%20echo%20is%20amplified.

3. Incorrect Position/ Suboptimal positioning: The organ of interest, i.e. kidney, 
is not correctly positioned in the captured imaged. It is not centrally placed or 
incompletely imaged (cut-off, cropped). Having the subject in decubitus position helps 
to get good access to image the kidney as explained in the video on Moodle MBBS Clinical
Skills Platform under Radiological, Ultrasound Section IIC 7.1. If this is not possible, 
then try positioning the probe anteriorly and posteriorly to find an ideal view of the
kidney maybe required as every subject is different. 

4. Optimal: Well done/good work for obtaining optimal image quality of the kidney. 

5. Wrong: The image acquired is of the wrong organ. Please refer to Moodle MBBS Clinical 
Skills Platform under Radiological, Ultrasound Section IIC 7.1, where there is a video
demonstrating how to perform and acquire image of the kidney using ultrasound:

https://moodle.hku.hk/mod/page/view.php?id=2748898

'''
    for prediction in predicted_classes:
        feedback_for_prediction = []
        labels = prediction.split(", ")
        prompt = f"{label_information}\n\nBased on the above information, please provide feedback for an ultrasound image with the following characteristics: {', '.join(labels)}.Also check if url link is provided for particular.If link is there, provide the link along with generated for that particular label.\n Please provide a creative response while maintaining an academic tone and factual information."

        response_text = get_completion(prompt)
        feedback_text = response_text.strip()
        feedback_for_prediction.append(feedback_text)
        feedback.append(feedback_for_prediction)

    return feedback



############################ EXAMPLE    #############################


""" 

predicted_classes = ["Artefact", "Incorrect Gain", "Optimal"]
feedback = generate_feedback(predicted_classes)

for i, fb in enumerate(feedback):
    print(f"Feedback for prediction {i + 1}:")
    print(fb[0])
    print()
 """









def generate_feedback(predicted_classes):
    feedback = []
    for prediction in predicted_classes:
        feedback_for_prediction = []
        labels = prediction.split(", ")
        for label in labels:
            if label == "Artefact":
                artefact_feedback_options = [ "Image artifacts: The image contains artifacts that may result from acoustic shadowing or ring-down artifacts. To learn more about ultrasound artifacts, visit the Moodle MBBS Clinical Skills Platform under Radiological, Ultrasound Section I 2.3. To avoid rib artifacts, ask the subject to take a deep breath or position the probe between the ribs. To overcome ring-down artifacts, have the subject fast or gently apply pressure to displace gas.",
                    
                    "Presence of artifacts: The image has artifacts, possibly due to acoustic shadowing or ring-down artifacts. For more information on ultrasound artifacts, check the Moodle MBBS Clinical Skills Platform under Radiological, Ultrasound Section I 2.3. Minimize rib artifacts by having the subject take a deep breath or positioning the probe between the ribs. To address ring-down artifacts, ensure the subject is fasted or apply gentle pressure to displace gas.",
                    
                    "Artifacts in the image: The image displays artifacts that could be caused by acoustic shadowing or ring-down artifacts. To learn more about these artifacts, refer to the Moodle MBBS Clinical Skills Platform under Radiological, Ultrasound Section I 2.3. To avoid rib artifacts, instruct the subject to inhale deeply or place the probe between the ribs. To handle ring-down artifacts, have the subject fast or apply gentle pressure to move gas away from the area.",
                    
                    "Image artifacts present: The image exhibits artifacts, which might be due to acoustic shadowing or ring-down artifacts. For further information on ultrasound artifacts, consult the Moodle MBBS Clinical Skills Platform under Radiological, Ultrasound Section I 2.3. To mitigate rib artifacts, ask the subject to breathe in deeply or position the probe between the ribs. To deal with ring-down artifacts, ensure the subject has fasted or apply gentle pressure to displace gas.",
                    
                    "Artifacts detected: The image shows artifacts that could result from acoustic shadowing or ring-down artifacts. To gain more insight into ultrasound artifacts, visit the Moodle MBBS Clinical Skills Platform under Radiological, Ultrasound Section I 2.3. To prevent rib artifacts, have the subject take a deep breath or place the probe between the ribs. To address ring-down artifacts, make sure the subject is fasted or apply gentle pressure to move gas away from the area.",
                    
                    "Artifacts observed: The image contains artifacts, possibly due to acoustic shadowing or ring-down artifacts. For additional information on ultrasound artifacts, refer to the Moodle MBBS Clinical Skills Platform under Radiological, Ultrasound Section I 2.3. To minimize rib artifacts, instruct the subject to inhale deeply or position the probe between the ribs. To handle ring-down artifacts, ensure the subject has fasted or apply gentle pressure to displace gas."
                ]
                feedback_for_prediction.append(random.choice(artefact_feedback_options))
        feedback.append(feedback_for_prediction)
    return feedback











def generate_feedback(predicted_classes):
    feedback = []
    for prediction in predicted_classes:
        feedback_for_prediction = []
        labels = prediction.split(", ")
        for label in labels:
            if label == "Artefact":
                artefact_feedback_options = [''' The image contains artifacts that may result from acoustic shadowing or
                                            ring-down artifacts. To learn more about ultrasound artifacts, 
                                            visit the Moodle MBBS Clinical Skills Platform under Radiological, 
                                            Ultrasound Section I 2.3. To avoid rib artifacts, ask the subject to take a deep
                                            breath or position the probe between the ribs. To overcome ring-down artifacts,
                                            have the subject fast or gently apply pressure to displace gas.''',

                                            '''The image has artifacts, possibly due to acoustic shadowing or ring-down artifacts. 
                                            For more information on ultrasound artifacts, check the Moodle MBBS Clinical Skills 
                                            Platform under Radiological, Ultrasound Section I 2.3. Minimize rib artifacts by having 
                                            the subject take a deep breath or positioning the probe between the ribs. 
                                            To address ring-down artifacts, ensure the subject is fasted or apply gentle pressure to displace gas.''',


                                              
                                            '''The image displays artifacts that could be caused by acoustic shadowing or ring-down artifacts. 
                                            To learn more about these artifacts, refer to the Moodle MBBS Clinical Skills Platform under Radiological,
                                            Ultrasound Section I 2.3. To avoid rib artifacts, instruct the subject to inhale deeply or place the probe
                                            between the ribs. To handle ring-down artifacts, have the subject fast or apply gentle pressure to move
                                            gas away from the area.''',

                                                

                                            '''The image exhibits artifacts, which might be due to acoustic shadowing or ring-down artifacts. 
                                            For further information on ultrasound artifacts, consult the Moodle MBBS Clinical Skills Platform under
                                            Radiological, Ultrasound Section I 2.3. To mitigate rib artifacts, ask the subject to breathe in deeply
                                            or position the probe between the ribs. To deal with ring-down artifacts, ensure the subject has 
                                            fasted or apply gentle pressure to displace gas.''',


                                            '''The image shows artifacts that could result from acoustic shadowing or ring-down artifacts. 
                                            To gain more insight into ultrasound artifacts, visit the Moodle MBBS Clinical Skills Platform under Radiological, 
                                            Ultrasound Section I 2.3. To prevent rib artifacts, have the subject take a deep breath or place the probe between 
                                            the ribs. To address ring-down artifacts, make sure the subject is fasted or apply gentle pressure to move gas away 
                                            from the area.''',


                                            '''The image contains artifacts, possibly due to acoustic shadowing or ring-down artifacts. 
                                            For additional information on ultrasound artifacts, refer to the Moodle MBBS Clinical Skills Platform 
                                            under Radiological, Ultrasound Section I 2.3. To minimize rib artifacts, instruct the subject to
                                            inhale deeply or position the probe between the ribs. To handle ring-down artifacts, ensure the subject 
                                            has fasted or apply gentle pressure to displace gas.''',



                                            '''The image displays artifacts that might be caused by acoustic shadowing or ring-down artifacts. 
                                            To learn more about these artifacts, consult the Moodle MBBS Clinical Skills Platform under Radiological,
                                            Ultrasound Section I 2.3. To avoid rib artifacts, ask the subject to breathe in deeply or place the probe 
                                            between the ribs. To deal with ring-down artifacts, have the subject fast or apply gentle pressure to move
                                            gas away from the area.''',


                                            '''There are artefacts on the image. These could be due to acoustic shadowing
                                            from the ribs (having the kidneys in the upper retroperitoneum) or ring-down 
                                            artefacts from gas bubbles in the colon. If you are interested in reading more on 
                                            ultrasound artefacts, please refer to explanation on Moodle MBBS Clinical Skills
                                            Platform under Radiological, Ultrasound Section I 2.3. 
                                            You can avoid these arfefacts from the ribs by asking the subject to take a deep 
                                            inspiration, which will lower the diaphragm and hence the position of the kidney away 
                                            from the ribcage, or by positioning the probe in between the ribs to avoid the artefact. 
                                            To overcome ring-down artefacts, having the subject fasted will help or gently applying
                                            pressure to displace the gas away from the area (but sometimes even with these efforts,
                                            nothing work!). ''']

                feedback_for_prediction.append(random.choice(artefact_feedback_options))

            elif label == "Incorrect_Gain":
                incorrect_gain_feedback_options = [
                                            '''Gain issues: The image is either too bright or too dark. Adjust the Gain to control the image brightness 
                                            (see Moodle MBBS Clinical Skills Platform under Radiological, Ultrasound Section I 3.5). 
                                            Another helpful resource for understanding Gain can be found at:
                                            https://123sonography.com/blog/ultrasound-101-part-5-gain-and-time-gain-compensation.''',


                                            '''Gain problems: The image appears either too bright or too dark. Modify the Gain to regulate the
                                            image brightness (refer to Moodle MBBS Clinical Skills Platform under Radiological, Ultrasound Section I 3.5).
                                            For further explanation on Gain, visit:
                                            https://123sonography.com/blog/ultrasound-101-part-5-gain-and-time-gain-compensation.''',


                                            '''Inappropriate gain: The image is either overly bright or too dark. Adjust the Gain to manage the image
                                            brightness (consult Moodle MBBS Clinical Skills Platform under Radiological, Ultrasound Section I 3.5).
                                            Another resource for understanding Gain is available at: 
                                            https://123sonography.com/blog/ultrasound-101-part-5-gain-and-time-gain-compensation.''',



                                            '''Incorrect gain settings: The image is either excessively bright or too dark. Change the Gain to control
                                            the image brightness (see Moodle MBBS Clinical Skills Platform under Radiological, Ultrasound Section I 3.5).
                                            For more information on Gain, check: 
                                            https://123sonography.com/blog/ultrasound-101-part-5-gain-and-time-gain-compensation.''',


                                            '''Gain-related issues: The image is either too bright or too dark. Tweak the Gain to adjust the image brightness
                                            (refer to Moodle MBBS Clinical Skills Platform under Radiological, Ultrasound Section I 3.5). 
                                            For additional explanation on Gain, visit: 
                                            https://123sonography.com/blog/ultrasound-101-part-5-gain-and-time-gain-compensation.''',


                                            '''Suboptimal gain settings: The image appears either too bright or too dark. 
                                            Modify the Gain to manage the image brightness (consult Moodle MBBS Clinical Skills Platform under 
                                            Radiological, Ultrasound Section I 3.5). For further understanding of Gain, check: 
                                            https://123sonography.com/blog/ultrasound-101-part-5-gain-and-time-gain-compensation.''',




                                            '''Gain adjustment needed: The image is either overly bright or too dark. Adjust the Gain to regulate 
                                            the image brightness (see Moodle MBBS Clinical Skills Platform under Radiological, Ultrasound Section I 3.5).
                                            Another helpful resource for learning about Gain is available at: 
                                            https://123sonography.com/blog/ultrasound-101-part-5-gain-and-time-gain-compensation.''']
                
                feedback_for_prediction.append(random.choice(incorrect_gain_feedback_options))





            elif label == "Incorrect_Position":
                incorrect_position_feedback_options = [
                                                        '''Positioning issues: The kidney is not correctly positioned in the captured image. 
                                                        It is not centrally placed or incompletely imaged. Placing the subject in a decubitus position helps
                                                        obtain a better image of the kidney (see Moodle MBBS Clinical Skills Platform under Radiological,
                                                        Ultrasound Section IIC 7.1). If this is not possible, try positioning the probe anteriorly and
                                                        posteriorly to find an ideal view of the kidney.''',


                                                        '''Suboptimal positioning: The kidney is not properly positioned in the image, appearing off-center
                                                        or partially imaged. Using a decubitus position can improve kidney imaging (refer to Moodle MBBS 
                                                        Clinical Skills Platform under Radiological, Ultrasound Section IIC 7.1). If this is not feasible, 
                                                        adjust the probe's position anteriorly and posteriorly to obtain an optimal view of the kidney.''',

    
                                                        '''Incorrect position: The kidney is not accurately positioned in the captured image, being off-center
                                                        or incompletely imaged. Positioning the subject in a decubitus position can enhance kidney imaging
                                                        (consult Moodle MBBS Clinical Skills Platform under Radiological, Ultrasound Section IIC 7.1). 
                                                        If this is not possible, try moving the probe anteriorly and posteriorly to find the best view
                                                        of the kidney.''',

    
                                                        '''Positioning problems: The kidney is not correctly positioned in the image, appearing off-center 
                                                        or partially imaged. A decubitus position can help achieve better kidney imaging (see Moodle MBBS 
                                                        Clinical Skills Platform under Radiological, Ultrasound Section IIC 7.1). If this is not feasible,
                                                        adjust the probe's position anteriorly and posteriorly to obtain an optimal view of the kidney.''',

    
                                                        '''Inaccurate positioning: The kidney is not properly positioned in the captured image,
                                                        being off-center or incompletely imaged. Using a decubitus position can improve kidney imaging
                                                        (refer to Moodle MBBS Clinical Skills Platform under Radiological, Ultrasound Section IIC 7.1).
                                                        If this is not possible, try moving the probe anteriorly and posteriorly to find the best view 
                                                        of the kidney.''',


    
                                                        '''Suboptimal position: The kidney is not accurately positioned in the image, appearing off-center
                                                        or partially imaged. Positioning the subject in a decubitus position can enhance kidney imaging
                                                        (consult Moodle MBBS Clinical Skills Platform under Radiological, Ultrasound Section IIC 7.1). 
                                                        If this is not feasible, adjust the probe's position anteriorly and posteriorly to obtain an 
                                                        optimal view of the kidney.''',


    
                                                        '''Positioning errors: The kidney is not correctly positioned in the captured image, being off-center
                                                        or incompletely imaged. A decubitus position can help achieve better kidney imaging (see Moodle MBBS
                                                        Clinical Skills Platform under Radiological, Ultrasound Section IIC 7.1). If this is not possible,
                                                        try moving the probe anteriorly and posteriorly to find the best view of the kidney.''']
                
                feedback_for_prediction.append(random.choice(incorrect_position_feedback_options))




            elif label == "Optimal":
                optimal_feedback_options = [
                                            '''Optimal image quality: Congratulations on obtaining an optimal image quality of the kidney.''',

                                            '''Excellent image quality: Well done on achieving excellent image quality of the kidney.''',

                                            '''High-quality image: Great job on capturing a high-quality image of the kidney.''',
                                            
                                            '''Superior image quality: Kudos for obtaining a superior image quality of the kidney.''',
                                            
                                            '''Outstanding image quality: Impressive work on acquiring an outstanding image quality of the kidney.''',
                                            
                                            '''Exceptional image quality: Bravo for achieving an exceptional image quality of the kidney.''',

                                            '''Top-notch image quality: Excellent work on capturing a top-notch image quality of the kidney.''']


                feedback_for_prediction.append(random.choice(optimal_feedback_options))






            elif label == "Wrong":
                wrong_feedback_options = [
                                            
                                            '''Incorrect organ: The image acquired is of the wrong organ. Please refer to the video on Moodle MBBS 
                                            Clinical Skills Platform under Radiological, Ultrasound Section IIC 7.1 for guidance on acquiring an image
                                              of the kidney using ultrasound: https://moodle.hku.hk/mod/page/view.php?id=2748898.''',
                                              
                                            
                                            '''Wrong organ imaged: The captured image is of the incorrect organ. Consult the video on Moodle MBBS Clinical 
                                            Skills Platform under Radiological, Ultrasound Section IIC 7.1 for instructions on imaging the kidney using 
                                            ultrasound: https://moodle.hku.hk/mod/page/view.php?id=2748898.''',

                                            
                                            '''Image of incorrect organ: The acquired image is of the wrong organ. Please review the video on Moodle MBBS 
                                            Clinical Skills Platform under Radiological, Ultrasound Section IIC 7.1 to learn how to image the kidney using
                                              ultrasound: https://moodle.hku.hk/mod/page/view.php?id=2748898.''',

                                            
                                            '''Captured wrong organ: The image captured is of the incorrect organ. Refer to the video on Moodle MBBS
                                              Clinical Skills Platform under Radiological, Ultrasound Section IIC 7.1 for guidance on obtaining an 
                                              image of the kidney using ultrasound: https://moodle.hku.hk/mod/page/view.php?id=2748898.''',

                                            
                                            '''Incorrect organ image: The image obtained is of the wrong organ. Consult the video on Moodle MBBS Clinical
                                              Skills Platform under Radiological, Ultrasound Section IIC 7.1 for instructions on imaging the kidney using
                                                ultrasound: https://moodle.hku.hk/mod/page/view.php?id=2748898.''',

                                            

                                            '''Wrong organ captured: The acquired image is of the incorrect organ. Please review the video on Moodle MBBS 
                                            Clinical Skills Platform under Radiological, Ultrasound Section IIC 7.1 to learn how to image the kidney using
                                              ultrasound: https://moodle.hku.hk/mod/page/view.php?id=2748898.''',

                                            
                                            '''Image of wrong organ: The captured image is of the wrong organ. Refer to the video on Moodle MBBS Clinical
                                              Skills Platform under Radiological, Ultrasound Section IIC 7.1 for guidance on obtaining an image of the
                                                kidney using ultrasound: https://moodle.hku.hk/mod/page/view.php?id=2748898.''']
                

                feedback_for_prediction.append(random.choice(wrong_feedback_options))
            else:
                feedback_for_prediction.append("I am sorry, something went wrong")
        feedback.append(feedback_for_prediction)
    return feedback




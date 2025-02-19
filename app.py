from flask import Flask, render_template, request, send_from_directory, flash, redirect, url_for
import cv2
import numpy as np
from fer import FER
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Pre-load the emotion detector using the FER library
detector = FER(mtcnn=True)

def get_support_message(emotion):
    """Return a supportive message based on the detected emotion."""
    messages = {
       "angry": "It seems you're feeling angry. Try some deep breathing or a short walk to help calm down.",
       "disgust": "You seem uneasy. Maybe take a break and do something relaxing.",
       "fear": "Feeling scared is tough. Consider grounding techniques or talking to someone you trust.",
       "happy": "You're happy! Keep enjoying your day and spread the positivity.",
       "sad": "It looks like you're feeling sad. A warm drink or a short walk might lift your spirits.",
       "surprise": "You appear surprised. Take a moment to process your feelings.",
       "neutral": "Your expression seems neutral. Reflecting on your feelings can sometimes be helpful.",
    }
    return messages.get(emotion, "Take care and stay positive!")

@app.route('/static/<path:filename>')
def send_static(filename):
    return send_from_directory('static', filename)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        # Check if the file is part of the POST request
        if 'image' not in request.files:
            flash("No file part in the request.", 'error')
            return redirect(request.url)
        file = request.files['image']
        if file.filename == '':
            flash("No selected file.", 'error')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            # Read image using OpenCV
            img = cv2.imread(filepath)
            # Use FER to detect emotions
            analysis = detector.detect_emotions(img)
            if analysis:
                # Assume the first detected face is the user; get its emotion scores
                emotions = analysis[0]["emotions"]
                dominant_emotion = max(emotions, key=emotions.get)
                support_message = get_support_message(dominant_emotion)
                result = f"Detected Emotion: {dominant_emotion.capitalize()}<br>Recommendation: {support_message}"
            else:
                result = "No face detected. Please try another image."
            flash(result, 'info')
            return redirect(request.url)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

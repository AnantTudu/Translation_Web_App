from flask import Flask, request, jsonify
import speech_recognition as sr
from flask_cors import CORS  # Import CORS


app = Flask(__name__)
CORS(app)  # Enable CORS for this app


def speech_to_text(language_choice):
    # Initialize the recognizer
    recognizer = sr.Recognizer()
    
    # Use the microphone as the audio source
    with sr.Microphone() as source:
        print("Adjusting for ambient noise, please wait...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        print("Please say something...")

        # Capture audio from the microphone
        audio = recognizer.listen(source)
        
        try:
            # Use Google Web Speech API to convert audio to text
            if language_choice == 2:  # 2 for Hindi
                text = recognizer.recognize_google(audio, language="hi-IN")  # Set language to Hindi
            elif language_choice == 1:  # 1 for English
                text = recognizer.recognize_google(audio, language="en-US")  # Set language to English
            else:
                return "Invalid language choice. Please choose either English (1) or Hindi (2)."
            
            return text
        
        except sr.UnknownValueError:
            return "Sorry, I could not understand the audio."
        except sr.RequestError as e:
            return f"Could not request results from Google Speech Recognition service; {e}"

# Home route
@app.route('/')
def home():
    return "Welcome to the Speech-to-Text API! Use POST /speech-to-text to convert speech to text."

# Route for speech-to-text
@app.route('/speech-to-text', methods=['POST'])
def api_speech_to_text():
    data = request.json
    language_choice = data.get('language_choice')

    if not language_choice or language_choice not in [1, 2]:
        return jsonify({"error": "Invalid or missing language choice. Use 1 for English or 2 for Hindi."}), 400

    # Convert speech to text
    result = speech_to_text(language_choice)

    return jsonify({"transcribed_text": result})

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)

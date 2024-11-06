import os
import uuid
import pygame
import speech_recognition as sr
from io import BytesIO
from dotenv import load_dotenv
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from deep_translator import GoogleTranslator
from flask import Flask, request, jsonify
from flask_cors import CORS
from text_translation_F import translate_text
from ocr_translation_F import ocr_translate, display_image_with_text
from text_to_speech_F import text_to_speech_stream
from speech_to_text_F import speech_to_text
from speech_translation_F import get_target_language_choice, translate_text, text_to_speech_stream, speech_to_text

# Load environment variables from the .env file
load_dotenv()

# Retrieve the ElevenLabs API key from environment variables
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

app = Flask(__name__)
CORS(app)  # Enable CORS for this app



# Route for text translation
@app.route('/api/translate', methods=['POST'])
def api_translate_text():
    data = request.json
    text = data.get('text')
    target_language = data.get('target_language')

    if not text or not target_language:
        return jsonify({"error": "Missing text or target language"}), 400

    try:
        translated_text = translate_text(text, target_language)
        return jsonify({"translated_text": translated_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500




# Route for OCR translation (image to text)
@app.route('/api/ocr-translate', methods=['POST'])
def api_ocr_translate():
    return ocr_translate()

# Initialize the speech recognizer
recognizer = sr.Recognizer()

# Function to convert text to speech using ElevenLabs API
def text_to_speech_stream(text: str) -> BytesIO:
    # Perform the text-to-speech conversion using ElevenLabs API
    response = client.text_to_speech.convert(
        voice_id="pNInz6obpgDQGcFmaJgB",  # Adam pre-made voice
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_multilingual_v2",
        voice_settings=VoiceSettings(
            stability=0.0,
            similarity_boost=1.0,
            style=0.0,
            use_speaker_boost=True,
        ),
    )

    # Create a BytesIO object to hold the audio data in memory
    audio_stream = BytesIO()

    # Write each chunk of audio data to the stream
    for chunk in response:
        if chunk:
            audio_stream.write(chunk)

    # Reset stream position to the beginning
    audio_stream.seek(0)

    return audio_stream

# Route for text-to-speech
@app.route('/api/text-to-speech', methods=['POST'])
def api_text_to_speech():
    data = request.json
    text = data.get('text')

    if not text:
        return jsonify({"error": "Missing text"}), 400

    # Get the audio stream using ElevenLabs API
    audio_stream = text_to_speech_stream(text)

    # Initialize pygame mixer
    pygame.mixer.init()

    # Load the audio stream directly into pygame
    pygame.mixer.music.load(audio_stream, 'mp3')

    # Play the audio
    pygame.mixer.music.play()

    # Optionally, you can wait until the music finishes playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    return jsonify({"message": "Audio is playing"})

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

# Route for speech-to-text
@app.route('/api/speech-to-text', methods=['POST'])
def api_speech_to_text():
    data = request.json
    language_choice = data.get('language_choice')

    if not language_choice or language_choice not in [1, 2]:
        return jsonify({"error": "Invalid or missing language choice. Use 1 for English or 2 for Hindi."}), 400

    # Convert speech to text
    result = speech_to_text()

    return jsonify({"transcribed_text": result})

# Function to get the target language choice from the user
def get_target_language_choice():
    print("Available languages for translation:")
    print("1. English (en)")
    print("2. Spanish (es)")
    print("3. German (de)")
    print("4. French (fr)")
    print("5. Hindi (hi)")
    
    language_map = {
        '1': 'en',  # English
        '2': 'es',  # Spanish
        '3': 'de',  # German
        '4': 'fr',  # French
        '5': 'hi'   # Hindi
    }
    
    choice = input("Select the target language by entering the corresponding number: ")
    
    return language_map.get(choice, 'en')  # Default to English if invalid choice

# Function to translate text
def translate_text(text, target_language):
    translator = GoogleTranslator(source='auto', target=target_language)
    translated = translator.translate(text)
    return translated

# Function to convert text to speech
def text_to_speech_stream(text: str) -> BytesIO:
    # Perform the text-to-speech conversion using ElevenLabs API
    response = client.text_to_speech.convert(
        voice_id="pNInz6obpgDQGcFmaJgB",  # Adam pre-made voice
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_multilingual_v2",
        voice_settings=VoiceSettings(
            stability=0.0,
            similarity_boost=1.0,
            style=0.0,
            use_speaker_boost=True,
        ),
    )

    # Create a BytesIO object to hold the audio data in memory
    audio_stream = BytesIO()

    # Write each chunk of audio data to the stream
    for chunk in response:
        if chunk:
            audio_stream.write(chunk)

    # Reset stream position to the beginning
    audio_stream.seek(0)

    return audio_stream

# Function for speech recognition
def speech_to_text():
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
            # Recognize the speech using Google Web Speech API
            text = recognizer.recognize_google(audio)  # Use automatic language recognition
            print("You said: " + text)
            return text

        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

        return None

# Route for real-time voice translation
@app.route('/api/translate-speech', methods=['POST'])
def api_translate():
    # Get JSON data from the request
    data = request.json
    
    # If the JSON data is None (like when sending an empty body), initialize data as an empty dictionary
    if data is None:
        data = {}

    # Ensure you can proceed with the recognized speech
    original_text = speech_to_text()
    if original_text is None:
        return jsonify({"error": "No speech detected."}), 400

    # Check if the request has a specified target language choice
    target_language = data.get('target_language')
    
    # If not provided, fall back to interactive prompt
    if not target_language:
        target_language = get_target_language_choice()

    # Translate the text to the selected target language
    translated_text = translate_text(original_text, target_language)
    
    print(f"Translated text ({target_language}): {translated_text}")

    # Convert the translated text to speech
    audio_stream = text_to_speech_stream(translated_text)

    # Initialize pygame mixer
    pygame.mixer.init()

    # Load and play the audio stream directly without saving to a file
    pygame.mixer.music.load(audio_stream, 'mp3')
    pygame.mixer.music.play()

    # Wait until the music finishes playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    return jsonify({"original_text": original_text, "translated_text": translated_text})



# Home route
@app.route('/')
def home():
    return "Welcome to the Real-Time Voice Translation API! Use POST /translate to translate speech."

if __name__ == "__main__":
    app.run(debug=True)

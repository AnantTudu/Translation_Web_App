import os
import uuid
from io import BytesIO
from dotenv import load_dotenv
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
import pygame
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS



# Load environment variables from the .env file
load_dotenv()

# Retrieve the ElevenLabs API key from environment variables
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

app = Flask(__name__)
CORS(app)  # Enable CORS for this app


def text_to_speech_stream(text: str) -> BytesIO:
    # Perform the text-to-speech conversion
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

# Home route
@app.route('/')
def home():
    return "Welcome to the Text-to-Speech API! Use POST /text-to-speech to convert text to speech."

# Route for text-to-speech
@app.route('/text-to-speech', methods=['POST'])
def api_text_to_speech():
    data = request.json
    text = data.get('text')

    if not text:
        return jsonify({"error": "Missing text"}), 400

    # Convert text to speech and get audio stream
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

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)

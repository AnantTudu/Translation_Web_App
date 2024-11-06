from flask import Flask, request, jsonify
from deep_translator import GoogleTranslator
from flask_cors import CORS  # Import CORS

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Function to translate text
def translate_text(text, target_language):
    translator = GoogleTranslator(source='auto', target=target_language)
    translated = translator.translate(text)
    return translated

# List of allowed target languages
allowed_languages = ['en', 'es', 'de', 'fr', 'hi']

# Home route
@app.route('/')
def home():
    return "Welcome to the Translation API! Use POST /translate to get translations."

# Route for text translation
@app.route('/translate', methods=['POST'])
def api_translate_text():
    data = request.json  # Get the JSON payload from the request
    text = data.get('text')  # Extract text from the request
    target_language = data.get('target_language')  # Extract target language

    # Validate input
    if not text or not target_language:
        return jsonify({"error": "Missing text or target language"}), 400

    # Check if the target language is allowed
    if target_language not in allowed_languages:
        return jsonify({"error": f"Target language '{target_language}' not supported"}), 400

    # Perform translation
    try:
        translated_text = translate_text(text, target_language)
        return jsonify({"translated_text": translated_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, request, jsonify
import easyocr
import matplotlib.pyplot as plt
import cv2
import os
from deep_translator import GoogleTranslator
from flask_cors import CORS  # Import CORS


app = Flask(__name__)
CORS(app)  # Enable CORS for this app


# Initialize the EasyOCR reader object for both English and Hindi
reader = easyocr.Reader(['en', 'hi'])

# Route for text extraction and translation from image
@app.route('/ocr-translate', methods=['POST'])
def ocr_translate():
    # Check if an image is provided in the request
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400
    
    file = request.files['image']
    
    # Save the uploaded image
    image_path = os.path.join('uploads', file.filename)  # Ensure 'uploads' folder exists
    file.save(image_path)

    # Load the image
    image = cv2.imread(image_path)

    # Use EasyOCR to detect and extract text from the image
    result = reader.readtext(image_path)

    # Initialize an empty list to store detected texts
    detected_texts = []

    # Iterate over the OCR results
    for (bbox, text, prob) in result:
        detected_texts.append(text)  # Append each detected text to the list

    # Join the detected texts into a single sentence
    sentence = ' '.join(detected_texts)

    # Print the detected text before translation
    print(f"Detected Text: {sentence}")

    # Initialize the translator
    translator = GoogleTranslator(source='auto', target='en')

    try:
        # Perform translation
        translated_text = translator.translate(sentence)
        print(f"Translated Text to English: {translated_text}")
    except Exception as e:
        return jsonify({"error": f"An error occurred during translation: {str(e)}"}), 500

    # Optional: Display the image with detected text (uncomment to enable)
    # display_image_with_text(image, result)

    # Return the detected and translated text as JSON response
    return jsonify({
        "detected_text": sentence,
        "translated_text": translated_text
    })

# Function to display the image with detected text (optional)
def display_image_with_text(image, result):
    for (bbox, text, prob) in result:
        # Unpack the bounding box
        (top_left, top_right, bottom_right, bottom_left) = bbox
        top_left = tuple(map(int, top_left))
        bottom_right = tuple(map(int, bottom_right))

        # Draw a rectangle around the detected text
        cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)

        # Put the detected text on the image
        cv2.putText(image, text, (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Convert the image from BGR to RGB format
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Display the image with matplotlib
    plt.figure(figsize=(10, 10))
    plt.imshow(image_rgb)
    plt.axis('off')
    plt.show()

# Home route
@app.route('/')
def home():
    return "Welcome to the OCR and Translation API! Use POST /ocr-translate to upload an image."

# Run the Flask app
if __name__ == "__main__":
    # Make sure to create an 'uploads' directory in the same path to save images
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    
    app.run(debug=True)

async function translateText() {
    const textInput = document.getElementById('text-input').value;
    const targetLanguage = document.getElementById('target-language').value;

    const response = await fetch('http://127.0.0.1:5000/translate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: textInput, target_language: targetLanguage }),
    });

    const data = await response.json();
    document.getElementById('translation-output').innerText = data.translated_text || data.error;
}

async function ocrTranslate() {
    const fileInput = document.getElementById('ocr-file');
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    const response = await fetch('http://127.0.0.1:5000/ocr-translate', {
        method: 'POST',
        body: formData,
    });

    const data = await response.json();
    document.getElementById('ocr-output').innerText = data.translated_text || data.error;
}

async function textToSpeech() {
    const ttsInput = document.getElementById('tts-input').value;

    const response = await fetch('http://127.0.0.1:5000/text-to-speech', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: ttsInput }),
    });

    const data = await response.json();
    document.getElementById('tts-output').innerText = data.message;
}

// async function speechToText() {
//     const languageChoice = parseInt(document.getElementById('stt-language').value, 10); // Parse as integer

//     const response = await fetch('http://127.0.0.1:5000/speech-to-text', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({ language_choice: languageChoice }), // Ensure it's an integer
//     });

//     const data = await response.json();
//     document.getElementById('stt-output').innerText = data.transcribed_text || data.error;
// }


async function speechToText() {
    const languageChoice = parseInt(document.getElementById('stt-language').value, 10); // Parse as integer

    // Display "Adjusting to ambient sound...."
    const statusMessage = document.getElementById('statusMessage');
    if (!statusMessage) {
        console.error("Element with ID 'statusMessage' not found.");
        return; // Exit if the element does not exist
    }

    statusMessage.innerText = "Adjusting to ambient sound....";

    // After 1 second, change message to "Please Speak"
    await new Promise(resolve => setTimeout(resolve, 1000)); // Wait for 1 second

    statusMessage.innerText = "Please Speak";

    // Fetch the speech-to-text API
    try {
        const response = await fetch('http://127.0.0.1:5000/speech-to-text', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ language_choice: languageChoice }), // Ensure it's an integer
        });

        // Check if the response is OK (status in the range 200-299)
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        document.getElementById('stt-output').innerText = data.transcribed_text || data.error;

    } catch (error) {
        // Display error message to the user
        console.error("Error during speech-to-text conversion:", error);
        document.getElementById('stt-output').innerText = "An error occurred during the process. Please try again.";
    }
}



async function speechTranslate() {
    const targetLanguage = document.getElementById('speech-target-language').value;

    const response = await fetch('http://127.0.0.1:5000/speech-translate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ target_language: targetLanguage }),
    });

    const data = await response.json();
    document.getElementById('speech-translation-output').innerText = data.translated_text || data.error;
}

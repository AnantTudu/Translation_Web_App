document.getElementById("translate-text").addEventListener("click", async () => {
    const text = document.getElementById("text-to-translate").value;
    const targetLanguage = document.getElementById("target-language").value;

    const response = await fetch("http://localhost:5000/translate", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ text, target_language: targetLanguage }),
    });

    const data = await response.json();
    document.getElementById("translated-text").innerText = data.translated_text || data.error;
});

document.getElementById("ocr-translate").addEventListener("click", async () => {
    const fileInput = document.getElementById("ocr-file");
    const file = fileInput.files[0];
    
    const formData = new FormData();
    formData.append("image", file);

    const response = await fetch("http://localhost:5000/ocr-translate", {
        method: "POST",
        body: formData,
    });

    const data = await response.json();
    document.getElementById("ocr-translated-text").innerText = data.translated_text || data.error;
});

document.getElementById("text-to-speech").addEventListener("click", async () => {
    const text = document.getElementById("text-to-speak").value;

    const response = await fetch("http://localhost:5000/text-to-speech", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ text }),
    });

    const data = await response.json();
    console.log(data.message);
});

document.getElementById("speech-to-text").addEventListener("click", async () => {
    const response = await fetch("http://localhost:5000/speech-to-text", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ language_choice: 1 }), // Change this to the desired language choice
    });

    const data = await response.json();
    document.getElementById("speech-transcription").innerText = data.transcribed_text || data.error;
});

document.getElementById("speech-translate").addEventListener("click", async () => {
    const response = await fetch("http://localhost:5000/speech-translate", {
        method: "POST",
    });

    const data = await response.json();
    document.getElementById("speech-translation-result").innerText = data.translated_text || data.error;
});

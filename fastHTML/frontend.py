from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import httpx

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Mystic Mirror</title>
        <style>
            body {
                background-image: linear-gradient(to bottom, #0f0c29, #302b63, #24243e);
                color: #f1f1f1;
                font-family: Arial, sans-serif;
                text-align: center;
                padding: 50px;
            }
            .button {
                background-color: #7e57c2;
                color: white;
                padding: 14px 28px;
                border-radius: 10px;
                font-size: 22px;
                cursor: pointer;
            }
            .fortune-box {
                background-color: rgba(62, 39, 135, 0.2);
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                margin-top: 20px;
            }
            .fortune-text {
                font-size: 18px;
                font-style: italic;
                color: #fff59d;
            }
        </style>
    </head>
    <body>
        <h1>🔮 The Mystic Mirror of Destiny 🔮</h1>
        <p style='font-style: italic; color: #b39ddb;'>
            Gaze into the magical mirror and uncover the secrets that lie within your visage.
            The ancient spirits await to reveal your destiny...
        </p>
        <input type="file" id="fileInput" accept="image/*">
        <button class="button" onclick="uploadImage()">📸 Capture Your Essence</button>
        <div id="fortuneContainer"></div>
        <script>
            async function uploadImage() {
                const fileInput = document.getElementById('fileInput');
                if (fileInput.files.length === 0) {
                    alert("Please select an image file.");
                    return;
                }
                const file = fileInput.files[0];
                const formData = new FormData();
                formData.append('file', file);
                const response = await fetch('/detect_face/', {
                    method: 'POST',
                    body: formData
                });
                const result = await response.json();
                const fortuneContainer = document.getElementById('fortuneContainer');
                if (response.ok) {
                    fortuneContainer.innerHTML = `
                        <div class='fortune-box'>
                            <h3>Your Fortune Reveals:</h3>
                            <p class='fortune-text'>${result.fortune}</p>
                        </div>
                    `;
                } else {
                    fortuneContainer.innerHTML = `
                        <div class='fortune-box'>
                            <h3>Error:</h3>
                            <p class='fortune-text'>${result.detail}</p>
                        </div>
                    `;
                }
            }
        </script>
    </body>
    </html>
    """
"""
Telepathy REST API - FastAPI Backend for Voice Emotion Recognition
"""
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import numpy as np
import librosa
import tensorflow as tf
import joblib
import io
import os
from datetime import datetime
from pydantic import BaseModel

# Initialize FastAPI
app = FastAPI(
    title="Telepathy API",
    description="AI-powered Voice Emotion Recognition",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
model = None
scaler = None
label_encoder = None
SAMPLE_RATE = 44100
DURATION = 5

# Models
class PredictionResult(BaseModel):
    emotion: str
    confidence: float
    all_probabilities: dict
    timestamp: str

class HealthCheck(BaseModel):
    status: str
    model_loaded: bool
    supported_emotions: list

# Startup event
@app.on_event("startup")
async def load_models():
    """Load ML models on startup"""
    global model, scaler, label_encoder
    
    try:
        model = tf.keras.models.load_model("model_augmented.h5")
        scaler = joblib.load("scaler.pkl")
        label_encoder = joblib.load("label_encoder.pkl")
        print("✅ Models loaded successfully!")
    except Exception as e:
        print(f"❌ Error loading models: {e}")
        raise

# Helper functions
def extract_features(audio, sr):
    """Extract audio features"""
    mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=40)
    stft = np.abs(librosa.stft(audio))
    chroma = librosa.feature.chroma_stft(S=stft, sr=sr)
    spec_contrast = librosa.feature.spectral_contrast(S=stft, sr=sr)
    tonnetz = librosa.feature.tonnetz(y=librosa.effects.harmonic(audio), sr=sr)
    
    features = np.vstack([mfccs, chroma, spec_contrast, tonnetz]).T
    return features

def predict_emotion(audio):
    """Predict emotion from audio"""
    # Extract features
    features = extract_features(audio, SAMPLE_RATE)
    
    # Pad or truncate
    time_steps = model.input_shape[1]
    if features.shape[0] < time_steps:
        features = np.pad(features, ((0, time_steps - features.shape[0]), (0,0)), mode='constant')
    elif features.shape[0] > time_steps:
        features = features[:time_steps, :]
    
    # Scale features
    features_2d = features.reshape(1, -1)
    features_scaled_2d = scaler.transform(features_2d)
    features_scaled = features_scaled_2d.reshape(1, time_steps, features.shape[1])
    
    # Make prediction
    pred_probs = model.predict(features_scaled, verbose=0)
    pred_index = np.argmax(pred_probs)
    pred_label = label_encoder.inverse_transform([pred_index])[0]
    confidence = float(pred_probs[0][pred_index])
    
    # All probabilities
    all_probs = {
        emotion: float(prob) 
        for emotion, prob in zip(label_encoder.classes_, pred_probs[0])
    }
    
    return pred_label, confidence, all_probs

# Routes
@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main HTML page"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Telepathy - Voice Emotion Recognition</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            .container {
                background: white;
                border-radius: 20px;
                padding: 40px;
                max-width: 600px;
                width: 100%;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            }
            h1 {
                text-align: center;
                color: #667eea;
                margin-bottom: 10px;
                font-size: 2.5em;
            }
            .subtitle {
                text-align: center;
                color: #666;
                margin-bottom: 30px;
            }
            .upload-area {
                border: 3px dashed #667eea;
                border-radius: 10px;
                padding: 40px;
                text-align: center;
                cursor: pointer;
                transition: all 0.3s;
                margin-bottom: 20px;
            }
            .upload-area:hover {
                background: #f8f9ff;
                border-color: #764ba2;
            }
            .upload-icon { font-size: 3em; margin-bottom: 10px; }
            input[type="file"] { display: none; }
            .btn {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                padding: 15px 30px;
                border-radius: 10px;
                font-size: 1.1em;
                cursor: pointer;
                width: 100%;
                transition: transform 0.2s;
            }
            .btn:hover { transform: translateY(-2px); }
            .btn:disabled {
                opacity: 0.5;
                cursor: not-allowed;
            }
            .result {
                margin-top: 30px;
                padding: 20px;
                background: #f8f9ff;
                border-radius: 10px;
                display: none;
            }
            .result.show { display: block; }
            .emotion {
                font-size: 2em;
                font-weight: bold;
                text-align: center;
                color: #667eea;
                margin-bottom: 10px;
            }
            .confidence {
                text-align: center;
                color: #666;
                margin-bottom: 20px;
            }
            .prob-bar {
                margin: 10px 0;
            }
            .prob-label {
                display: flex;
                justify-content: space-between;
                margin-bottom: 5px;
                font-size: 0.9em;
            }
            .bar-container {
                background: #e0e0e0;
                border-radius: 5px;
                overflow: hidden;
                height: 25px;
            }
            .bar {
                height: 100%;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                transition: width 0.5s;
                display: flex;
                align-items: center;
                padding-left: 10px;
                color: white;
                font-size: 0.8em;
            }
            .loading {
                text-align: center;
                color: #667eea;
                display: none;
            }
            .loading.show { display: block; }
            .error {
                color: #e74c3c;
                text-align: center;
                margin-top: 10px;
            }
            .emoji {
                font-size: 3em;
                text-align: center;
                margin-bottom: 10px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🧠 Telepathy</h1>
            <p class="subtitle">AI-Powered Voice Emotion Recognition</p>
            
            <div class="upload-area" id="uploadArea" onclick="document.getElementById('fileInput').click()">
                <div class="upload-icon">🎤</div>
                <p>Click to upload audio file</p>
                <p style="font-size: 0.9em; color: #999; margin-top: 10px;">Supports WAV, MP3, OGG formats</p>
            </div>
            
            <input type="file" id="fileInput" accept="audio/*" onchange="uploadFile()">
            
            <div class="loading" id="loading">
                <p>🔮 Analyzing emotions...</p>
            </div>
            
            <div class="result" id="result">
                <div class="emoji" id="emoji"></div>
                <div class="emotion" id="emotion"></div>
                <div class="confidence" id="confidence"></div>
                
                <h3 style="margin-bottom: 15px;">Probability Distribution:</h3>
                <div id="probabilities"></div>
            </div>
            
            <p class="error" id="error"></p>
        </div>
        
        <script>
            const emotionEmojis = {
                'happy': '😊',
                'sad': '😢',
                'angry': '😠',
                'fearful': '😨',
                'neutral': '😐'
            };
            
            async function uploadFile() {
                const fileInput = document.getElementById('fileInput');
                const file = fileInput.files[0];
                
                if (!file) return;
                
                // Show loading
                document.getElementById('loading').classList.add('show');
                document.getElementById('result').classList.remove('show');
                document.getElementById('error').textContent = '';
                
                const formData = new FormData();
                formData.append('file', file);
                
                try {
                    const response = await fetch('/predict', {
                        method: 'POST',
                        body: formData
                    });
                    
                    if (!response.ok) {
                        throw new Error('Prediction failed');
                    }
                    
                    const data = await response.json();
                    displayResult(data);
                    
                } catch (error) {
                    document.getElementById('error').textContent = '❌ Error: ' + error.message;
                } finally {
                    document.getElementById('loading').classList.remove('show');
                }
            }
            
            function displayResult(data) {
                document.getElementById('result').classList.add('show');
                
                // Emotion and emoji
                const emotion = data.emotion;
                document.getElementById('emoji').textContent = emotionEmojis[emotion] || '🎭';
                document.getElementById('emotion').textContent = emotion.toUpperCase();
                document.getElementById('confidence').textContent = 
                    `Confidence: ${(data.confidence * 100).toFixed(2)}%`;
                
                // Probabilities
                const probsContainer = document.getElementById('probabilities');
                probsContainer.innerHTML = '';
                
                const probs = data.all_probabilities;
                const sortedEmotions = Object.keys(probs).sort((a, b) => probs[b] - probs[a]);
                
                sortedEmotions.forEach(emotion => {
                    const prob = probs[emotion];
                    const percentage = (prob * 100).toFixed(2);
                    
                    const barDiv = document.createElement('div');
                    barDiv.className = 'prob-bar';
                    barDiv.innerHTML = `
                        <div class="prob-label">
                            <span>${emotion}</span>
                            <span>${percentage}%</span>
                        </div>
                        <div class="bar-container">
                            <div class="bar" style="width: ${percentage}%"></div>
                        </div>
                    `;
                    probsContainer.appendChild(barDiv);
                });
            }
        </script>
    </body>
    </html>
    """

@app.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "supported_emotions": list(label_encoder.classes_) if label_encoder else []
    }

@app.post("/predict", response_model=PredictionResult)
async def predict(file: UploadFile = File(...)):
    """
    Predict emotion from uploaded audio file
    """
    if not model:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Read audio file
        contents = await file.read()
        audio_data = io.BytesIO(contents)
        
        # Load audio with librosa
        audio, sr = librosa.load(audio_data, sr=SAMPLE_RATE, duration=DURATION, mono=True)
        
        # Predict
        emotion, confidence, all_probs = predict_emotion(audio)
        
        return {
            "emotion": emotion,
            "confidence": confidence,
            "all_probabilities": all_probs,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing audio: {str(e)}")

@app.get("/api/emotions")
async def get_emotions():
    """Get list of supported emotions"""
    if not label_encoder:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return {"emotions": list(label_encoder.classes_)}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Telepathy API Server...")
    print("📍 Access the web interface at: http://localhost:8000")
    print("📖 API documentation at: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)

# 🚀 Telepathy - Quick Start Guide

Get up and running with Telepathy in 5 minutes!

---

## Prerequisites

- Python 3.11+ installed
- pip package manager
- Microphone (for live recording)
- Basic terminal/command line knowledge

---

## Installation

### 1. Clone or Download the Project

```bash
cd /Users/uditjainnnn/Telepathy
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**Expected installation time:** 2-3 minutes

### 3. Verify Installation

```bash
python3 -c "import tensorflow; import librosa; print('✅ All dependencies installed!')"
```

---

## Quick Start: Three Ways to Use Telepathy

### Option 1: Web Interface (Easiest)

**Start the API server:**
```bash
python3 api.py
```

**Open your browser:**
```
http://localhost:8000
```

**Upload an audio file and see the results!**

✨ The web interface has a beautiful UI with:
- Drag-and-drop file upload
- Real-time emotion analysis
- Confidence scores
- Probability distribution charts

---

### Option 2: Interactive CLI

**Run the interactive demo:**
```bash
python3 predict_interactive.py
```

**Choose an option:**
- `1` - Record from microphone (speak with emotion!)
- `2` - Test with sample files (demo mode)
- `3` - Exit

**Demo mode will test all emotions automatically!**

---

### Option 3: API (For Developers)

**Start the server:**
```bash
python3 api.py
```

**In another terminal, make API calls:**

#### Health Check
```bash
curl http://localhost:8000/health
```

#### Predict Emotion
```bash
curl -X POST http://localhost:8000/predict \
  -F "file=@sample_data/happy/happy_00.wav"
```

#### Response Format
```json
{
  "emotion": "happy",
  "confidence": 0.583,
  "all_probabilities": {
    "angry": 0.142,
    "fearful": 0.127,
    "happy": 0.583,
    "neutral": 0.083,
    "sad": 0.064
  },
  "timestamp": "2025-11-09T17:58:41.745724"
}
```

---

## Training Your Own Model (Optional)

If you want to train a fresh model:

### Using Sample Data (Quick Test)

```bash
# Generate sample data (if not already created)
python3 create_sample_data.py

# Train the model
python3 train_simple.py
```

**Training time:** ~5-10 minutes on CPU
**Expected accuracy:** ~100% (synthetic data)

### Using Real Datasets (Production)

**Step 1: Download datasets**
- RAVDESS: https://zenodo.org/record/1188976
- CREMA-D: https://github.com/CheyneyComputerScience/CREMA-D
- TESS: https://tspace.library.utoronto.ca/handle/1807/24487

**Step 2: Update paths in train_lstm.py**

**Step 3: Train**
```bash
python3 train_lstm.py
```

**Training time:** 2-3 hours (100 epochs)
**Expected accuracy:** 85-90%

---

## API Documentation

### Endpoints

#### `GET /`
Returns the web interface HTML

#### `GET /health`
Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "supported_emotions": ["angry", "fearful", "happy", "neutral", "sad"]
}
```

#### `POST /predict`
Predict emotion from audio file

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: `file` (audio file: WAV, MP3, OGG)

**Response:**
```json
{
  "emotion": "happy",
  "confidence": 0.583,
  "all_probabilities": {...},
  "timestamp": "2025-11-09T..."
}
```

**Error Responses:**
- `400` - Invalid audio file or format
- `503` - Model not loaded

#### `GET /api/emotions`
Get list of supported emotions

**Response:**
```json
{
  "emotions": ["angry", "fearful", "happy", "neutral", "sad"]
}
```

#### `GET /docs`
Interactive API documentation (Swagger UI)

---

## Integration Examples

### Python

```python
import requests

# Predict from file
with open('my_audio.wav', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/predict',
        files={'file': f}
    )
    result = response.json()
    print(f"Emotion: {result['emotion']}")
    print(f"Confidence: {result['confidence']:.2%}")
```

### JavaScript/Node.js

```javascript
const FormData = require('form-data');
const fs = require('fs');
const axios = require('axios');

const form = new FormData();
form.append('file', fs.createReadStream('my_audio.wav'));

axios.post('http://localhost:8000/predict', form, {
  headers: form.getHeaders()
})
.then(response => {
  console.log('Emotion:', response.data.emotion);
  console.log('Confidence:', response.data.confidence);
});
```

### cURL

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/audio.wav"
```

### Python with requests

```python
import requests

url = "http://localhost:8000/predict"
files = {"file": open("audio.wav", "rb")}
response = requests.post(url, files=files)
print(response.json())
```

---

## Supported Audio Formats

- **WAV** (recommended)
- **MP3**
- **OGG**
- **FLAC**
- **M4A**

**Recommended specs:**
- Sample rate: 44.1 kHz
- Channels: Mono
- Duration: 3-10 seconds
- Bit depth: 16-bit

---

## Tips for Best Results

### Audio Quality
✅ **DO:**
- Use clear, high-quality recordings
- Record in quiet environment
- Speak naturally with emotion
- Keep audio 3-10 seconds

❌ **DON'T:**
- Use heavily compressed audio
- Include background noise/music
- Use very short clips (<1 second)
- Use robotic/synthesized voices

### Emotions to Express
- **Happy:** Upbeat, energetic, positive tone
- **Sad:** Low energy, slow, downcast tone
- **Angry:** Loud, intense, aggressive tone
- **Fearful:** Shaky, anxious, worried tone
- **Neutral:** Calm, even, matter-of-fact tone

---

## Troubleshooting

### Problem: "Model not found"
**Solution:** Train the model first:
```bash
python3 train_simple.py
```

### Problem: "Module not found"
**Solution:** Install dependencies:
```bash
pip install -r requirements.txt
```

### Problem: "Port 8000 already in use"
**Solution:** Kill the existing process:
```bash
lsof -ti:8000 | xargs kill -9
```

Or use a different port:
```bash
uvicorn api:app --port 8001
```

### Problem: "Microphone not accessible"
**Solution:** Grant microphone permissions:
- macOS: System Preferences → Security & Privacy → Microphone
- Windows: Settings → Privacy → Microphone

### Problem: Low accuracy predictions
**Solution:** 
1. Train on real datasets (not synthetic)
2. Ensure audio quality is good
3. Use 5+ second audio clips
4. Check that emotion is clearly expressed

---

## Advanced Usage

### Batch Processing

```python
import requests
from pathlib import Path

audio_files = Path('audio_folder').glob('*.wav')

results = []
for file in audio_files:
    with open(file, 'rb') as f:
        response = requests.post(
            'http://localhost:8000/predict',
            files={'file': f}
        )
        results.append({
            'file': file.name,
            'emotion': response.json()['emotion']
        })

print(results)
```

### Streaming Audio (Coming Soon)

```python
# WebSocket streaming support planned
import asyncio
import websockets

async def stream_audio():
    async with websockets.connect('ws://localhost:8000/ws/stream') as ws:
        # Stream audio chunks
        for chunk in audio_stream:
            await ws.send(chunk)
            emotion = await ws.recv()
            print(f"Current emotion: {emotion}")
```

---

## Performance Benchmarks

**Current Performance (Local):**
- Response time: ~1.5s per 5s audio
- Memory usage: ~500MB
- Throughput: ~0.67 requests/second

**Production Target:**
- Response time: <500ms
- Memory usage: <1GB
- Throughput: >10 requests/second

---

## Project Structure

```
Telepathy/
├── api.py                      # FastAPI web server
├── predict_interactive.py      # Interactive CLI demo
├── predict_voice.py           # Original prediction script
├── train_simple.py            # Training script (sample data)
├── train_lstm.py              # Training script (real datasets)
├── create_sample_data.py      # Generate synthetic data
├── requirements.txt           # Python dependencies
├── README.md                  # Project overview
├── PROJECT_CONTEXT.md         # Technical documentation
├── BUSINESS_PLAN.md           # Business strategy
├── MARKETING_STRATEGY.md      # Marketing materials
├── IMPROVEMENT_ROADMAP.md     # Product roadmap
├── EXECUTIVE_SUMMARY.md       # Investor pitch
├── QUICK_START.md             # This file
├── sample_data/               # Synthetic training data
│   ├── angry/
│   ├── fearful/
│   ├── happy/
│   ├── neutral/
│   └── sad/
├── model_augmented.h5         # Trained model
├── scaler.pkl                 # Feature scaler
└── label_encoder.pkl          # Label encoder
```

---

## FAQ

**Q: How accurate is the model?**
A: 100% on synthetic data, 85-90% expected on real voices with proper training.

**Q: Can I use this commercially?**
A: Yes! Check LICENSE file for details. Contact for commercial licensing.

**Q: What's the API rate limit?**
A: Currently none (local). Production will have tiered limits.

**Q: Can I train on custom emotions?**
A: Yes! Modify the training script to include your own labels.

**Q: Does it work in real-time?**
A: Yes for files. WebSocket streaming coming soon for true real-time.

**Q: Is it GDPR/HIPAA compliant?**
A: Not yet. Production version will be compliant.

**Q: Can I deploy to production?**
A: MVP is functional but needs hardening. See IMPROVEMENT_ROADMAP.md.

**Q: How can I contribute?**
A: Issues and PRs welcome! Contact for collaboration.

---

## Resources

### Documentation
- 📚 Full API Docs: http://localhost:8000/docs
- 🔧 Technical Details: PROJECT_CONTEXT.md
- 🚀 Improvement Plan: IMPROVEMENT_ROADMAP.md

### Support
- 📧 Email: [your-email]
- 💬 Discord: [coming soon]
- 🐛 Issues: [GitHub issues]

### Learning
- 📖 Audio ML: librosa.org/doc/latest
- 🧠 Deep Learning: tensorflow.org/tutorials
- 🎤 Voice AI: papers on emotion recognition

---

## Next Steps

### For Developers
1. ✅ Run the web interface
2. ✅ Test the API with sample files
3. ✅ Try recording your own voice
4. 🔲 Read the API documentation
5. 🔲 Integrate into your app

### For Business Users
1. ✅ Try the demo
2. ✅ Review the business plan
3. 🔲 Schedule a product demo
4. 🔲 Discuss custom solutions
5. 🔲 Get pricing quote

### For Investors
1. ✅ Read executive summary
2. ✅ Try the product demo
3. 🔲 Review financial model
4. 🔲 Schedule due diligence call
5. 🔲 Make investment decision

---

## Success! 🎉

You're now ready to use Telepathy for emotion recognition!

**What's next?**
- Explore the web interface
- Test with your own audio
- Read the business plan
- Join our community
- Build something amazing!

---

**Need help?** Open an issue or contact support.

**Want to contribute?** PRs are welcome!

**Ready to scale?** Let's talk: [contact info]

---

*Built with ❤️ for emotional intelligence*

**Last Updated:** November 9, 2025
**Version:** 1.0.0 (MVP)

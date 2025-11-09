# 🚀 Telepathy Deployment Instructions

## Quick Deployment Guide for Render and Vercel

---

## ✅ OPTION 1: Deploy to Render (Recommended - Free Tier)

Render is the **best choice** for this Python FastAPI application because:
- ✅ Native Python support
- ✅ Free tier available
- ✅ Auto-detects render.yaml configuration
- ✅ Handles background jobs (model training)
- ✅ Persistent storage for model files

### Steps to Deploy on Render:

1. **Push to GitHub** (if not already done):
   ```bash
   cd ~/Telepathy
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Deploy on Render**:
   - Go to https://render.com
   - Click "New +" → "Web Service"
   - Click "Connect a repository" and authorize GitHub
   - Select the `telepathy-voice-ai` repository
   - Render will **auto-detect** the `render.yaml` file
   - Click "Create Web Service"

3. **Wait for Build** (5-10 minutes):
   - Render will:
     - Install Python dependencies
     - Generate sample training data
     - Train the ML model
     - Start the API server
   
4. **Get Your URL**:
   - Your API will be live at: `https://telepathy-api.onrender.com`
   - Access the web interface at that URL
   - API docs at: `https://telepathy-api.onrender.com/docs`

### Environment Variables (Optional):
If you need to customize, go to Settings → Environment and add:
- `PYTHON_VERSION`: 3.11.4
- `PORT`: 8000

---

## ⚠️ OPTION 2: Deploy to Vercel (Limited Support)

**Important Note**: Vercel is optimized for serverless functions and has limitations for Python FastAPI:
- ⚠️ File system is read-only (can't save trained models)
- ⚠️ 10-second timeout limit on functions
- ⚠️ No persistent storage
- ⚠️ Better suited for static sites and Node.js

### If you still want to try Vercel:

1. **Pre-train the model locally**:
   ```bash
   cd ~/Telepathy
   python create_sample_data.py
   python train_simple.py
   ```

2. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

3. **Deploy**:
   ```bash
   cd ~/Telepathy
   vercel
   ```
   
4. **Follow prompts**:
   - Login to Vercel
   - Set up project
   - Deploy

5. **Note**: The model training won't work on Vercel. You'll need to:
   - Train models locally
   - Commit model files (model_augmented.h5, scaler.pkl, label_encoder.pkl) to git
   - Deploy with pre-trained models

---

## 🎯 OPTION 3: Deploy Frontend to Vercel + Backend to Render (Best Practice)

This is the **recommended production setup**:

### Backend (API) on Render:
1. Follow "Option 1" above to deploy API to Render
2. Note your API URL: `https://telepathy-api.onrender.com`

### Frontend on Vercel:
1. Create a separate Next.js or static site for the frontend
2. Update API calls to point to Render URL
3. Deploy to Vercel:
   ```bash
   cd ~/Telepathy/frontend
   vercel
   ```

---

## 📊 Post-Deployment Checklist

After deploying, test these endpoints:

### 1. Health Check
```bash
curl https://your-app-url.com/health
```
Expected response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "supported_emotions": ["happy", "sad", "angry", "fearful", "neutral"]
}
```

### 2. Web Interface
- Open: `https://your-app-url.com`
- Upload a test audio file
- Verify emotion prediction works

### 3. API Documentation
- Open: `https://your-app-url.com/docs`
- Swagger UI should load with all endpoints

### 4. Test Prediction API
```bash
curl -X POST "https://your-app-url.com/predict" \
  -F "file=@test_audio.wav"
```

---

## 🔧 Troubleshooting

### Render Issues:

**Build fails:**
```bash
# Check logs in Render dashboard
# Common fixes:
- Verify requirements.txt has all dependencies
- Check Python version (3.11.4 recommended)
- Ensure build.sh has execute permissions
```

**Model not loading:**
```bash
# Ensure build.sh runs training:
pip install -r requirements.txt
python create_sample_data.py
python train_simple.py
```

**503 Service Unavailable:**
- Free tier spins down after 15 min inactivity
- First request may take 30-60 seconds to wake up
- Consider upgrading to paid tier for always-on

### Vercel Issues:

**Function timeout:**
- Vercel has 10-second limit on free tier
- Model training/loading may exceed this
- Solution: Use pre-trained models only

**Module not found:**
- Some packages (like tensorflow) are too large for Vercel
- Consider using lighter ML models
- Or deploy backend to Render instead

---

## 💰 Pricing Comparison

| Platform | Free Tier | Best For | Cost (Paid) |
|----------|-----------|----------|-------------|
| **Render** | 750 hrs/month | Python APIs | $7-25/month |
| **Vercel** | 100 GB-hours | Static sites, Next.js | $20/month |
| **Both** | Free + Free | Production apps | $27/month |

---

## 🚀 Quick Commands

### Deploy to Render:
```bash
# Already configured! Just push to GitHub
git push origin main
# Then connect repo on render.com
```

### Deploy to Vercel:
```bash
# Install CLI
npm i -g vercel

# Deploy
cd ~/Telepathy
vercel

# Production deploy
vercel --prod
```

### Update Deployment:
```bash
# Make changes
git add .
git commit -m "Update"
git push origin main

# Render auto-deploys on push!
# For Vercel, run: vercel --prod
```

---

## 📱 Accessing Your Deployed App

### Render URL Format:
```
https://telepathy-api.onrender.com
https://telepathy-api.onrender.com/docs
https://telepathy-api.onrender.com/health
```

### Vercel URL Format:
```
https://telepathy-voice-ai.vercel.app
https://telepathy-voice-ai-username.vercel.app
```

### Custom Domain (Both platforms):
1. Go to Settings → Domains
2. Add your domain (e.g., api.telepathy.ai)
3. Update DNS records as instructed
4. SSL auto-configured ✅

---

## 🎉 Success Indicators

You'll know deployment succeeded when:

✅ Build completes without errors
✅ Health endpoint returns `"status": "healthy"`
✅ Web interface loads and accepts uploads
✅ Prediction returns emotion results
✅ No errors in platform logs
✅ Response time < 3 seconds

---

## 📞 Support

**Render Issues:**
- Docs: https://render.com/docs
- Community: https://community.render.com

**Vercel Issues:**
- Docs: https://vercel.com/docs
- Community: https://github.com/vercel/vercel/discussions

**Project Issues:**
- GitHub: https://github.com/Labdhimandovara/telepathy-voice-ai/issues

---

## 🎯 Recommended Approach

**For Your Use Case:**

1. ✅ **Deploy API to Render** (using existing render.yaml)
2. ✅ Use Render's free tier to start
3. ✅ Optional: Deploy static landing page to Vercel
4. ✅ Upgrade Render to paid tier when needed

**Why Render for Backend:**
- Python FastAPI fully supported
- Model training works in build step
- Persistent file storage
- Simple configuration with render.yaml

**Why Vercel for Frontend (optional):**
- Fast CDN for static assets
- Great for React/Next.js frontends
- Free SSL and custom domains
- Lightning-fast deployments

---

**Good luck with your deployment! 🚀**

*Generated: November 9, 2024*

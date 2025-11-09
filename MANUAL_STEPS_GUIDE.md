# 🎯 STEP-BY-STEP MANUAL DEPLOYMENT GUIDE

## 📍 WHERE YOU ARE NOW

✅ **Completed:**
- Frontend is LIVE on Vercel: https://frontend-lp3etj38b-labdhi-mandovaras-projects.vercel.app
- All code is on GitHub: https://github.com/Labdhimandovara/telepathy-voice-ai
- Everything is configured and ready

⏳ **What's Left:**
- Deploy backend API to Render (5 minutes)
- Connect frontend to backend (1 minute)

---

## 🚀 STEP 1: DEPLOY BACKEND TO RENDER

### 1.1 Open Render Dashboard

Go to this URL (I should have opened it for you):
```
https://dashboard.render.com/select-repo?type=blueprint
```

Or manually go to:
1. https://dashboard.render.com/
2. Click the blue **"New +"** button (top right)
3. Select **"Blueprint"** from the dropdown

### 1.2 Connect Your GitHub Repository

You'll see a page titled **"Create services from a blueprint"**

**What to do:**

1. **Find your repository:**
   - Look for **"telepathy-voice-ai"** in the list
   - It should show: `Labdhimandovara/telepathy-voice-ai`

2. **Click the blue "Connect" button** next to it

   **If you don't see your repo:**
   - Click **"Configure account"** or **"Connect GitHub"**
   - Authorize Render to access your GitHub
   - Select "All repositories" or just "telepathy-voice-ai"
   - Click "Install" or "Save"
   - Go back and refresh

### 1.3 Review Blueprint Configuration

After clicking "Connect", Render will read your `render.yaml` file and show:

**Service Name:** `telepathy-api`

**Configuration Preview:**
```
Type: Web Service
Build Command: ./build.sh
Start Command: uvicorn api:app --host 0.0.0.0 --port $PORT
Region: Oregon
Plan: Free
```

**What to do:**
1. **Review the settings** (they're already perfect!)
2. Scroll down to the bottom
3. Click the blue **"Apply"** button

### 1.4 Wait for Deployment

**What happens now:**

Render will start building and deploying your API:

1. **Initializing** (10 seconds)
   - Setting up the environment
   
2. **Building** (5-10 minutes) ⏰
   - Installing Python packages
   - Running `build.sh`
   - Generating 100 audio samples
   - Training the LSTM model (this takes time!)
   - Saving the trained model

3. **Deploying** (30 seconds)
   - Starting the API server
   - Health checks

**How to watch progress:**
- You'll see a live log stream
- Green text = good
- Look for: "✅ Build completed successfully!"
- Then: "Your service is live 🎉"

### 1.5 Get Your Backend URL

Once deployed, you'll see:

**Your service is live at:**
```
https://telepathy-api-XXXXX.onrender.com
```

**Copy this URL!** You'll need it for Step 2.

**Example URLs:**
- https://telepathy-api.onrender.com
- https://telepathy-api-abc123.onrender.com

**To find it later:**
- Go to https://dashboard.render.com/
- Click on "telepathy-api"
- See the URL at the top

---

## 🔗 STEP 2: CONNECT FRONTEND TO BACKEND

Now you need to tell your frontend where the backend API is.

### 2.1 Copy Your Backend URL

From Render dashboard, copy the full URL:
```
https://telepathy-api-XXXXX.onrender.com
```

### 2.2 Run the Update Script

Open Terminal and run:

```bash
cd /Users/uditjainnnn/Telepathy
./update-frontend.sh https://telepathy-api-XXXXX.onrender.com
```

**Replace with your actual URL!**

**What this script does:**
1. Opens `frontend/index.html`
2. Replaces `API_URL_PLACEHOLDER` with your Render URL
3. Deploys updated frontend to Vercel
4. Shows you the new frontend URL

**Expected output:**
```
🔧 Updating frontend with backend URL...
Backend URL: https://telepathy-api-XXXXX.onrender.com
✅ Updated index.html

🚀 Deploying to Vercel...
✅ Production: https://frontend-lp3etj38b...vercel.app

✅ Frontend updated and deployed!

Your app is now fully live! 🎉
```

---

## ✅ STEP 3: TEST YOUR APP

### 3.1 Open Your Frontend

Go to: https://frontend-lp3etj38b-labdhi-mandovaras-projects.vercel.app

You should see:
- Beautiful purple gradient background
- "🧠 Telepathy" title
- "AI-Powered Voice Emotion Recognition" subtitle
- Green "✅ API Online" status (wait 30 seconds if it's red)
- Upload area with microphone icon

### 3.2 Test It!

**Option A: Use a sample file**
```bash
# Get a sample file
open /Users/uditjainnnn/Telepathy/sample_data/happy/
```
- Drag one of the `.wav` files to your browser
- Drop it on the upload area
- Wait 2-3 seconds
- See the emotion result!

**Option B: Record your own voice**
- Use QuickTime or Voice Memos to record yourself
- Say something with emotion (happy, sad, angry, etc.)
- Save as `.wav` or `.mp3`
- Upload to the website

### 3.3 Check the Result

You should see:
- 😊 Emoji for the emotion
- **HAPPY** (or other emotion) in large text
- **Confidence: 58.32%** (or similar)
- Colorful probability bars showing all emotions

---

## 🎉 YOU'RE DONE!

Your AI app is now fully live on the internet!

**Share these URLs:**
- 🌐 Frontend: https://frontend-lp3etj38b-labdhi-mandovaras-projects.vercel.app
- 🔧 Backend: https://telepathy-api-XXXXX.onrender.com
- 📖 GitHub: https://github.com/Labdhimandovara/telepathy-voice-ai

---

## 🐛 TROUBLESHOOTING

### Problem 1: "⚠️ API Offline" in Frontend

**Cause:** Backend is still starting up (first time takes 30-60 seconds)

**Solution:**
1. Wait 30 seconds
2. Refresh the page
3. Check Render dashboard - is it still deploying?

### Problem 2: "API may be starting up, try again in 30 seconds"

**Cause:** Render free tier "spins down" after 15 minutes of inactivity

**Solution:**
- First request wakes it up (takes 30 seconds)
- Try again after 30 seconds
- This is normal for free tier

### Problem 3: Build Fails on Render

**Causes & Solutions:**

**If it says "Command not found: ./build.sh"**
- The file might not be executable
- Go to GitHub repo → build.sh → Edit
- Make sure it starts with `#!/bin/bash`

**If it says "Timeout after 15 minutes"**
- Model training took too long
- This shouldn't happen with our simple model
- Check Render logs for actual error

**If it says "No module named 'tensorflow'"**
- requirements.txt wasn't read
- Check that requirements.txt is in the root directory
- Re-trigger deploy from Render dashboard

### Problem 4: Frontend Shows "Prediction failed"

**Cause:** Backend URL is wrong or backend is down

**Solution:**
1. Check backend is running: `curl https://your-render-url.onrender.com/health`
2. Should return: `{"status":"healthy","model_loaded":true}`
3. Check frontend has correct URL:
   - View source of frontend page
   - Find: `const API_URL = '...'`
   - Make sure it's your Render URL

### Problem 5: CORS Error in Browser Console

**Cause:** Backend not allowing frontend domain

**Solution:**
- Our backend already has CORS enabled for all domains
- This shouldn't happen
- If it does, check Render logs for errors

---

## 📊 WHAT HAPPENS DURING BUILD

Understanding what Render does (so you know what's normal):

### Phase 1: Environment Setup (1 minute)
```
==> Cloning from https://github.com/Labdhimandovara/telepathy-voice-ai...
==> Checking out commit abc123...
==> Using Python version 3.11.4
```

### Phase 2: Build (5-10 minutes)
```
==> Running build command: ./build.sh
🚀 Starting Telepathy deployment build...
📦 Installing Python dependencies...
  - Installing numpy...
  - Installing tensorflow... (this takes time!)
  - Installing librosa...
🎵 Generating sample training data...
  Created 20 samples for neutral
  Created 20 samples for happy
  ... (100 total)
🏋️ Training model...
  Epoch 1/50 ... (this takes 5+ minutes!)
  ...
  Epoch 50/50
✅ Build completed successfully!
```

### Phase 3: Deploy (30 seconds)
```
==> Starting service...
==> uvicorn api:app --host 0.0.0.0 --port $PORT
🧠 Loading Telepathy AI model...
✅ Models loaded successfully!
INFO: Application startup complete
==> Your service is live! 🎉
```

**Total time: 6-12 minutes**

---

## 📝 DETAILED TIMING EXPECTATIONS

| Step | Time | What You'll See |
|------|------|-----------------|
| Click "Apply" | Instant | Build starts |
| Installing deps | 1-2 min | Lots of package names |
| Generating audio | 1 min | Progress messages |
| Training model | 5-8 min | Epoch progress bars |
| Starting service | 30 sec | "Your service is live" |
| **TOTAL** | **8-12 min** | Green success message |

---

## 🎬 VISUAL GUIDE

### What Render Dashboard Looks Like:

**Before Deployment:**
```
+------------------------------------------+
|  Create services from a blueprint        |
+------------------------------------------+
|                                          |
|  Labdhimandovara/telepathy-voice-ai     |
|  [Connect]  <-- Click this!             |
|                                          |
+------------------------------------------+
```

**After Clicking Connect:**
```
+------------------------------------------+
|  Blueprint: telepathy-voice-ai           |
+------------------------------------------+
|                                          |
|  Service Name: telepathy-api             |
|  Type: Web Service                       |
|  Build: ./build.sh                       |
|  Start: uvicorn api:app...              |
|  Region: Oregon                          |
|  Plan: Free                              |
|                                          |
|  [Apply]  <-- Click this!               |
+------------------------------------------+
```

**During Build:**
```
+------------------------------------------+
|  telepathy-api                           |
+------------------------------------------+
|  Status: ⏳ Building...                  |
|                                          |
|  Live logs:                              |
|  > Cloning repository...                 |
|  > Installing dependencies...            |
|  > Training model...                     |
|  > Epoch 15/50...                        |
+------------------------------------------+
```

**After Success:**
```
+------------------------------------------+
|  telepathy-api                           |
+------------------------------------------+
|  Status: ✅ Live                         |
|                                          |
|  https://telepathy-api-xxx.onrender.com  |
|                                          |
|  [Logs] [Settings] [Shell]              |
+------------------------------------------+
```

---

## 💡 TIPS

1. **Keep Render tab open** while building - you can watch progress

2. **Don't close browser** - build continues even if you do, but you won't see progress

3. **Free tier sleep** - After 15 min of no requests, service sleeps
   - First request after sleep: 30-60 seconds to wake up
   - This is normal!

4. **Copy URLs immediately** - You'll need them for documentation

5. **Test with sample files first** - Before recording your own

6. **Share your app!** - Post on Twitter/LinkedIn with both URLs

---

## 🎯 CHECKLIST

Copy this and check off as you go:

```
□ Step 1.1: Opened Render Blueprint page
□ Step 1.2: Found telepathy-voice-ai repo
□ Step 1.2: Clicked "Connect"
□ Step 1.3: Reviewed configuration
□ Step 1.3: Clicked "Apply"
□ Step 1.4: Waited 8-12 minutes for build
□ Step 1.5: Copied backend URL
□ Step 2.1: Copied backend URL again (to clipboard)
□ Step 2.2: Ran update-frontend.sh with URL
□ Step 3.1: Opened frontend URL
□ Step 3.2: Tested with sample file
□ Step 3.3: Saw emotion result
□ DONE: App is fully live! 🎉
```

---

## 📞 NEED HELP?

If something goes wrong:

1. **Check Render logs:**
   - Go to Render dashboard
   - Click "telepathy-api"
   - Click "Logs" tab
   - Look for red error messages

2. **Check browser console:**
   - Open frontend
   - Press F12 (Chrome DevTools)
   - Click "Console" tab
   - Look for red errors

3. **Verify files on GitHub:**
   - Go to https://github.com/Labdhimandovara/telepathy-voice-ai
   - Check these files exist:
     - render.yaml
     - build.sh
     - api.py
     - requirements.txt

4. **Re-trigger deploy:**
   - In Render dashboard
   - Click "Manual Deploy"
   - Select "Clear build cache & deploy"

---

## 🎊 AFTER SUCCESS

Once everything works:

1. **Update README with live URLs**
2. **Share on social media**
3. **Submit to Product Hunt**
4. **Show to potential investors/customers**
5. **Add custom domain (optional)**
6. **Monitor usage in Render dashboard**

---

**Good luck! You're so close! 🚀**

*Built with ❤️ - November 9, 2025*

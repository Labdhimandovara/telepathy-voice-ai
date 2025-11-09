# 🚀 Quick Deploy Guide - Telepathy Voice AI

## Choose Your Platform

### ✅ OPTION 1: Render (Recommended)
**Best for:** Python FastAPI backend with ML models

```bash
cd ~/Telepathy
./deploy-to-render.sh
```

**Then:**
1. Go to https://render.com
2. Connect your GitHub repo
3. Click "Create Web Service"
4. Done! 🎉

**Your app will be live at:** `https://telepathy-api.onrender.com`

---

### ⚠️ OPTION 2: Vercel (Limited)
**Best for:** Static frontends (NOT recommended for this ML backend)

```bash
cd ~/Telepathy
./deploy-to-vercel.sh
```

**Note:** Vercel has limitations for Python ML apps:
- 10-second timeout
- No persistent storage
- Can't train models on serverless

---

## What Each Script Does

### `deploy-to-render.sh`
- ✅ Checks git status
- ✅ Commits changes if needed
- ✅ Pushes to GitHub
- ✅ Opens Render dashboard
- ✅ Step-by-step instructions

### `deploy-to-vercel.sh`
- ⚠️ Trains models locally first
- ⚠️ Installs Vercel CLI if needed
- ⚠️ Deploys with pre-trained models
- ⚠️ Shows deployment URL

---

## Manual Deployment

### Render (Manual)
1. Push to GitHub:
   ```bash
   git add .
   git commit -m "Deploy to Render"
   git push origin main
   ```

2. On Render.com:
   - New + → Web Service
   - Connect repository
   - Auto-detects `render.yaml`
   - Create Web Service

### Vercel (Manual)
1. Install Vercel CLI:
   ```bash
   npm install -g vercel
   ```

2. Deploy:
   ```bash
   vercel --prod
   ```

---

## Testing Your Deployment

After deployment, test these URLs:

```bash
# Health check
curl https://your-app-url.com/health

# Web interface
open https://your-app-url.com

# API docs
open https://your-app-url.com/docs
```

---

## Need Help?

- 📖 Full guide: `DEPLOYMENT_INSTRUCTIONS.md`
- 📚 Original docs: `DEPLOYMENT_GUIDE.md`
- 🐛 Issues: GitHub Issues tab

---

**Recommended: Use Render for this ML application! 🎯**

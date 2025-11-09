# 🚀 Telepathy Deployment Guide

## Quick Deploy Options

### Option 1: Render (Recommended - Free Tier Available)

#### Automatic Deployment

1. **Push to GitHub:**
   ```bash
   cd /Users/uditjainnnn/Telepathy
   git add .
   git commit -m "Initial commit - Telepathy MVP"
   git push origin main
   ```

2. **Deploy on Render:**
   - Go to https://render.com
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select "telepathy" repository
   - Render will auto-detect the `render.yaml` file
   - Click "Create Web Service"

3. **That's it!** Render will:
   - Install dependencies
   - Generate sample data
   - Train the model
   - Deploy your API
   - Give you a URL like: `https://telepathy-api.onrender.com`

#### Manual Setup (Alternative)

If auto-detection doesn't work:

```yaml
Build Command: ./build.sh
Start Command: uvicorn api:app --host 0.0.0.0 --port $PORT
```

---

### Option 2: Docker (Any Cloud Platform)

#### Build and Run Locally
```bash
cd /Users/uditjainnnn/Telepathy

# Build image
docker build -t telepathy-api .

# Run container
docker run -p 8000:8000 telepathy-api
```

#### Deploy to Cloud

**Google Cloud Run:**
```bash
# Build and push
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/telepathy-api

# Deploy
gcloud run deploy telepathy-api \
  --image gcr.io/YOUR_PROJECT_ID/telepathy-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

**AWS ECS/Fargate:**
```bash
# Build and push to ECR
aws ecr create-repository --repository-name telepathy-api
docker tag telepathy-api:latest YOUR_ACCOUNT.dkr.ecr.REGION.amazonaws.com/telepathy-api:latest
docker push YOUR_ACCOUNT.dkr.ecr.REGION.amazonaws.com/telepathy-api:latest

# Deploy to ECS (use AWS Console or CLI)
```

**Azure Container Instances:**
```bash
az container create \
  --resource-group telepathy-rg \
  --name telepathy-api \
  --image telepathy-api:latest \
  --dns-name-label telepathy-api \
  --ports 8000
```

---

### Option 3: Railway (Easy & Fast)

1. **Install Railway CLI:**
   ```bash
   npm install -g @railway/cli
   ```

2. **Deploy:**
   ```bash
   cd /Users/uditjainnnn/Telepathy
   railway login
   railway init
   railway up
   ```

3. **Your app will be live at:** `https://YOUR_APP.railway.app`

---

### Option 4: Vercel (For Static/Serverless)

⚠️ **Note:** Vercel is optimized for Node.js and serverless functions. For Python FastAPI, use Render or Railway instead.

If you still want to try:

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd /Users/uditjainnnn/Telepathy
vercel
```

You'll need to add a `vercel.json`:
```json
{
  "builds": [
    {
      "src": "api.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "api.py"
    }
  ]
}
```

---

### Option 5: Fly.io (Global Edge Deployment)

1. **Install Fly CLI:**
   ```bash
   brew install flyctl  # macOS
   ```

2. **Deploy:**
   ```bash
   cd /Users/uditjainnnn/Telepathy
   flyctl launch
   flyctl deploy
   ```

---

## Environment Variables (If Needed)

For production deployments, you may want to set:

```bash
# Optional environment variables
PYTHON_VERSION=3.11.4
PORT=8000
MODEL_PATH=./model_augmented.h5
MAX_UPLOAD_SIZE=10485760  # 10MB
```

---

## Post-Deployment Checklist

After deploying, verify:

1. **Health Check:** `https://your-app-url.com/health`
   - Should return: `{"status":"healthy","model_loaded":true}`

2. **API Docs:** `https://your-app-url.com/docs`
   - Swagger UI should load

3. **Test Prediction:** Upload a sample audio file

4. **Performance:**
   - Response time < 2 seconds
   - No errors in logs

---

## Scaling Considerations

### Free Tier Limitations
- **Render Free:** Spins down after 15 min inactivity
- **Railway Free:** 500 hours/month
- **Fly.io Free:** 3 shared-cpu-1x VMs

### Production Requirements (Paid Tiers)
- **CPU:** 2+ cores recommended
- **RAM:** 2GB minimum, 4GB recommended
- **Storage:** 10GB (for model files)
- **Bandwidth:** Depends on usage

### Estimated Costs (Monthly)
- **Hobby/Small:** $7-15 (Render, Railway)
- **Production:** $25-50 (better instances)
- **Enterprise:** $100+ (auto-scaling, load balancing)

---

## Monitoring & Logs

### Check Deployment Status

**Render:**
```bash
# View logs in dashboard or CLI
render logs -s telepathy-api
```

**Railway:**
```bash
railway logs
```

**Fly.io:**
```bash
flyctl logs
```

---

## Troubleshooting

### Build Fails
- Check `build.sh` runs successfully locally
- Verify all dependencies in `requirements.txt`
- Check Python version compatibility

### Model Not Loading
- Ensure `build.sh` runs training script
- Check file paths are relative, not absolute
- Verify model files are generated during build

### Port Issues
- Use `${PORT}` environment variable
- Render/Railway inject PORT automatically
- Default to 8000 if PORT not set

### Timeout Issues
- Increase build timeout in platform settings
- Model training might take 5-10 minutes
- Consider pre-trained models for faster deploys

---

## Custom Domain Setup

### Render
1. Go to Settings → Custom Domain
2. Add your domain: `api.telepathy.ai`
3. Update DNS records as shown
4. SSL auto-configured

### Railway
```bash
railway domain
```

### Fly.io
```bash
flyctl certs create api.telepathy.ai
```

---

## CI/CD (Continuous Deployment)

### GitHub Actions (Auto-deploy on push)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Render

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Render
        run: |
          curl -X POST "https://api.render.com/v1/services/${{ secrets.RENDER_SERVICE_ID }}/deploys" \
            -H "Authorization: Bearer ${{ secrets.RENDER_API_KEY }}"
```

---

## Security Checklist

- [ ] Add API key authentication (see IMPROVEMENT_ROADMAP.md)
- [ ] Rate limiting configured
- [ ] HTTPS enabled (auto on most platforms)
- [ ] Environment variables for secrets
- [ ] CORS configured properly
- [ ] Input validation on file uploads
- [ ] Error messages don't leak sensitive info

---

## Next Steps After Deployment

1. **Update Documentation:**
   - Replace `localhost:8000` with your live URL
   - Update README.md with live demo link

2. **Share Your API:**
   - Post on Twitter/LinkedIn
   - Submit to Product Hunt
   - Add to API marketplaces

3. **Monitor Usage:**
   - Set up analytics
   - Track API calls
   - Monitor errors

4. **Iterate:**
   - Gather user feedback
   - Improve model accuracy
   - Add requested features

---

## Example Deployment Commands

### Quick Deploy to Render (Recommended)

```bash
cd /Users/uditjainnnn/Telepathy

# Make sure you have a GitHub repo
gh repo create telepathy --public --source=. --remote=origin

# Add all files
git add .
git commit -m "🚀 Initial deployment - Telepathy MVP"
git push -u origin main

# Go to render.com and connect the repo!
```

### Quick Deploy to Railway

```bash
cd /Users/uditjainnnn/Telepathy

# One command deploy
railway login
railway init
railway up

# Get your URL
railway domain
```

---

## Support & Resources

- **Documentation:** Check all `.md` files in this repo
- **Issues:** Open GitHub issues for bugs
- **Questions:** See QUICK_START.md for FAQs

---

**Your API will be live in minutes! 🚀**

Choose Render for easiest deployment with free tier.
Choose Railway for fastest deployment.
Choose Docker for maximum flexibility.

---

*Last Updated: November 9, 2025*

#!/bin/bash
# Automated deployment script for Telepathy

set -e  # Exit on any error

echo "🚀 TELEPATHY AUTOMATED DEPLOYMENT"
echo "=================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Push to GitHub
echo -e "${BLUE}📤 Step 1: Pushing to GitHub...${NC}"
cd /Users/uditjainnnn/Telepathy

git push -u origin main 2>&1

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Successfully pushed to GitHub!${NC}"
else
    echo -e "${YELLOW}⚠️  GitHub push failed. Make sure you created the repo at: https://github.com/new${NC}"
    echo "   Name: telepathy-voice-ai"
    echo "   Visibility: Public"
    exit 1
fi

echo ""

# Step 2: Open Render dashboard
echo -e "${BLUE}📡 Step 2: Opening Render dashboard...${NC}"
open "https://dashboard.render.com/create?type=web"

echo ""
echo -e "${GREEN}✅ GitHub repo is ready!${NC}"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🌐 NEXT STEPS IN RENDER DASHBOARD:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. Click 'Connect' next to GitHub (if needed)"
echo "2. Find 'telepathy-voice-ai' in the repo list"
echo "3. Click 'Connect'"
echo "4. Render auto-fills everything from render.yaml!"
echo "5. Scroll down and click 'Create Web Service'"
echo "6. Wait 5-10 minutes for deployment"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "After deployment completes, you'll get a URL like:"
echo "https://telepathy-api.onrender.com"
echo ""
echo "Then update frontend/index.html with that URL and run:"
echo "cd frontend && vercel --prod"
echo ""
echo -e "${GREEN}🎉 Your app will be fully live!${NC}"
echo ""
echo "Frontend: https://frontend-lp3etj38b-labdhi-mandovaras-projects.vercel.app"
echo "Backend: (will be live after Render deployment)"
echo ""

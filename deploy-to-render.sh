#!/bin/bash

# Telepathy - Automated Render Deployment Script
# This script will guide you through deploying to Render

set -e

echo "🚀 Telepathy - Render Deployment Helper"
echo "========================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if we're in a git repo
if [ ! -d .git ]; then
    echo -e "${RED}❌ Error: Not a git repository${NC}"
    echo "Please run this from the Telepathy project directory"
    exit 1
fi

# Check if render.yaml exists
if [ ! -f render.yaml ]; then
    echo -e "${RED}❌ Error: render.yaml not found${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Git repository found${NC}"
echo -e "${GREEN}✅ render.yaml configuration found${NC}"
echo ""

# Check git status
echo "📊 Checking git status..."
if [[ -n $(git status -s) ]]; then
    echo -e "${YELLOW}⚠️  You have uncommitted changes${NC}"
    echo ""
    git status -s
    echo ""
    read -p "Do you want to commit these changes? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "Enter commit message: " commit_msg
        git add .
        git commit -m "$commit_msg"
        echo -e "${GREEN}✅ Changes committed${NC}"
    fi
else
    echo -e "${GREEN}✅ No uncommitted changes${NC}"
fi

echo ""

# Check remote
echo "🔗 Checking git remote..."
if git remote -v | grep -q origin; then
    echo -e "${GREEN}✅ Git remote 'origin' found${NC}"
    git remote -v
else
    echo -e "${YELLOW}⚠️  No git remote found${NC}"
    echo "Setting up remote..."
    read -p "Enter your GitHub repository URL: " repo_url
    git remote add origin "$repo_url"
    echo -e "${GREEN}✅ Remote added${NC}"
fi

echo ""

# Push to GitHub
echo "📤 Pushing to GitHub..."
read -p "Push to GitHub? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    git push -u origin main || git push -u origin master
    echo -e "${GREEN}✅ Code pushed to GitHub${NC}"
else
    echo -e "${YELLOW}⚠️  Skipped push. You'll need to push manually.${NC}"
fi

echo ""
echo "🎯 Next Steps for Render Deployment:"
echo "===================================="
echo ""
echo "1. Go to: https://render.com"
echo "2. Sign in or create an account"
echo "3. Click 'New +' → 'Web Service'"
echo "4. Click 'Connect a repository'"
echo "5. Authorize GitHub and select your repository"
echo "6. Render will auto-detect render.yaml"
echo "7. Click 'Create Web Service'"
echo ""
echo "⏳ Build will take 5-10 minutes (training ML model)"
echo "🌐 Your API will be live at: https://telepathy-api.onrender.com"
echo ""
echo -e "${GREEN}✅ Setup complete!${NC}"
echo ""
echo "📖 For detailed instructions, see: DEPLOYMENT_INSTRUCTIONS.md"
echo ""

# Open Render website
read -p "Open Render website now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if [[ "$OSTYPE" == "darwin"* ]]; then
        open "https://render.com"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        xdg-open "https://render.com"
    else
        echo "Please open https://render.com in your browser"
    fi
fi

echo ""
echo "🎉 Good luck with your deployment!"

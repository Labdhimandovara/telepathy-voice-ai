#!/bin/bash
# Quick deployment script for Telepathy

echo "🚀 Telepathy Deployment Script"
echo "================================"
echo ""

# Check if GitHub repo exists
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "⚠️  No GitHub remote found."
    echo ""
    echo "📝 To deploy, you need to:"
    echo ""
    echo "1. Create GitHub repo manually:"
    echo "   - Go to: https://github.com/new"
    echo "   - Name: telepathy-voice-ai"
    echo "   - Description: AI-Powered Voice Emotion Recognition"
    echo "   - Make it PUBLIC"
    echo "   - Click 'Create repository'"
    echo ""
    echo "2. Then run these commands:"
    echo "   git remote add origin https://github.com/YOUR_USERNAME/telepathy-voice-ai.git"
    echo "   git push -u origin main"
    echo ""
    echo "3. Deploy to Render:"
    echo "   - Go to: https://render.com"
    echo "   - Click 'New +' → 'Web Service'"
    echo "   - Connect your GitHub repo"
    echo "   - Render will auto-detect settings"
    echo "   - Click 'Create Web Service'"
    echo ""
    echo "Your API will be live in ~5 minutes! 🎉"
    exit 0
fi

# If remote exists, push
echo "✅ GitHub remote found!"
echo "📤 Pushing to GitHub..."

git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo ""
    echo "🌐 Next: Deploy to Render"
    echo "   1. Go to: https://render.com"
    echo "   2. Click 'New +' → 'Web Service'"
    echo "   3. Select your GitHub repo"
    echo "   4. Click 'Create Web Service'"
    echo ""
    echo "Your API will be live at: https://telepathy-voice-ai.onrender.com"
else
    echo ""
    echo "❌ Push failed. Make sure:"
    echo "   - You have permission to push to the repo"
    echo "   - GitHub authentication is configured"
    echo "   - Run: gh auth login"
fi

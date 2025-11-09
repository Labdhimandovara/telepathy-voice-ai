#!/bin/bash

# Telepathy - Automated Vercel Deployment Script

set -e

echo "🚀 Telepathy - Vercel Deployment Helper"
echo "========================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if vercel.json exists
if [ ! -f vercel.json ]; then
    echo -e "${RED}❌ Error: vercel.json not found${NC}"
    exit 1
fi

echo -e "${GREEN}✅ vercel.json configuration found${NC}"
echo ""

# Warning about Vercel limitations
echo -e "${YELLOW}⚠️  IMPORTANT: Vercel Limitations for Python/FastAPI${NC}"
echo ""
echo "Vercel is NOT recommended for this application because:"
echo "  • 10-second function timeout (model training will fail)"
echo "  • Read-only file system (can't save trained models)"
echo "  • Limited Python package support"
echo ""
echo "👉 We recommend using Render instead (run ./deploy-to-render.sh)"
echo ""
read -p "Continue with Vercel anyway? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Deployment cancelled. Use Render for best results!"
    exit 0
fi

echo ""

# Check if models are trained locally
echo "🔍 Checking for trained models..."
if [ -f model_augmented.h5 ] && [ -f scaler.pkl ] && [ -f label_encoder.pkl ]; then
    echo -e "${GREEN}✅ Model files found${NC}"
else
    echo -e "${YELLOW}⚠️  Model files not found. Training locally...${NC}"
    echo ""
    
    # Install dependencies if needed
    if ! python3 -c "import tensorflow" 2>/dev/null; then
        echo "Installing dependencies..."
        pip3 install -r requirements.txt
    fi
    
    # Train model
    echo "Generating sample data..."
    python3 create_sample_data.py
    
    echo "Training model..."
    python3 train_simple.py
    
    echo -e "${GREEN}✅ Model trained${NC}"
fi

echo ""

# Check if Vercel CLI is installed
echo "🔍 Checking for Vercel CLI..."
if ! command -v vercel &> /dev/null; then
    echo -e "${YELLOW}⚠️  Vercel CLI not found${NC}"
    echo ""
    read -p "Install Vercel CLI? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Installing Vercel CLI..."
        npm install -g vercel
        echo -e "${GREEN}✅ Vercel CLI installed${NC}"
    else
        echo -e "${RED}❌ Cannot deploy without Vercel CLI${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✅ Vercel CLI found${NC}"
fi

echo ""

# Login to Vercel
echo "🔐 Logging in to Vercel..."
vercel login

echo ""

# Deploy
echo "🚀 Deploying to Vercel..."
echo ""
read -p "Deploy to production? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    vercel --prod
    echo -e "${GREEN}✅ Deployed to production${NC}"
else
    vercel
    echo -e "${GREEN}✅ Deployed to preview${NC}"
fi

echo ""
echo "🎉 Deployment complete!"
echo ""
echo "📖 Check your deployment at the URL shown above"
echo "📖 For more info, see: DEPLOYMENT_INSTRUCTIONS.md"
echo ""

# Note about limitations
echo -e "${YELLOW}⚠️  Remember: Vercel deployment has limitations${NC}"
echo "   • Model training won't work on serverless"
echo "   • Using pre-trained models from local build"
echo "   • For production, consider Render for the backend"
echo ""

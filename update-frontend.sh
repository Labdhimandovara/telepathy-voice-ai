#!/bin/bash
# Update frontend with backend URL and redeploy

if [ -z "$1" ]; then
    echo "Usage: ./update-frontend.sh <RENDER_URL>"
    echo ""
    echo "Example:"
    echo "  ./update-frontend.sh https://telepathy-api.onrender.com"
    echo ""
    exit 1
fi

BACKEND_URL=$1

echo "🔧 Updating frontend with backend URL..."
echo "Backend URL: $BACKEND_URL"

cd /Users/uditjainnnn/Telepathy/frontend

# Update the API URL in index.html
sed -i '' "s|const API_URL = 'API_URL_PLACEHOLDER';|const API_URL = '$BACKEND_URL';|g" index.html

echo "✅ Updated index.html"
echo ""
echo "🚀 Deploying to Vercel..."

vercel --prod --yes

echo ""
echo "✅ Frontend updated and deployed!"
echo ""
echo "Your app is now fully live! 🎉"
echo ""
echo "Frontend: https://frontend-lp3etj38b-labdhi-mandovaras-projects.vercel.app"
echo "Backend: $BACKEND_URL"

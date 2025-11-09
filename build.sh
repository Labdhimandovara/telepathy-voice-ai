#!/bin/bash
# Build script for Render

echo "🚀 Starting Telepathy deployment build..."

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Generate sample data
echo "🎵 Generating sample training data..."
python create_sample_data.py

# Train model
echo "🏋️ Training model..."
python train_simple.py

echo "✅ Build completed successfully!"

#!/usr/bin/env python3
"""
Deploy to Render using their API
"""
import json
import subprocess
import sys

print("🚀 Deploying Telepathy to Render via API...")
print("")

# Get Render API token from CLI config
try:
    result = subprocess.run(['render', 'whoami'], capture_output=True, text=True)
    if result.returncode != 0:
        print("❌ Not logged into Render. Run: render login")
        sys.exit(1)
    print("✅ Authenticated with Render")
except:
    print("❌ Render CLI not found or not authenticated")
    sys.exit(1)

print("")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("📋 RENDER BLUEPRINT DEPLOYMENT")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("")
print("The Render CLI doesn't support creating services directly.")
print("However, your render.yaml is ready!")
print("")
print("Please visit:")
print("https://dashboard.render.com/select-repo?type=blueprint")
print("")
print("Then:")
print("1. Select 'telepathy-voice-ai' repository")
print("2. Click 'Connect'")
print("3. Render will read render.yaml automatically")
print("4. Click 'Apply'")
print("")
print("Your API will be live in 5-10 minutes! 🎉")
print("")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

# Open the blueprint URL
subprocess.run(['open', 'https://dashboard.render.com/select-repo?type=blueprint'])
print("")
print("✅ Opening Render Blueprint deployment page...")


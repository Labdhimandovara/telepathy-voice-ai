"""
Telepathy - Real-time emotion prediction with demo mode
"""
import numpy as np
import sounddevice as sd
import librosa
import tensorflow as tf
import joblib
import sys
import os

# ------------------ Parameters ------------------
DURATION = 5          # seconds
SAMPLE_RATE = 22050*2 # Hz

# ------------------ Load model and preprocessors ------------------
print("🧠 Loading Telepathy AI model...")

if not os.path.exists("model_augmented.h5"):
    print("❌ Error: model_augmented.h5 not found!")
    print("Please run train_simple.py first to train the model.")
    sys.exit(1)

model = tf.keras.models.load_model("model_augmented.h5")
scaler = joblib.load("scaler.pkl")
label_encoder = joblib.load("label_encoder.pkl")

print("✅ Model loaded successfully!")
print(f"📊 Emotions detected: {list(label_encoder.classes_)}")

# ------------------ Helper Functions ------------------
def extract_features(audio, sr):
    """Extract audio features"""
    mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=40)
    stft = np.abs(librosa.stft(audio))
    chroma = librosa.feature.chroma_stft(S=stft, sr=sr)
    spec_contrast = librosa.feature.spectral_contrast(S=stft, sr=sr)
    tonnetz = librosa.feature.tonnetz(y=librosa.effects.harmonic(audio), sr=sr)
    
    features = np.vstack([mfccs, chroma, spec_contrast, tonnetz]).T
    return features

def predict_emotion(audio):
    """Predict emotion from audio"""
    # Extract features
    features = extract_features(audio, SAMPLE_RATE)
    
    # Pad or truncate to match training time_steps
    time_steps = model.input_shape[1]
    if features.shape[0] < time_steps:
        features = np.pad(features, ((0, time_steps - features.shape[0]), (0,0)), mode='constant')
    elif features.shape[0] > time_steps:
        features = features[:time_steps, :]
    
    # Scale features
    features_2d = features.reshape(1, -1)
    features_scaled_2d = scaler.transform(features_2d)
    features_scaled = features_scaled_2d.reshape(1, time_steps, features.shape[1])
    
    # Make prediction
    pred_probs = model.predict(features_scaled, verbose=0)
    pred_index = np.argmax(pred_probs)
    pred_label = label_encoder.inverse_transform([pred_index])[0]
    confidence = pred_probs[0][pred_index] * 100
    
    return pred_label, confidence, pred_probs[0]

# ------------------ Demo Mode ------------------
def demo_mode():
    """Test with sample audio files"""
    print("\n🎭 Demo Mode - Testing with sample audio files...")
    
    if not os.path.exists("sample_data"):
        print("❌ Sample data not found!")
        return
    
    emotions = os.listdir("sample_data")
    emotions = [e for e in emotions if os.path.isdir(os.path.join("sample_data", e))]
    
    for emotion in emotions:
        emotion_dir = os.path.join("sample_data", emotion)
        files = [f for f in os.listdir(emotion_dir) if f.endswith('.wav')]
        
        if files:
            # Test first file
            test_file = os.path.join(emotion_dir, files[0])
            audio, sr = librosa.load(test_file, sr=SAMPLE_RATE, duration=DURATION)
            
            pred_emotion, confidence, probs = predict_emotion(audio)
            
            print(f"\n  📂 File: {emotion}/{files[0]}")
            print(f"  🎯 Actual: {emotion}")
            print(f"  🤖 Predicted: {pred_emotion} ({confidence:.2f}% confidence)")
            
            if pred_emotion == emotion:
                print("  ✅ CORRECT!")
            else:
                print("  ❌ INCORRECT")

# ------------------ Live Recording Mode ------------------
def live_mode():
    """Record and predict from microphone"""
    print("\n🎤 Live Recording Mode")
    print(f"⏱️  Recording for {DURATION} seconds...")
    print("💬 Speak now with emotion!")
    
    audio = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1)
    sd.wait()
    print("✅ Recording finished!")
    
    # Convert to 1D array
    audio = audio.flatten()
    
    # Predict
    pred_emotion, confidence, probs = predict_emotion(audio)
    
    print(f"\n{'='*50}")
    print(f"🎯 PREDICTED EMOTION: {pred_emotion.upper()}")
    print(f"💯 Confidence: {confidence:.2f}%")
    print(f"{'='*50}")
    
    print("\n📊 Probability Distribution:")
    for emotion, prob in zip(label_encoder.classes_, probs):
        bar_length = int(prob * 50)
        bar = '█' * bar_length + '░' * (50 - bar_length)
        print(f"  {emotion:10s} [{bar}] {prob*100:5.2f}%")

# ------------------ Main Menu ------------------
def main():
    print("\n" + "="*50)
    print("🧠 TELEPATHY - Voice Emotion Recognition")
    print("="*50)
    
    while True:
        print("\n📋 Select Mode:")
        print("  1. 🎤 Live Recording (Record from microphone)")
        print("  2. 🎭 Demo Mode (Test with sample files)")
        print("  3. 🚪 Exit")
        
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == '1':
            try:
                live_mode()
            except Exception as e:
                print(f"❌ Error in live mode: {e}")
                print("💡 Make sure your microphone is connected and accessible")
        
        elif choice == '2':
            demo_mode()
        
        elif choice == '3':
            print("\n👋 Thank you for using Telepathy!")
            break
        
        else:
            print("⚠️  Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()

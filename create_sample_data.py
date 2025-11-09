"""
Create sample audio data for testing Telepathy without large datasets
Generates synthetic emotional speech patterns
"""
import numpy as np
import librosa
import soundfile as sf
import os

def generate_emotional_audio(emotion, duration=5, sr=44100):
    """
    Generate synthetic audio with characteristics of different emotions
    """
    t = np.linspace(0, duration, int(sr * duration))
    
    # Base frequency patterns for emotions
    emotion_params = {
        'neutral': {'freq': 200, 'variation': 10, 'noise': 0.05},
        'happy': {'freq': 300, 'variation': 50, 'noise': 0.1},
        'sad': {'freq': 150, 'variation': 5, 'noise': 0.03},
        'angry': {'freq': 250, 'variation': 80, 'noise': 0.15},
        'fearful': {'freq': 350, 'variation': 100, 'noise': 0.12}
    }
    
    params = emotion_params[emotion]
    
    # Generate base signal with emotion characteristics
    signal = np.zeros_like(t)
    
    # Add multiple harmonics with emotional variations
    for i in range(1, 6):
        freq = params['freq'] * i
        variation = params['variation'] * np.sin(2 * np.pi * 0.5 * t)
        signal += np.sin(2 * np.pi * (freq + variation) * t) / i
    
    # Add noise based on emotion
    noise = np.random.normal(0, params['noise'], len(t))
    signal += noise
    
    # Normalize
    signal = signal / np.max(np.abs(signal)) * 0.8
    
    return signal

# Create sample data directory
os.makedirs('sample_data', exist_ok=True)

emotions = ['neutral', 'happy', 'sad', 'angry', 'fearful']
samples_per_emotion = 20

print("Generating sample emotional audio data...")

for emotion in emotions:
    emotion_dir = os.path.join('sample_data', emotion)
    os.makedirs(emotion_dir, exist_ok=True)
    
    for i in range(samples_per_emotion):
        audio = generate_emotional_audio(emotion)
        filename = os.path.join(emotion_dir, f'{emotion}_{i:02d}.wav')
        sf.write(filename, audio, 44100)
    
    print(f"Created {samples_per_emotion} samples for {emotion}")

print(f"\nTotal samples created: {len(emotions) * samples_per_emotion}")
print("Sample data saved in: ./sample_data/")

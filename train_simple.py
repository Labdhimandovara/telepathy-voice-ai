"""
Simplified training script for Telepathy using local sample data
"""
import os
import numpy as np
import librosa
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
import joblib

# ==============================
# CONFIG
# ==============================
DATA_PATH = "sample_data"
DURATION = 5
SAMPLE_RATE = 22050 * 2
N_MFCC = 40

EMOTIONS = ["neutral", "happy", "sad", "angry", "fearful"]

features = []
labels = []

print("🚀 Starting Telepathy training...")
print(f"📂 Data path: {DATA_PATH}")

# ==============================
# FEATURE EXTRACTION FUNCTION
# ==============================
def extract_features(file_path, sample_rate):
    """Extract audio features from file"""
    X, sr = librosa.load(file_path, res_type='kaiser_fast', 
                         duration=DURATION, sr=sample_rate, mono=True)
    
    # MFCC
    mfccs = librosa.feature.mfcc(y=X, sr=sr, n_mfcc=N_MFCC)
    # Chroma
    stft = np.abs(librosa.stft(X))
    chroma = librosa.feature.chroma_stft(S=stft, sr=sr)
    # Spectral Contrast
    spec_contrast = librosa.feature.spectral_contrast(S=stft, sr=sr)
    # Tonnetz
    tonnetz = librosa.feature.tonnetz(y=librosa.effects.harmonic(X), sr=sr)
    
    # Combine all features
    combined = np.vstack([mfccs, chroma, spec_contrast, tonnetz]).T
    return combined

# ==============================
# FEATURE EXTRACTION FROM SAMPLE DATA
# ==============================
print("\n📊 Extracting features from audio files...")

for emotion in EMOTIONS:
    emotion_folder = os.path.join(DATA_PATH, emotion)
    if not os.path.exists(emotion_folder):
        print(f"⚠️  Warning: {emotion_folder} not found, skipping...")
        continue
    
    file_count = 0
    for file in os.listdir(emotion_folder):
        if not file.endswith(".wav"):
            continue
        
        file_path = os.path.join(emotion_folder, file)
        try:
            feats = extract_features(file_path, SAMPLE_RATE)
            features.append(feats)
            labels.append(emotion)
            file_count += 1
        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")
    
    print(f"  ✓ {emotion}: {file_count} files processed")

if len(features) == 0:
    raise ValueError("❌ No valid audio files found! Please run create_sample_data.py first.")

print(f"\n✅ Total samples processed: {len(features)}")

# ==============================
# PREPROCESSING
# ==============================
print("\n🔧 Preprocessing data...")

# Pad features to same length
max_len = max([f.shape[0] for f in features])
features_padded = np.array([np.pad(f, ((0, max_len - f.shape[0]), (0,0)), 
                                   mode='constant') for f in features])

X = features_padded
y = np.array(labels)

# Encode labels
le = LabelEncoder()
y_encoded = le.fit_transform(y)
y_categorical = to_categorical(y_encoded)

# Split train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y_categorical, test_size=0.2, random_state=42, stratify=y_encoded
)

print(f"  Training samples: {len(X_train)}")
print(f"  Testing samples: {len(X_test)}")

# Scale features
num_samples_train, time_steps, num_features = X_train.shape
X_train_2d = X_train.reshape(num_samples_train, time_steps * num_features)

scaler = StandardScaler()
X_train_scaled_2d = scaler.fit_transform(X_train_2d)
X_train_scaled = X_train_scaled_2d.reshape(num_samples_train, time_steps, num_features)

# Scale test data
num_samples_test = X_test.shape[0]
X_test_2d = X_test.reshape(num_samples_test, time_steps * num_features)
X_test_scaled_2d = scaler.transform(X_test_2d)
X_test_scaled = X_test_scaled_2d.reshape(num_samples_test, time_steps, num_features)

# Save scaler & label encoder
joblib.dump(scaler, "scaler.pkl")
joblib.dump(le, "label_encoder.pkl")
print("  ✓ Saved scaler and label encoder")

# ==============================
# LSTM MODEL
# ==============================
print("\n🧠 Building LSTM model...")

model = Sequential([
    LSTM(128, input_shape=(X_train_scaled.shape[1], X_train_scaled.shape[2]), 
         return_sequences=True),
    Dropout(0.3),
    LSTM(64),
    Dropout(0.3),
    Dense(y_categorical.shape[1], activation='softmax')
])

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

print(model.summary())

# ==============================
# TRAIN
# ==============================
print("\n🏋️  Training model...")

checkpoint = ModelCheckpoint("model_augmented.h5", monitor='val_accuracy', 
                            save_best_only=True, verbose=1)
early_stop = EarlyStopping(monitor='val_loss', patience=10, verbose=1)

history = model.fit(
    X_train_scaled, y_train, 
    validation_data=(X_test_scaled, y_test),
    epochs=50, 
    batch_size=16, 
    callbacks=[checkpoint, early_stop],
    verbose=1
)

# ==============================
# EVALUATE
# ==============================
print("\n📈 Evaluating model...")

loss, accuracy = model.evaluate(X_test_scaled, y_test, verbose=0)
print(f"  Test Loss: {loss:.4f}")
print(f"  Test Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")

print("\n✨ Training completed successfully!")
print("📁 Generated files:")
print("  - model_augmented.h5")
print("  - scaler.pkl")
print("  - label_encoder.pkl")
print("\n🎯 Ready to run predictions with predict_voice.py")

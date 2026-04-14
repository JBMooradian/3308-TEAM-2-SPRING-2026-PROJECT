import librosa
import numpy as np
import os

REF_ROOT = "data/reference"
SPEC_ROOT = "data/spectrograms"

# adapted from Peyton's LOAD FILES functions. Loops through all reference data
def build_spectrogram_dataset():
    for root, _, files in os.walk(REF_ROOT):
        for f in files:
            if not f.lower().endswith((".mp3", ".m4a")):
                continue
            audio_path = os.path.join(root, f)
            generate_mel_spectrogram(audio_path)
            save_spectrogram(audio_path)

# adapted from Bri's model. It now normalizes the specs and then saves them to a new dir called "spectrograms"
def generate_mel_spectrogram(audio_path):

    # Load the audio file
    y, sr = librosa.load(audio_path, sr=None)

    # Extract the Mel-spectrogram
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)

    # Convert power to decibels (log scale)
    S_db = librosa.power_to_db(S, ref=np.max)

    # Normalize during processing
    return normalize(S_db)

# saves the numpy arrays to the new directory 
def save_spectrogram(audio_path):

    spec = generate_mel_spectrogram(audio_path)
    
    rel_path = os.path.relpath(audio_path, REF_ROOT)
    rel_path_npy = os.path.splitext(rel_path)[0] + ".npy"
    output_path = os.path.join(SPEC_ROOT, rel_path_npy)

    # Check for existing directory
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Save np array
    np.save(output_path, spec)
    print(f"[SAVED] {output_path}") # <--used when creating the original directory


# pulled from Peyton's similarity_ranker
def normalize(spec):
    min_val, max_val = spec.min(), spec.max()
    if max_val == min_val:
        return np.zeros_like(spec)
    return (spec - min_val) / (max_val - min_val)
    

if __name__ == "__main__":
    build_spectrogram_dataset()


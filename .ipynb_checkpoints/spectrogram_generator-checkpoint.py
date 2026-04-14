"""
Bird Call Spectogram Generator
Sprint 1: Bri Martinez

Pipeline:
    [Dataset (Jake)] > [THIS MODULE] > [Similarity Model (Peyton)] > [UI (Stephen)]

What this does:
    Librosa Implementation: The generate_mel_spectrogram function takes a raw file and outputs a normalized 2D NumPy array, which is what Peyton's compare_to_references function requires.

    Matplotlib Implementation: The plot_spectrogram function provides the visual output requested for the MVP, allowing users to "see" the bird call in the UI that Stephen outlined.

    Team Integration: By standardizing on n_mels=128, we ensure that the "shapes" of our spectrograms are consistent before they hit the resizing logic in the similarity model.

Dependencies:
    librosa
    matplot
    numpy
"""

import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

def generate_mel_spectrogram(audio_path):
    """
    Converts an audio file into a Mel-spectrogram array for similarity ranking.
    This fulfills the 'Build librosa prototype' task for Sprint 1.
    """
    
    # 1. Load the audio file
    # 'sr=None' preserves the native sampling rate for better quality
    y, sr = librosa.load(audio_path, sr=None)

    # 2. Extract the Mel-spectrogram
    # We use 128 'mels' (frequency bins) to match common ML standards
    # n_fft is the window size; hop_length is the spacing between frames
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)

    # 3. Convert power to decibels (log scale)
    # This makes the data more 'image-like' and easier for the model to process
    S_db = librosa.power_to_db(S, ref=np.max)

    return S_db

def plot_spectrogram(S_db, save_path="spectrogram.png", bird_name="Unknown Bird"):
    """
    Creates a visual representation of the audio signal.
    This fulfills the 'Build matplotlib prototype' task for Sprint 1.
    """
    plt.figure(figsize=(10, 4))
    
    # Display the spectrogram with a 'magma' color map for high contrast
    librosa.display.specshow(S_db, x_axis='time', y_axis='mel', fmax=8000)
    
    plt.colorbar(format='%+2.0f dB')
    plt.title(f'Mel-Spectrogram: {bird_name}')
    plt.tight_layout()
    
    # EDIT: save to passed path when called by app.py
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

# --- INTEGRATION EXAMPLE ---
# This mirrors how the pipeline will flow from the module to Peyton's ranker.
if __name__ == "__main__":
    # Example path (to be provided by Jake's dataset)
    test_file = "cardinal_sample.mp3" 
    
    try:
        # Generate the 2D array (The 'Transformation' step)
        spectrogram_data = generate_mel_spectrogram(test_file)
        print(f"Spectrogram generated with shape: {spectrogram_data.shape}")

        # Visualize it (The 'Matplotlib' step)
        plot_spectrogram(spectrogram_data, "Northern Cardinal")
        
        # NOTE FOR TEAM: Pass 'spectrogram_data' to Peyton's 
        # compare_to_references(input_spectrogram, reference_spectrograms)
        
    except Exception as e:
        print(f"Error processing audio: {e}")
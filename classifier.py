import numpy as np
import os
from dataset_builder import generate_mel_spectrogram # <- combo of Bri's spectrogram and normalizing
from nn import NeuralNetwork

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

MODEL_PATH = "data/model/bird_nn.npy"
LABELS_PATH = "data/model/labels.npy"
TARGET_COLS = 32

TESTS_PATH = "data/test"

# repeated from nn_trainer. Pads misaligned arrays, rather than cropping to match before flatten
def flatten_spec(spec, target_cols=TARGET_COLS):
    rows, cols = spec.shape
    if cols >= target_cols:
        spec = spec[:, :target_cols]
    else:
        pad = np.zeros((rows, target_cols - cols))
        spec = np.hstack([spec, pad])
    return spec.flatten()
    
# from pretrained bird_nn and labels numpy arrays found in 'model' directory
def load_model():
    labels = list(np.load(LABELS_PATH, allow_pickle=True))
    weights = np.load(MODEL_PATH, allow_pickle=True)
    input_dim = weights[0].shape[0] - 1  # removes bias node used in nn
    n_classes = weights[-1].shape[1]
    nn = NeuralNetwork.load(MODEL_PATH, [input_dim, 64, n_classes])
    return nn, labels

# refactored from the cross-correlation function in ranker. This just uses nn.predict
# instead of scipy.signal.correlate
def identify_bird(audio_path):
    spec = generate_mel_spectrogram(audio_path)
    vec = flatten_spec(spec)
    nn, labels = load_model()

    probs = nn.predict(np.atleast_2d(vec))[0] # call predict module form nn. Shape: (n_classes,)
    ranked = sorted(enumerate(probs), key=lambda x: x[1], reverse=True)

    return [
        {"rank": i+1, "bird": labels[idx], "score": round(float(prob), 4)}
        for i, (idx, prob) in enumerate(ranked)
    ]

def test_all_birds():
    for root, _, files in os.walk(TESTS_PATH):
        for f in files:
            if not f.lower().endswith((".mp3", ".m4a")):
                continue
            audio_path = os.path.join(root, f)
            expected_bird = os.path.basename(root)
            results = identify_bird(audio_path)
            top_match = results[0]["bird"]
            correct = "CORRECT" if top_match == expected_bird else "INCORRECT"
            print(f"\nExpected: {expected_bird} Top match: {top_match} (confidence: {results[0]['score']}) [{correct}]\n")
            for r in results:
                print(f"  #{r['rank']}  {r['bird']:<30} {r['score']}")
            

if __name__ == "__main__":
    test_all_birds()

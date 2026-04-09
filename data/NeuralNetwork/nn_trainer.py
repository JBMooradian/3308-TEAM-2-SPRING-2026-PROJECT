import numpy as np
import os
from nn import NeuralNetwork

SPEC_ROOT = "data/spectrograms"
MODEL_OUT = "data/model/bird_nn.npy"
LABELS_OUT = "data/model/labels.npy"
TARGET_COLS = 128

def flatten_spec(spec, target_cols=TARGET_COLS):
    rows, cols = spec.shape
    if cols >= target_cols:
        spec = spec[:, :target_cols]
    else:
        pad = np.zeros((rows, target_cols - cols))
        spec = np.hstack([spec, pad])
    return spec.flatten()

def load_training_data():
    X = [] # Array of flattened specs
    y_raw = [] # vertical (mel-bins) Will be one-hot encoded to create bird signatures, thus "raw"
    label_names = [] # array of spec ids

    # same logic as get_reference_files() from the ranker
    for bird in sorted(os.listdir(SPEC_ROOT)):
        path = os.path.join(SPEC_ROOT, bird)
        if not os.path.isdir(path):
            continue
        label_names.append(bird)
        label_idx = len(label_names) - 1

        for f in os.listdir(path):
            if f.endswith(".npy"):
                spec = np.load(os.path.join(path, f))
                X.append(flatten_spec(spec))
                y_raw.append(label_idx)

    X = np.array(X) # Standardize shape
    n_classes = len(label_names) # number of different bird types

    # one-hot encode specs
    y = np.zeros((len(y_raw), n_classes))
    for i, label in enumerate(y_raw):
        y[i, label] = 1.0

    return X, y, label_names

# pass loaded data into the nn.fit() class function, let backprop do its thing
def train_and_save():
    X, y, label_names = load_training_data()
    n_classes = len(label_names)
    input_dim = X.shape[1]

    print(f"[TRAIN] {X.shape[0]} samples, {n_classes} classes, input dim {input_dim}")

    # Assert layer sizes: input -> hidden layers -> output
    nn = NeuralNetwork([input_dim, 64, n_classes], alpha=0.01)
    nn.fit(X, y, epochs=500, displayUpdate=50)

    # Save the weights and their labels in the "model" directory
    os.makedirs("data/model", exist_ok=True)
    np.save(MODEL_OUT, np.array(nn.W, dtype=object), allow_pickle=True)
    np.save(LABELS_OUT, np.array(label_names))
    print(f"[SAVED] Model -> {MODEL_OUT}")
    print(f"[SAVED] Labels -> {LABELS_OUT}")

if __name__ == "__main__":
    train_and_save()

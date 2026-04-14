import numpy as np
import os
from nn import NeuralNetwork

SPEC_ROOT = "data/spectrograms"
MODEL_OUT = "data/model/bird_nn.npy"
LABELS_OUT = "data/model/labels.npy"
TARGET_COLS = 32

def flatten_spec(spec, target_cols=TARGET_COLS):
    rows, cols = spec.shape
    if cols >= target_cols:
        spec = spec[:, :target_cols]
    else:
        pad = np.zeros((rows, target_cols - cols))
        spec = np.hstack([spec, pad])
    return spec.flatten()

def load_training_data():
    # Array of flattened specs
    X = [] 
    # vertical (mel-bins) Will be one-hot encoded to create bird signatures, thus "raw"
    y_raw = [] 
    # Sort label names for persistent order if using correlation scores & assert checkpoint ignore
    label_names = [bird for bird in sorted(os.listdir(SPEC_ROOT))
                   if bird != ".ipynb_checkpoints" and
                   os.path.isdir(os.path.join(SPEC_ROOT, bird))]
    
    # Similar logic as get_reference_files() from the ranker
    for bird in label_names:
        path = os.path.join(SPEC_ROOT, bird)
        label_idx = label_names.index(bird)
        for file in os.listdir(path):
            if file.endswith(".npy"):
                spec = np.load(os.path.join(path, file))
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
    # limiting hidden layers to 8 shrinks model size/processing. 6 classes is not very big
    nn = NeuralNetwork([input_dim, 18, n_classes], alpha=0.01)
    nn.fit(X, y, epochs=3500, displayUpdate=100)

    # Save the weights and their labels in the "model" directory
    os.makedirs("data/model", exist_ok=True)
    np.save(MODEL_OUT, np.array(nn.W, dtype=object), allow_pickle=True) 
    np.save(LABELS_OUT, np.array(label_names))
    print(f"[SAVED] Model -> {MODEL_OUT}")
    print(f"[SAVED] Labels -> {LABELS_OUT}")


if __name__ == "__main__":
    train_and_save()


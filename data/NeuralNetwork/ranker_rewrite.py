# reworking of Peyton's original similarity_ranker to work with a prebuilt dataset
# minor changes include relocation of normalize function into dataset_builder,
# and ensuring that only one mel spec is generated from the user input and only stored in memory

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # adds project root to path so all modules are found

import numpy as np
from scipy.signal import correlate
from dataset_builder import generate_mel_spectrogram, normalize # <- this is a hybrid of Bri's generator and Peyton's normalizer

# PATHS

REFERENCE_DIR     = "data/spectrograms"  # Changed dir to new spectrogram dataset
TEST_DIR          = "data/test"         


# LOAD FILES

# Change: load from pre-processed numpy arrays; renamed variables to emphasize
def get_reference_specs(): 
    """Load cached spectrograms from secondary directory build by dataset_builder."""
    files = {}
    
    for bird in sorted(os.listdir(REFERENCE_DIR)):                              
        path = os.path.join(REFERENCE_DIR, bird)
        
        if not os.path.isdir(path):                                             
            continue
               
        specs = [os.path.join(path, f) for f in sorted(os.listdir(path))
                 if f.endswith(".npy") ] 
        
        if specs:
            files[bird] = specs
            
    return files


def get_test_files():
    """Scan data/test/ and return one test file per bird."""
    files = {}
    
    for bird in sorted(os.listdir(TEST_DIR)):                                   
        path = os.path.join(TEST_DIR, bird)
        
        if not os.path.isdir(path):                                             
            continue
            
        audio = [os.path.join(path, f) for f in sorted(os.listdir(path))
                 if f.endswith(".mp3") or f.endswith(".wav")]
        if audio:
            files[bird] = audio[0]                                              
    return files


# COMPARISON

def crop_to_match(a, b):
    """Crop both spectrograms to the same shape before comparing."""
    rows = min(a.shape[0], b.shape[0])
    cols = min(a.shape[1], b.shape[1])
    return a[:rows, :cols], b[:rows, :cols]

# CHANGE: normalize happens in new hybrid program
def score(input_spec, reference_spec):
    """Return a similarity score between two spectrograms using cross correlation."""
    a, b = crop_to_match(input_spec, reference_spec)
    correlation = correlate(a.flatten(), b.flatten(), mode = "valid")           # slide signals over each other and measure overlap
    return float(np.max(correlation))                                           # peak overlap is the similarity score


def rank_birds(input_spec, reference_files):
    """Score input against all reference birds and return ranked results."""
    scores = {}
    for bird, ref_paths in reference_files.items():
        
        bird_scores = []

        for path in ref_paths:
            reference_spec = np.load(path) # <- new fast load
            bird_scores.append(score(input_spec, reference_spec))
            
        scores[bird] = sum(bird_scores) / len(bird_scores)

    ranked = sorted(scores.items(), key = lambda x: x[1], reverse = True)      # sort highest score first
    return [{"rank": i + 1, "bird": bird, "score": round(s, 4)} for i, (bird, s) in enumerate(ranked)]


def compare_to_references(input_spectrogram, reference_files):
    """Main entry point for Stephen's UI."""
    if not isinstance(input_spectrogram, np.ndarray):
        raise TypeError("input_spectrogram must be a numpy array")
    if input_spectrogram.ndim != 2:
        raise ValueError(f"Expected 2D array, got shape {input_spectrogram.shape}")
    if len(reference_files) == 0:
        raise ValueError("reference_files is empty")
    return rank_birds(input_spectrogram, reference_files)


# RUN

if __name__ == "__main__":
    reference_specs = get_reference_specs()                                    
    test_files      = get_test_files()                                          

    print(f"\n[PIPELINE] Testing {len(test_files)} birds against {len(reference_specs)} references\n")

    for test_bird, test_path in test_files.items():                             # loop through every test bird
        test_spec = generate_mel_spectrogram(test_path)                         # convert test audio to spectrogram
        results   = compare_to_references(test_spec, reference_specs)           # rank against all references
        top_match = results[0]["bird"]
        correct   = "CORRECT" if top_match == test_bird else "WRONG"

        print(f"  Tested: {test_bird:<30} Top match: {top_match:<30} [{correct}]")
        for entry in results:
            print(f"    #{entry['rank']}  {entry['bird']:<30} score: {entry['score']}")
        print()
"""
Bird Call Identifier - UI
Sprint 2: Stephen

Pipeline:
    [Dataset (Jake)] > [Spectrograms (Brie)] > [Ranker (Peyton)] > [THIS MODULE]
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # adds project root to path

from flask import Flask, render_template, request                                # Flask handles routing and rendering
from spectrogram.spectrogram_generator import generate_mel_spectrogram           # Brie's function
from similarity_model.similarity_ranker import compare_to_references, get_reference_files  # Peyton's functions

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'ui/static/uploads'                               # where uploaded audio files are saved
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok = True)                       # create the folder if it doesn't exist

reference_files = get_reference_files()                                         # load reference birds once when app starts,
                                                                                # no need to reload on every request


@app.route('/')
def index():
    """Serve the upload page."""
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Accept uploaded audio file, run it through the pipeline, return ranked results.
    Called when user submits the form on index.html.
    """

    if 'audio_file' not in request.files:                                       # check that the form included a file
        return "No file uploaded", 400

    file = request.files['audio_file']                                          # get the uploaded file from the form

    if file.filename == '':                                                     # check that the user actually selected a file
        return "No file selected", 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)        # build the path to save the file
    file.save(filepath)                                                         # save the uploaded file to disk

    spec = generate_mel_spectrogram(filepath)                                   # Brie's function converts audio to spectrogram array

    results = compare_to_references(spec, reference_files)                      # Peyton's function ranks against all reference birds

    return render_template('results.html', results = results, filename = file.filename) # pass results to results page


if __name__ == '__main__':
    app.run(debug = True)                                                       # debug=True auto reloads on file changes during development

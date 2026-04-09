from flask import Flask, render_template, request, redirect, url_for
import os

from spectrogram.spectrogram_generator import plot_spectrogram, generate_mel_spectrogram
from ranker.ranker import compare_to_references, generate_mock_spectrogram, reference_specs

app = Flask(__name__)
# Configure uploads folder:
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# 1) Landing Page
@app.route('/')
def landing():
    return render_template('landing.html')

# 2) Upload Page
@app.route('/upload')
def upload_page():
    return render_template('upload.html')

# 3) Analyze 
@app.route('/analyze', methods=['POST'])
def analyze():
    
    # When user submits the form, Flask creates dictionary called request.files
    # Each <input type="file" name="..."> becomes a key in request.files
    if 'audio_file' not in request.files:
        return "No file uploaded", 400
        
    file = request.files['audio_file']
    if file.filename == '':
        return "No selected file", 400

    # Save uploaded file
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    # ("static/uploads", "raven_call.mp3") -> "static/uploads/raven_call.mp3"
    file.save(filepath)

    # Generate spectrogram from uploaded audio
    spec = generate_mel_spectrogram(filepath)

    # Save spectrogram image
    bird_name = "uploaded_call"
    plot_spectrogram(spec, bird_name)

    # TODO: Pass reference_specs ***
    # Added: from ranker.ranker import reference_specs
    results = compare_to_references(spec, reference_specs)

    return render_template(
        'results.html',
        # *** needs plot_spectogram to save file to static/uploads/
        spectrogram_image=f"uploads/{bird_name}_spectrogram.png",
        results=results
    )

# 4) Bird Details Page
@app.route('/bird/<bird_name>')
def bird_details(bird_name):
    # TODO: Replace with SQL lookup ***
    bird_data = {
        "name": bird_name,
        "description": "Placeholder description.",
        "image": f"birds/{bird_name}.png",
        "audio": f"birds/{bird_name}.mp3",
        "reference_spec": f"birds/{bird_name}_spectrogram.png"
    }

    return render_template('bird_details.html', bird=bird_data)
    
# 5) About Page
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
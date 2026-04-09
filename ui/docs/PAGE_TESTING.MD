# PAGE_TESTING.md

This document describes five pages we will implement for the Cawler ID application.  
Each page includes:

- Page Title  
- Page Description  
- Parameters needed  
- Data needed  
- Link destinations  
- Rendering tests  

---

# 1) Landing Page

## Page Title
Landing Page (Welcome)

## Page Description
Purpose: Introduce **Cawler ID**, explain the purpose of the app, and direct users to upload a bird call.
This page acts as the main entry point and provides a simple overview of how the system works.

## Parameters Needed
None.

## Data Needed to Render
- App name  
- Tagline  
- Static text for “How It Works”  
- Navigation links  

## Link Destinations
- '/upload'  
- '/about'  

## Tests for Verifying Rendering
1. Page loads with title “Cawler ID”.  
2. “Upload a Bird Call” button is visible and links to '/upload'.  
3. “How It Works” section renders correctly.  
4. Navigation links appear and route correctly.  
5. Page renders without requiring parameters.

---

# 2) Upload Page

## Page Title
Upload Bird Call

## Page Description
Purpose: Allow users to upload an audio file (MP3/WAV) for analysis.  
This page contains the file upload form that posts to '/analyze'.

## Parameters Needed
None.

## Data Needed to Render
- Static form fields  
- Supported formats text  

## Link Destinations
- POST '/analyze'  
- GET '/' (back to landing)

## Tests for Verifying Rendering
1. File input renders with 'name="audio_file"'.  
2. Form uses 'enctype="multipart/form-data"'.  
3. Submit button labeled “Analyze Bird Call” is visible.  
4. Uploading no file triggers validation error.  
5. Uploading a valid file redirects to '/results'.
6. Uploading an invalid file type results in error page.

---

# 3) Results Page

## Page Title
Analysis Results

## Page Description
Purpose: Display the generated spectrogram and ranked similarity results from the audio analysis.

## Parameters Needed
- 'spectrogram_image' (string path)  
- 'results' (list of ranked entries)

Each entry includes:
- 'rank'  
- 'bird'  
- 'score'

## Data Needed to Render
- Path to saved spectrogram image  
- Ranked similarity results  
- Bird names for linking to detail pages  

## Link Destinations
- '/bird/<bird_name>'  
- '/upload'

## Tests for Verifying Rendering
1. Spectrogram image loads via 'url_for('static', ...)'.  
2. Results list renders all entries in order.  
3. Each bird name links to '/bird/<name>'.  
4. Missing or empty results show a fallback message.  
5. Page renders without JavaScript errors.

---

# 4) Bird Details Page

## Page Title
Bird Details — '<bird_name>'

## Page Description
Purpose: Provide species‑specific information, including example audio, description, and reference spectrogram.  
This page acts as a mini field‑guide entry for each bird species.

## Parameters Needed
- 'bird_name' (URL parameter)

## Data Needed to Render
From a bird database in SQL:
- Bird name  
- Description  
- Image path  
- Example audio path  
- Reference spectrogram path  

## Link Destinations
- '/results'  
- '/upload'

## Tests for Verifying Rendering
1. Page loads correct bird information from URL.  
2. Bird image renders correctly.  
3. Audio playback element appears.  
4. Reference spectrogram loads.  


---

# 5) About Page

## Page Title
About Cawler ID

## Page Description
Purpose: Explain what the app does, how spectrograms work, and the motivation behind the project.  
This page provides context and background for users who want to understand the system.

## Parameters Needed
None.

## Data Needed to Render
- Static text content  
- Optional images or diagrams  

## Link Destinations
- '/'  
- '/upload'

## Tests for Verifying Rendering
1. Page loads with correct title.  
2. All sections (What, How, Motivation) appear.  
3. Navigation links work.  
4. Page renders without requiring parameters.  
5. No missing assets (images, icons).

---

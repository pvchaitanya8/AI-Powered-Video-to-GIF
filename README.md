# Video to GIF Generator

This project is a Streamlit web application that allows users to generate GIFs from videos with text overlays corresponding to spoken words in the video. The approach involves transcribing the video, identifying GIF-worthy fragments, and creating GIFs with text overlays.

## Features

- Upload video files and generate GIFs with captions.
- Transcribe video audio to text.
- Identify sentences suitable for GIF captions using a language model.
- Extract specific video segments corresponding to identified captions.
- Add text overlays to video clips.
- Convert video clips to GIFs.
- Download all generated GIFs as a zip file.

## Prerequisites

- Python 3.8 or higher
- Required Python packages (listed in `requirements.txt`)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-repository/video-to-gif-generator.git
cd video-to-gif-generator
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage
1. Update your GROQ_API_KEY with your API Key

2. Run the Streamlit application:

```bash
streamlit run app.py
```

2. Open the Streamlit app in your web browser. The default URL is `http://localhost:8501`.

3. Upload a video file using the file uploader.

4. Configure the caption settings in the sidebar (font style, scale, color, thickness).

5. Generate GIFs by clicking the "Generate GIFs" button.

6. Download the generated GIFs as a zip file.

## Project Structure

- `app.py`: Main application file containing the Streamlit UI and backend logic.
- `requirements.txt`: List of required Python packages.
- `README.md`: This readme file.
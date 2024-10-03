# AI Powered GIF Studio
This project is a Streamlit web application that allows users to generate GIFs from videos with text overlays corresponding to spoken words in the video. The approach involves transcribing the video, identifying GIF-worthy fragments, and creating GIFs with text overlays.

## Features

- Upload video files and generate GIFs with captions.
- Transcribe video audio to text.
- Identify sentences suitable for GIF captions using a language model.
- Extract specific video segments corresponding to identified captions.
- Add text overlays to video clips.
- Convert video clips to GIFs.
- Download all generated GIFs as a zip file.

## Overview 
![image](https://github.com/pvchaitanya8/AI-Powered-Video-to-GIF/assets/93573686/e9d79e32-4996-4546-a851-fa249183a304)
[Execution Vedio](https://youtu.be/IX0wxBDqjKg) 


## Output Images
![image](https://github.com/pvchaitanya8/AI-Powered-Video-to-GIF/assets/93573686/3a41759a-5af3-4fed-a746-ac81bd4477d5)
![image](https://github.com/pvchaitanya8/AI-Powered-Video-to-GIF/assets/93573686/c8590a45-6a46-4983-a84c-4c6f33d06484)
![image](https://github.com/pvchaitanya8/AI-Powered-Video-to-GIF/assets/93573686/b6d9d7e2-21d6-4371-bec6-3bda0a1f8c6b)
![image](https://github.com/pvchaitanya8/AI-Powered-Video-to-GIF/assets/93573686/a6179e74-6d7b-400c-a2fb-d591cc8217f8)
![image](https://github.com/pvchaitanya8/AI-Powered-Video-to-GIF/assets/93573686/d95d66e7-4860-425a-b3fa-5785003d10a4)


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

3. Open the Streamlit app in your web browser. The default URL is `http://localhost:8501`.

4. Upload a video file using the file uploader.

5. Configure the caption settings in the sidebar (font style, scale, color, thickness).

6. Generate GIFs by clicking the "Generate GIFs" button.

7. Download the generated GIFs as a zip file.

## Project Structure

- `app.py`: Main application file containing the Streamlit UI and backend logic.
- `requirements.txt`: List of required Python packages.
- `README.md`: This readme file.

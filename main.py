import os
import json
from transcribe import extract_audio, transcribe_audio
from analyze import analyze_transcript
from create_gifs import create_gif

def main(video_file):
    # Step 1: Extract audio and transcribe
    audio_file = extract_audio(video_file)
    transcript = transcribe_audio(audio_file)
    
    with open("transcript.json", "w") as f:
        json.dump(transcript, f, indent=4)
    
    # Step 2: Analyze transcript for GIF-worthy segments
    suggestions = analyze_transcript(transcript)
    
    with open("suggestions.json", "w") as f:
        json.dump(suggestions, f, indent=4)
    
    # Step 3: Create GIFs from suggestions
    create_gif(video_file, suggestions)

if __name__ == "__main__":
    video_file = "input_video.mp4"
    main(video_file)

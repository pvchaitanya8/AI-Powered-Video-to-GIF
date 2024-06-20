
import tkinter as tk
from tkinter import filedialog
import speech_recognition as sr
import moviepy.editor as mp
from moviepy.video.VideoClip import TextClip
import openai
import os

# Function to transcribe video to text
def transcribe_video(video_path):
    recognizer = sr.Recognizer()
    video = mp.VideoFileClip(video_path)
    audio_path = "temp_audio.wav"
    video.audio.write_audiofile(audio_path)
    
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
    
    transcript = recognizer.recognize_google(audio)
    os.remove(audio_path)
    return transcript

# Function to identify GIF materials using OpenAI GPT
def identify_gif_material(transcript, openai_api_key):
    openai.api_key = openai_api_key
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Identify potential GIF materials from the transcript:\n\n{transcript}",
        max_tokens=150
    )
    return response.choices[0].text.strip().split('\n')

# Function to create GIFs
def create_gifs(video_path, gif_materials):
    video = mp.VideoFileClip(video_path)
    gifs = []
    for i, text in enumerate(gif_materials):
        text_clip = TextClip(text, fontsize=70, color='white', size=video.size)
        text_clip = text_clip.set_position('center').set_duration(5)
        gif_clip = mp.CompositeVideoClip([video, text_clip])
        gif_path = f"output_{i}.gif"
        gif_clip.write_gif(gif_path)
        gifs.append(gif_path)
    return gifs

# Function to browse and select a video file
def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.avi *.mov")])
    if file_path:
        video_path.set(file_path)

# Function to start the GIF generation process
def generate_gifs():
    video_file = video_path.get()
    api_key = openai_api_key.get()
    transcript = transcribe_video(video_file)
    gif_materials = identify_gif_material(transcript, api_key)
    gifs = create_gifs(video_file, gif_materials)
    result_label.config(text=f"GIFs created: {', '.join(gifs)}")

# GUI setup
root = tk.Tk()
root.title("GIF Generator")

tk.Label(root, text="Select Video File:").grid(row=0, column=0, padx=10, pady=10)
video_path = tk.StringVar()
tk.Entry(root, textvariable=video_path, width=50).grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=browse_file).grid(row=0, column=2, padx=10, pady=10)

tk.Label(root, text="OpenAI API Key:").grid(row=1, column=0, padx=10, pady=10)
openai_api_key = tk.StringVar()
tk.Entry(root, textvariable=openai_api_key, width=50).grid(row=1, column=1, padx=10, pady=10)

tk.Button(root, text="Generate GIFs", command=generate_gifs).grid(row=2, column=0, columnspan=3, padx=10, pady=10)

result_label = tk.Label(root, text="")
result_label.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

root.mainloop()

import streamlit as st
import os
import cv2
import json
from textwrap import dedent
import moviepy.editor as mp
from pydub import AudioSegment
import speech_recognition as sr
from moviepy.editor import VideoFileClip
from zipfile import ZipFile

from langchain_groq import ChatGroq
from crewai import Agent, Task, Process, Crew

GROQ_API_KEY = "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"
LLM_Model = "llama3-8b-8192"

def transcribe_video(video_path):
    recognizer = sr.Recognizer()
    video = mp.VideoFileClip(video_path)
    audio_path = "temp_audio.wav"
    video.audio.write_audiofile(audio_path)

    transcript = ""
    try:
        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)
        transcript = recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        transcript = "Google Speech Recognition could not understand audio"
    except sr.RequestError as e:
        transcript = f"Could not request results from Google Speech Recognition service; {e}"
    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)

    return transcript

def create_gif_caption_identifier_task(api_key, model, Text_Transcript):
    LLM_Grouq = ChatGroq(
        api_key=api_key,
        model=model
    )

    GIF_caption_identifier = Agent(
        role="GIF Caption Finder",
        goal="Identify sentences that can be used as text over GIFs",
        backstory=dedent("""\
            You're a GIF caption expert tasked with identifying sentences that are ideal for adding text overlays to GIFs. 
            Your role is crucial in selecting text fragments that convey impactful and memorable messages to enhance the visual appeal and communication of the GIFs. 
            Your task is to carefully read the provided text and list all sentences that are suitable for GIF captions, ensuring they are concise, relevant, and engaging.
        """),
        verbose=True,
        allow_delegation=True,
        llm=LLM_Grouq,
        memory=True,
    )

    GIF_caption_identifier_Task = Task(
        description=dedent(f"""\
            **INPUT:**
                * **Text:**
                    {Text_Transcript}
            **TASK:**
                Identify sentences within the text that can be used as captions for GIFs. ENSURE THE SELECTED SENTENCES ARE EXACTLY AS IN THE INPUT TEXT. NO SINGLE WORD OR LETTER SHOULD BE DIFFERENT OR NEW.
            
            **MANDATORY NOTE:**
                OUTPUT ONLY JSON. Absolutely nothing else.

            **OUTPUT:**
                Output the selected sentences as a JSON object, with each sentence being a separate entry.

            
            **EXAMPLE OUTPUT:**
                {{
                    "captions": [
                        "This is a perfect moment!",
                        "I can't believe this is happening.",
                        "Let's make this unforgettable."
                    ]
                }}
        """),
        agent=GIF_caption_identifier,
        expected_output=dedent("""\
            {
                "captions": [
                    "Sentence 1",
                    "Sentence 2",
                    ...
                    "Sentence n"
                ]
            }
        """),
        async_execution=False
    )

    crew = Crew(
        agents=[GIF_caption_identifier],
        tasks=[GIF_caption_identifier_Task],
        verbose=2,
        process=Process.sequential,
    )

    crew_result = crew.kickoff()

    return crew_result


def extract_audio_from_video(video_path, audio_path):
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)

def transcribe_audio_chunk(recognizer, audio_chunk):
    with sr.AudioFile(audio_chunk) as source:
        audio_data = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio_data).lower()
        except sr.UnknownValueError:
            return ""

def find_sentence_times(audio_path, target_sentence, initial_chunk_duration=2000, max_chunk_duration=10000):
    recognizer = sr.Recognizer()
    audio = AudioSegment.from_file(audio_path)

    audio_length = len(audio)
    target_sentence = target_sentence.lower()

    start_time = None
    end_time = None

    chunk_duration = initial_chunk_duration
    overlap_duration = initial_chunk_duration // 2 

    while chunk_duration <= max_chunk_duration:
        for i in range(0, audio_length, chunk_duration - overlap_duration): 
            chunk = audio[i:i+chunk_duration]
            chunk.export("chunk.wav", format="wav")

            text = transcribe_audio_chunk(recognizer, "chunk.wav")

            if target_sentence in text:
                sentence_start_index = text.find(target_sentence)
                sentence_end_index = sentence_start_index + len(target_sentence)

                start_time = i / 1000.0 + sentence_start_index / len(text) * chunk_duration / 1000.0
                end_time = i / 1000.0 + sentence_end_index / len(text) * chunk_duration / 1000.0

                break
        if start_time is not None:
            break
        chunk_duration += 1000  

    return start_time, end_time

def save_video_clip(video_path, start_time, end_time, output_path):
    video = VideoFileClip(video_path)
    clip = video.subclip(start_time, end_time)
    clip.write_videofile(output_path, codec="libx264")

def add_text_to_video(caption, video_path, output_path, font=cv2.FONT_HERSHEY_SIMPLEX):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error opening video file: {video_path}")
        return

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        font_scale = 3
        font_color = (255, 255, 255)  
        thickness = 9
        text_size = cv2.getTextSize(caption, font, font_scale, thickness)[0]
        text_x = (frame_width - text_size[0]) // 2
        text_y = frame_height - 160

        cv2.putText(frame, caption, (text_x, text_y), font, font_scale, font_color, thickness, cv2.LINE_AA)

        out.write(frame)

    cap.release()
    out.release()
    print(f"Processed video saved as {output_path}")

def convert_mp4_to_gif(mp4_file, speed_factor=4):
    gif_file = mp4_file.replace('.mp4', '.gif')
    clip = VideoFileClip(mp4_file)
    clip = clip.speedx(factor=speed_factor)
    clip.write_gif(gif_file)
    print(f"Converted {mp4_file} to {gif_file} with speed factor {speed_factor}")

st.title("Video to GIF Generator")
st.write("Upload a video file to generate GIFs with captions")

uploaded_file = st.file_uploader("Choose a video file...", type=["mp4"])
if uploaded_file is not None:
    video_path = f"uploaded_{uploaded_file.name}"
    with open(video_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.video(video_path)

    if st.button("Generate GIFs"):
        progress_bar = st.progress(0)
        status_text = st.empty()

        with st.spinner("Transcribing video..."):
            text_transcript = transcribe_video(video_path)

        progress_bar.progress(25)
        status_text.text("Step 1: Video transcribed successfully")

        with st.spinner("Identifying GIF-worthy captions..."):
            gif_sentences = create_gif_caption_identifier_task(GROQ_API_KEY, LLM_Model, text_transcript)
            if gif_sentences:
                pass
            else:
                st.write("Error: No captions identified.")
                st.stop()

        progress_bar.progress(50)
        status_text.text("Step 2: Captions identified successfully")

        temp = json.loads(gif_sentences)
        gif_sentences_list = temp["captions"]

        audio_path = "audio.wav"
        extract_audio_from_video(video_path, audio_path)

        clips_paths = {}
        for i, caption in enumerate(gif_sentences_list, 1):
            start_time, end_time = find_sentence_times(audio_path, caption)
            if start_time is not None:
                output_path = f"output_clip_{i}.mp4"
                save_video_clip(video_path, start_time, end_time, output_path)
                clips_paths[caption] = output_path

        progress_bar.progress(75)
        status_text.text("Step 3: Video clips created successfully")

        clips_paths_captioned = []
        for caption, video_path in clips_paths.items():
            output_path = f"output_{caption.replace(' ', '_')}.mp4"
            clips_paths_captioned.append(output_path)
            add_text_to_video(caption, video_path, output_path, font=cv2.FONT_HERSHEY_SIMPLEX)

        progress_bar.progress(90)
        status_text.text("Step 4: Added text to video clips successfully")

        gif_files = []
        for mp4_file in clips_paths_captioned:
            convert_mp4_to_gif(mp4_file)
            gif_file = mp4_file.replace('.mp4', '.gif')
            gif_files.append(gif_file)

        progress_bar.progress(100)
        status_text.text("Step 5: Converted video clips to GIFs successfully")

        zip_file_path = "output_gifs.zip"
        with ZipFile(zip_file_path, 'w') as zipf:
            for gif_file in gif_files:
                zipf.write(gif_file)

        st.download_button(label="Download all GIFs", data=open(zip_file_path, 'rb').read(), file_name=zip_file_path, mime='application/zip')

        st.success("All steps completed!")

st.write("Note: This process may take some time depending on the length of the video and the number of GIFs generated.")

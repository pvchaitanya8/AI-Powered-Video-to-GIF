from google.cloud import speech_v1p1beta1 as speech
from moviepy.editor import VideoFileClip
import io
import os

def extract_audio(video_file):
    video = VideoFileClip(video_file)
    audio_file = "audio.wav"
    video.audio.write_audiofile(audio_file)
    return audio_file

def transcribe_audio(audio_file):
    client = speech.SpeechClient()
    
    with io.open(audio_file, "rb") as audio:
        content = audio.read()
    
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_word_time_offsets=True
    )
    
    response = client.recognize(config=config, audio=audio)
    
    transcript = []
    for result in response.results:
        for word_info in result.alternatives[0].words:
            transcript.append({
                "word": word_info.word,
                "start_time": word_info.start_time.total_seconds(),
                "end_time": word_info.end_time.total_seconds()
            })
    
    return transcript

if __name__ == "__main__":
    video_file = "input_video.mp4"
    audio_file = extract_audio(video_file)
    transcript = transcribe_audio(audio_file)
    with open("transcript.json", "w") as f:
        json.dump(transcript, f, indent=4)

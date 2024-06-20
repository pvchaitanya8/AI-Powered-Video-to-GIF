from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import json

def create_gif(video_file, segments):
    for segment in segments:
        start_time = segment['start_time']
        end_time = segment['end_time']
        text = segment['text']
        
        clip = VideoFileClip(video_file).subclip(start_time, end_time)
        txt_clip = TextClip(text, fontsize=70, color='white')
        txt_clip = txt_clip.set_pos('center').set_duration(clip.duration)
        
        video = CompositeVideoClip([clip, txt_clip])
        gif_file = f"gif_{int(start_time)}_{int(end_time)}.gif"
        video.write_gif(gif_file)

if __name__ == "__main__":
    video_file = "input_video.mp4"
    
    with open("suggestions.json", "r") as f:
        suggestions = json.load(f)
    
    create_gif(video_file, suggestions)

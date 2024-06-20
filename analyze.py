import openai
import json

def analyze_transcript(transcript):
    openai.api_key = 'YOUR_API_KEY'
    prompt = f"Identify potential GIF segments from the following transcript:\n{transcript}"
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=500
    )
    
    suggestions = response.choices[0].text.strip()
    return suggestions

if __name__ == "__main__":
    with open("transcript.json", "r") as f:
        transcript = json.load(f)
    
    suggestions = analyze_transcript(transcript)
    with open("suggestions.json", "w") as f:
        json.dump(suggestions, f, indent=4)

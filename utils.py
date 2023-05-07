import openai
from io import BytesIO
import tempfile
import os

# Create a function to transcribe audio using Whisper
def transcribe_audio(api_key, audio_file):
    openai.api_key = api_key
    with BytesIO(audio_file.read()) as audio_bytes:
        # Get the extension of the uploaded file
        file_extension = os.path.splitext(audio_file.name)[-1]
        
        # Create a temporary file with the uploaded audio data and the correct extension
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_audio_file:
            temp_audio_file.write(audio_bytes.read())
            temp_audio_file.seek(0)  # Move the file pointer to the beginning of the file
            
            # Transcribe the temporary audio file
            transcript = openai.Audio.translate("whisper-1", temp_audio_file)

    return transcript

# Create a function to summarize the transcript using a custom prompt
def summarize_transcript(api_key, transcript, model, custom_prompt=None):
    openai.api_key = api_key
    prompt = f"Please summarize the following audio transcription: {transcript}"
    if custom_prompt:
        prompt = f"{custom_prompt}\n\n{transcript}"
    

    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=150,
    )
    
    summary = response['choices'][0]['message']['content']
    return summary
import openai
from io import BytesIO
import tempfile
import os
import streamlit as st

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

def call_gpt(api_key, prompt, model):
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=400,
    )
    
    return response['choices'][0]['message']['content']

def call_gpt_streaming(api_key,prompt, model):
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        stream=True
    )

    collected_events = []
    completion_text = ''
    placeholder = st.empty()

    for event in response:
        collected_events.append(event)
        # Check if content key exists
        if "content" in event['choices'][0]["delta"]:
            event_text = event['choices'][0]["delta"]["content"]
            completion_text += event_text
            placeholder.write(completion_text)  # Write the received text
    return completion_text

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


def generate_image_prompt(api_key, user_input):
    openai.api_key = api_key

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": f"Create a text that explains in a lot of details how the meme about this topic would look like: {user_input}"}],
        temperature=0.7,
        max_tokens=50,
    )

    return response['choices'][0]['message']['content']

def generate_image(api_key, prompt):
    openai.api_key = api_key

    response = openai.Image.create(
        model="image-alpha-001",
        prompt=prompt,
        n=1,
        size="256x256",
        response_format="url",
    )

    return response['data'][0]['url']
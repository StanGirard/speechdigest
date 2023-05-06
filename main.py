import streamlit as st
import openai
from io import BytesIO
import tempfile
import os


# Create a function to transcribe audio using Whisper
def transcribe_audio(api_key, audio_file):
    openai.api_key = api_key
    with BytesIO(audio_file.read()) as audio_bytes:
        # Get the extension of the uloaded file
        file_extension = os.path.splitext(audio_file.name)[-1]
        
        # Create a temporary file with the uploaded audio data and the correct extension
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_audio_file:
            temp_audio_file.write(audio_bytes.read())
            temp_audio_file.seek(0)  # Move the file pointer to the beginning of the file
            
            # Transcribe the temporary audio file
            transcript = openai.Audio.translate("whisper-1", temp_audio_file)

    return transcript

# Create a function to summarize the transcript using a custom prompt
def summarize_transcript(api_key, transcript, model):
    openai.api_key = api_key
    prompt = f"Please summarize the following audio transcription: {transcript}"

    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=150,
    )
    
    summary = response['choices'][0]['message']['content']
    return summary

# Streamlit app
st.title("Audio Transcription and Summarization")
st.write("Upload an audio file, transcribe it using Whisper, and summarize the transcription using your selected model.")

api_key = st.text_input("Enter your OpenAI API key:", type="password")
models = ["gpt-3.5-turbo", "gpt-4"]
model = st.selectbox("Select a model:", models)

uploaded_audio = st.file_uploader("Upload an audio file", type=['m4a', 'mp3', 'webm', 'mp4', 'mpga', 'wav', 'mpeg'], accept_multiple_files=False)

if uploaded_audio:
    if api_key:
        st.write("Transcribing the audio...")
        transcript = transcribe_audio(api_key, uploaded_audio)
        st.write("Transcription:", transcript)

        st.write("Summarizing the transcription...")
        summary = summarize_transcript(api_key, transcript, model)
        st.write("Summary:", summary)
    else:
        st.error("Please enter a valid OpenAI API key.")
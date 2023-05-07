import streamlit as st
from utils import transcribe_audio, summarize_transcript
import theme




# Streamlit app
st.set_page_config(**theme.page_config)


title = """
    <h1 style="color:#32CD32; font-family:sans-serif;">🎙️ Audio Transcription and Summarization 🎙️</h1>
"""
st.markdown(title, unsafe_allow_html=True)
st.write("Upload an audio file, transcribe it using Whisper, and summarize the transcription using your selected model.")

api_key = st.text_input("Enter your OpenAI API key:", type="password")
models = ["gpt-3.5-turbo", "gpt-4"]
model = st.selectbox("Select a model:", models)

uploaded_audio = st.file_uploader("Upload an audio file", type=['m4a', 'mp3', 'webm', 'mp4', 'mpga', 'wav', 'mpeg'], accept_multiple_files=False)

custom_prompt = None

custom_prompt = st.text_input("Enter a custom prompt:", value = "Summarize the following audio transcription:")

if st.button("Generate Summary"):
    if uploaded_audio:
        if api_key:
            st.markdown("Transcribing the audio...")
            transcript = transcribe_audio(api_key, uploaded_audio)
            st.markdown(f"###  Transcription:\n\n<details><summary>Click to view</summary><p><pre><code>{transcript.text}</code></pre></p></details>", unsafe_allow_html=True)

            st.markdown("Summarizing the transcription...")
            if custom_prompt:
                summary = summarize_transcript(api_key, transcript, model, custom_prompt)
            else:
                summary = summarize_transcript(api_key, transcript, model)
                
            st.markdown(f"### Summary:")
            st.write(summary)
        else:
            st.error("Please enter a valid OpenAI API key.")


st.markdown(
    """
    ---
    ### Source code and contact information
    - The source code for this app can be found on GitHub: [SpeechDigest](https://github.com/StanGirard/speechdigest)
    - If you have any questions or comments, feel free to reach out to me on Twitter: [@_StanGirard](https://twitter.com/_StanGirard)
    """
)

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        [![Tweet](https://img.shields.io/twitter/url?url=https%3A%2F%2Fgithub.com%2FStanGirard%2Fspeechdigest)](https://twitter.com/intent/tweet?url=https://github.com/StanGirard/speechdigest&text=Check%20out%20this%20awesome%20Speech%20Digest%20app%20built%20with%20Streamlit!%20%23speechdigest%20%23streamlit)
        """
    )

with col2:
    st.markdown(
        """
        [![GitHub Stars](https://img.shields.io/github/stars/StanGirard/speechdigest?style=social)](https://github.com/StanGirard/speechdigest/stargazers)
        """
    )
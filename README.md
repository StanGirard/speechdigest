# Speech Digest

This Streamlit app allows users to upload an audio file, transcribe the audio using OpenAI's Whisper ASR, and then summarize the transcription using OpenAI's GPT-3.5-turbo language model.

## Features

- Upload audio files in supported formats (m4a, mp3, webm, mp4, mpga, wav, and mpeg)
- Transcribe audio using OpenAI's Whisper ASR
- Summarize transcribed audio using OpenAI's GPT-3.5-turbo
- Provide custom API key and select the desired model

## Installation

### Prerequisites

- Python 3.6 or higher
- Streamlit
- OpenAI Python library (v0.27.0 or higher)

### Steps

1. Clone the repository:

```
git clone https://github.com/StanGirard/speechdigest
```

2. Change into the repository's directory:

```
cd speechdigest
```

3. Install the required packages:

```
pip install -r requirements.txt
```

4. Set your OpenAI API key as an environment variable:

```
export OPENAI_API_KEY="your-api-key"
```

5. Run the Streamlit app:

```
streamlit run app.py
```

The app will now be accessible at `http://localhost:8501` in your browser.

## Usage

1. Open the app in your browser.
2. Enter your OpenAI API key and select the desired model (GPT-4 or GPT-3.5-turbo) using the input fields.
3. Upload an audio file in a supported format using the file uploader.
4. The app will transcribe the audio using Whisper ASR and display the transcription.
5. The app will then summarize the transcription using the selected language model and display the summary.

## Contributing

Feel free to submit issues, feature requests, or pull requests. We appreciate any contribution to improve the app.
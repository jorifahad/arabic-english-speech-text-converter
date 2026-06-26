# SawtAI — Arabic and English Speech & Text Converter

SawtAI is a bilingual Streamlit application that converts spoken Arabic or English into editable text and turns written content back into downloadable speech.

## Features

- Upload WAV, MP3, M4A, MP4, MPEG, and MPGA files.
- Record audio directly from the browser.
- Automatic language detection with optional Arabic or English selection.
- Whisper model selection: Tiny, Base, or Small.
- Editable transcription with detected language and word count.
- Download transcription as TXT.
- Arabic and English text-to-speech.
- Audio playback and MP3 download.
- Responsive dark interface designed for portfolio presentation.

## Technologies

- Python
- Streamlit
- OpenAI Whisper
- gTTS
- FFmpeg

## Run Locally

1. Install FFmpeg.
2. Install the Python dependencies:

```bash
pip install -r requirements.txt
```

3. Start the application:

```bash
streamlit run whisper-app.py
```

Whisper downloads the selected model the first time it is used. Text-to-speech generation through gTTS requires an internet connection.

## Project Origin

This project was developed from an archived multilingual Whisper transcription application and substantially expanded with a redesigned interface, browser recording, language and model controls, editable downloads, and Arabic-English text-to-speech.

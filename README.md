# SawtAI — Arabic & English Speech–Text Converter

SawtAI is a bilingual web application independently built at the application level. It integrates pre-trained Whisper models for speech recognition and gTTS for speech synthesis.

## Features

- Upload audio files or record directly from the browser.
- Convert Arabic and English speech into editable text.
- Automatic language detection or manual language selection.
- Choose between Whisper Tiny, Base, and Small models.
- Display detected language and word count.
- Download transcription as TXT.
- Convert Arabic and English text into speech.
- Play generated audio and download it as MP3.
- Responsive dark interface designed for portfolio presentation.

## Project Structure

```text
SawtAI_from_scratch/
├── app.py
├── requirements.txt
├── packages.txt
├── README.md
├── services/
│   ├── __init__.py
│   ├── speech_to_text.py
│   └── text_to_speech.py
├── ui/
│   ├── __init__.py
│   └── styles.py
└── .streamlit/
    └── config.toml
```

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deployment

For Streamlit Community Cloud, use `app.py` as the main file path.

## Model Note

The application code and interface are independently structured. Speech recognition uses pre-trained Whisper models, while text-to-speech uses gTTS.

# SawtAI — Arabic & English Speech, Text, and Image Converter

SawtAI is a bilingual accessibility and content-conversion web application built from scratch at the application level. It integrates pre-trained models and libraries for speech recognition, text-to-speech, and optical character recognition.

## Features

### Speech to Text
- Upload an audio file or record directly from the browser.
- Convert Arabic and English speech into editable text.
- Automatic language detection or manual language selection.
- Choose between Whisper Tiny, Base, and Small.
- Download the transcription as TXT.

### Text to Speech
- Convert Arabic or English text into speech.
- Listen to the generated audio in the browser.
- Download the result as MP3.
- Optional slower speaking speed.

### Image to Speech
- Upload PNG, JPG, JPEG, or WEBP images.
- Extract Arabic or English text using PaddleOCR.
- Review and edit the extracted text.
- Download the extracted text as TXT.
- Convert the extracted text into speech.
- Download the generated image narration as MP3.

## Technologies

- Python
- Streamlit
- OpenAI Whisper
- PaddleOCR
- gTTS
- FFmpeg

## Project Structure

```text
├── app.py
├── requirements.txt
├── packages.txt
├── README.md
├── services/
│   ├── __init__.py
│   ├── speech_to_text.py
│   ├── text_to_speech.py
│   └── image_ocr.py
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

FFmpeg must also be installed on the system.

## Deployment

For Streamlit Community Cloud:

- Main file path: `app.py`
- Keep `packages.txt` in the repository root.
- The first OCR run may take longer because PaddleOCR downloads its pre-trained recognition models.

## Model Note

The application code and interface are independently developed. Whisper and PaddleOCR are pre-trained models, while gTTS provides speech synthesis.

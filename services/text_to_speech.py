from __future__ import annotations

from io import BytesIO

from gtts import gTTS

TTS_LANGUAGE_OPTIONS = {
    "Arabic": "ar",
    "English": "en",
}

def create_speech(text: str, language_code: str, slow: bool = False) -> bytes:
    if not text.strip():
        raise ValueError("Text cannot be empty.")

    output_buffer = BytesIO()
    speech = gTTS(text=text, lang=language_code, slow=slow)
    speech.write_to_fp(output_buffer)
    return output_buffer.getvalue()

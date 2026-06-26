from __future__ import annotations

import os
import tempfile
from pathlib import Path
from typing import Optional, Tuple

import streamlit as st
import whisper

LANGUAGE_OPTIONS = {
    "Auto Detect": None,
    "Arabic": "ar",
    "English": "en",
}

@st.cache_resource(show_spinner="Loading Whisper model...")
def load_whisper_model(model_name: str):
    return whisper.load_model(model_name)

def _save_audio_to_temporary_file(audio_source) -> str:
    original_name = getattr(audio_source, "name", "")
    suffix = Path(original_name).suffix or ".wav"
    audio_bytes = audio_source.getbuffer() if hasattr(audio_source, "getbuffer") else audio_source.read()

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temporary_file:
        temporary_file.write(audio_bytes)
        return temporary_file.name

def transcribe_audio(
    audio_source,
    model_name: str,
    language_code: Optional[str] = None,
) -> Tuple[str, str]:
    temporary_path = _save_audio_to_temporary_file(audio_source)

    try:
        model = load_whisper_model(model_name)
        options = {"fp16": False}
        if language_code:
            options["language"] = language_code

        result = model.transcribe(temporary_path, **options)
        text = result.get("text", "").strip()
        detected_language = result.get("language", language_code or "unknown")
        return text, detected_language
    finally:
        if os.path.exists(temporary_path):
            os.remove(temporary_path)

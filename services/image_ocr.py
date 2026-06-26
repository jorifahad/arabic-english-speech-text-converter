from __future__ import annotations

from typing import Any

import streamlit as st
from PIL import Image
from surya.detection import DetectionPredictor
from surya.recognition import RecognitionPredictor


# Keep the same values expected by app.py and gTTS.
# Surya itself detects the script automatically, so language_code is accepted
# for interface compatibility but is not passed to the model.
OCR_LANGUAGE_OPTIONS = {
    "Arabic": "ar",
    "English": "en",
}


@st.cache_resource(show_spinner="Loading Surya OCR models...")
def load_ocr_models() -> tuple[RecognitionPredictor, DetectionPredictor]:
    """Load the Surya v1 OCR models once for all Streamlit reruns."""
    recognition_predictor = RecognitionPredictor()
    detection_predictor = DetectionPredictor()
    return recognition_predictor, detection_predictor


def _read_text(value: Any) -> str:
    """Extract recognized text safely from Surya result objects or dictionaries."""
    if value is None:
        return ""

    if isinstance(value, str):
        return " ".join(value.split()).strip()

    if isinstance(value, dict):
        for key in ("text", "html"):
            text = _read_text(value.get(key))
            if text:
                return text
        return ""

    text = getattr(value, "text", None)
    if text:
        return " ".join(str(text).split()).strip()

    html = getattr(value, "html", None)
    if html:
        return " ".join(str(html).split()).strip()

    return ""


def extract_text_from_image(
    image: Image.Image,
    language_code: str,
) -> str:
    """Extract Arabic or English text from a PIL image using Surya OCR 0.14.6."""
    del language_code  # Surya is multilingual and detects the script automatically.

    if image is None:
        return ""

    recognition_predictor, detection_predictor = load_ocr_models()
    rgb_image = image.convert("RGB")

    # Surya v1 expects one language-list per image. Arabic and English are both
    # supplied because the app supports bilingual and mixed documents.
    predictions = recognition_predictor(
        [rgb_image],
        [["ar", "en"]],
        detection_predictor,
    )

    if not predictions:
        return ""

    page_result = predictions[0]
    text_lines = getattr(page_result, "text_lines", None)

    if text_lines is None and isinstance(page_result, dict):
        text_lines = page_result.get("text_lines", [])

    lines: list[str] = []
    for line in text_lines or []:
        text = _read_text(line)
        if text and (not lines or lines[-1] != text):
            lines.append(text)

    return "\n".join(lines).strip()

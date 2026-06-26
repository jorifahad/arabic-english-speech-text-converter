from __future__ import annotations

from typing import Any

import numpy as np
import streamlit as st
from PIL import Image
from paddleocr import PaddleOCR


OCR_LANGUAGE_OPTIONS = {
    "Arabic": "ar",
    "English": "en",
}


@st.cache_resource(show_spinner="Loading PaddleOCR model...")
def load_ocr_model(language_code: str):
    """Load and cache a PaddleOCR model."""
    try:
        return PaddleOCR(
            lang=language_code,
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=True,
        )
    except TypeError:
        return PaddleOCR(
            lang=language_code,
            use_angle_cls=True,
            show_log=False,
        )


def _collect_text(value: Any) -> list[str]:
    """Collect recognized text from PaddleOCR 2.x and 3.x result formats."""
    output: list[str] = []

    if value is None:
        return output

    if isinstance(value, str):
        cleaned = value.strip()
        if cleaned:
            output.append(cleaned)
        return output

    if isinstance(value, dict):
        for key in ("rec_texts", "texts", "text", "transcription"):
            if key in value:
                output.extend(_collect_text(value[key]))
        if output:
            return output
        for item in value.values():
            output.extend(_collect_text(item))
        return output

    if isinstance(value, (list, tuple)):
        if (
            len(value) >= 2
            and isinstance(value[1], (list, tuple))
            and value[1]
            and isinstance(value[1][0], str)
        ):
            output.append(value[1][0].strip())
            return output
        for item in value:
            output.extend(_collect_text(item))
        return output

    if hasattr(value, "json"):
        json_value = value.json() if callable(value.json) else value.json
        return _collect_text(json_value)

    if hasattr(value, "to_dict"):
        return _collect_text(value.to_dict())

    return output


def extract_text_from_image(image: Image.Image, language_code: str) -> str:
    """Extract Arabic or English text from an image."""
    model = load_ocr_model(language_code)
    image_array = np.asarray(image.convert("RGB"))

    if hasattr(model, "predict"):
        result = model.predict(image_array)
    else:
        result = model.ocr(image_array, cls=True)

    lines = _collect_text(result)
    cleaned_lines: list[str] = []

    for line in lines:
        cleaned = " ".join(line.split())
        if cleaned and (not cleaned_lines or cleaned_lines[-1] != cleaned):
            cleaned_lines.append(cleaned)

    return "\n".join(cleaned_lines).strip()

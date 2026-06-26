from __future__ import annotations

import numpy as np
import streamlit as st
from easyocr import Reader
from PIL import Image


# Values stay compatible with app.py and gTTS.
OCR_LANGUAGE_OPTIONS = {
    "Arabic": "ar",
    "English": "en",
}


@st.cache_resource(show_spinner="Loading EasyOCR model...")
def load_ocr_model() -> Reader:
    """Load one bilingual CPU model and reuse it across Streamlit reruns."""
    return Reader(
        ["ar", "en"],
        gpu=False,
        verbose=False,
    )


def extract_text_from_image(
    image: Image.Image,
    language_code: str,
) -> str:
    """Extract Arabic or English text from a PIL image using EasyOCR."""
    del language_code  # The bilingual reader handles Arabic, English, and mixed text.

    if image is None:
        return ""

    rgb_image = np.asarray(image.convert("RGB"))
    reader = load_ocr_model()

    results = reader.readtext(
        rgb_image,
        detail=1,
        paragraph=False,
        decoder="greedy",
        batch_size=1,
        workers=0,
    )

    if not results:
        return ""

    lines: list[str] = []

    for result in results:
        if not isinstance(result, (list, tuple)) or len(result) < 2:
            continue

        text = " ".join(str(result[1]).split()).strip()

        if text and (not lines or lines[-1] != text):
            lines.append(text)

    return "\n".join(lines).strip()

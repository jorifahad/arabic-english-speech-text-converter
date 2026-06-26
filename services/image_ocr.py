from __future__ import annotations

import os
from typing import Any

# تعطيل oneDNN وPIR لأنهما سببا الخطأ السابق على Streamlit.
os.environ["FLAGS_use_mkldnn"] = "0"
os.environ["FLAGS_enable_pir_api"] = "0"

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
    return PaddleOCR(
        lang=language_code,
        use_doc_orientation_classify=False,
        use_doc_unwarping=False,
        use_textline_orientation=True,
    )


def collect_text(value: Any) -> list[str]:
    texts: list[str] = []

    if value is None:
        return texts

    if isinstance(value, str):
        cleaned = " ".join(value.split())

        if cleaned:
            texts.append(cleaned)

        return texts

    if isinstance(value, dict):
        for key in ("rec_texts", "texts", "text"):
            if key in value:
                texts.extend(collect_text(value[key]))

        if texts:
            return texts

        for nested_value in value.values():
            texts.extend(collect_text(nested_value))

        return texts

    if isinstance(value, (list, tuple)):
        for item in value:
            texts.extend(collect_text(item))

        return texts

    if hasattr(value, "json"):
        json_value = value.json() if callable(value.json) else value.json
        texts.extend(collect_text(json_value))
        return texts

    if hasattr(value, "to_dict"):
        texts.extend(collect_text(value.to_dict()))
        return texts

    return texts


def extract_text_from_image(
    image: Image.Image,
    language_code: str,
) -> str:
    model = load_ocr_model(language_code)
    image_array = np.asarray(image.convert("RGB"))

    result = model.predict(image_array)
    lines = collect_text(result)

    unique_lines: list[str] = []

    for line in lines:
        if line and (not unique_lines or unique_lines[-1] != line):
            unique_lines.append(line)

    return "\n".join(unique_lines).strip()

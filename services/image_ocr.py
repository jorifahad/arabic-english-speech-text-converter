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
    return PaddleOCR(
        lang=language_code,
        use_angle_cls=True,
        use_gpu=False,
        enable_mkldnn=False,
        show_log=False,
    )


def extract_text_from_image(
    image: Image.Image,
    language_code: str,
) -> str:
    model = load_ocr_model(language_code)
    image_array = np.asarray(image.convert("RGB"))

    result = model.ocr(image_array, cls=True)

    lines = []

    if result:
        for page in result:
            if not page:
                continue

            for item in page:
                if (
                    isinstance(item, (list, tuple))
                    and len(item) >= 2
                    and isinstance(item[1], (list, tuple))
                    and len(item[1]) >= 1
                ):
                    text = str(item[1][0]).strip()

                    if text:
                        lines.append(text)

    return "\n".join(lines).strip()

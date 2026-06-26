from __future__ import annotations

from statistics import median

import numpy as np
import streamlit as st
from easyocr import Reader
from PIL import Image


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


def _box_metrics(box) -> tuple[float, float, float, float]:
    """Return left, right, vertical center, and height for an EasyOCR box."""
    xs = [float(point[0]) for point in box]
    ys = [float(point[1]) for point in box]

    left = min(xs)
    right = max(xs)
    top = min(ys)
    bottom = max(ys)

    return left, right, (top + bottom) / 2, max(bottom - top, 1.0)


def _arrange_text(results, language_code: str) -> str:
    """Group words into rows, then order Arabic right-to-left."""
    items = []

    for result in results:
        if not isinstance(result, (list, tuple)) or len(result) < 2:
            continue

        box, raw_text = result[0], result[1]
        text = " ".join(str(raw_text).split()).strip()

        if not text:
            continue

        left, right, center_y, height = _box_metrics(box)
        items.append(
            {
                "text": text,
                "left": left,
                "right": right,
                "center_y": center_y,
                "height": height,
            }
        )

    if not items:
        return ""

    typical_height = median(item["height"] for item in items)
    row_tolerance = max(typical_height * 0.65, 10.0)

    # Build rows from top to bottom.
    rows: list[dict] = []

    for item in sorted(items, key=lambda value: value["center_y"]):
        matching_row = None

        for row in rows:
            if abs(item["center_y"] - row["center_y"]) <= row_tolerance:
                matching_row = row
                break

        if matching_row is None:
            rows.append(
                {
                    "center_y": item["center_y"],
                    "items": [item],
                }
            )
        else:
            matching_row["items"].append(item)
            matching_row["center_y"] = sum(
                word["center_y"] for word in matching_row["items"]
            ) / len(matching_row["items"])

    rows.sort(key=lambda row: row["center_y"])

    rtl = language_code == "ar"
    output_lines: list[str] = []

    for row in rows:
        # Arabic is read from the rightmost detected segment to the leftmost.
        ordered_words = sorted(
            row["items"],
            key=lambda word: word["right"] if rtl else word["left"],
            reverse=rtl,
        )

        line = " ".join(word["text"] for word in ordered_words).strip()

        if line:
            output_lines.append(line)

    return "\n".join(output_lines).strip()


def extract_text_from_image(
    image: Image.Image,
    language_code: str,
) -> str:
    """Extract text and preserve natural Arabic/English reading order."""
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

    return _arrange_text(results, language_code)

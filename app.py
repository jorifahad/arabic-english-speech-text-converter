from __future__ import annotations

import streamlit as st
from PIL import Image

from services.image_ocr import OCR_LANGUAGE_OPTIONS, extract_text_from_image
from services.speech_to_text import LANGUAGE_OPTIONS, transcribe_audio
from services.text_to_speech import TTS_LANGUAGE_OPTIONS, create_speech
from ui.styles import apply_styles


st.set_page_config(
    page_title="SawtAI | Arabic & English Speech Converter",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

apply_styles()

DEFAULT_SESSION_VALUES = {
    "transcription": "",
    "detected_language": "",
    "generated_audio": None,
    "ocr_text": "",
    "ocr_audio": None,
}
for key, default_value in DEFAULT_SESSION_VALUES.items():
    if key not in st.session_state:
        st.session_state[key] = default_value


st.markdown(
    """
    <section class="hero">
        <div class="eyebrow">Bilingual Speech & Document Intelligence</div>
        <h1>Sawt<span>AI</span></h1>
        <p>
            Convert Arabic and English speech into editable text, transform written
            content into audio, and make text inside images readable and listenable.
        </p>
        <div class="feature-row">
            <span class="feature-pill">Speech Recognition</span>
            <span class="feature-pill">Text-to-Speech</span>
            <span class="feature-pill">Image OCR</span>
            <span class="feature-pill">Arabic & English</span>
            <span class="feature-pill">Downloadable Results</span>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

speech_tab, tts_tab, image_tab, about_tab = st.tabs(
    [
        "🎙️ Speech to Text",
        "🔊 Text to Speech",
        "🖼️ Image to Speech",
        "✨ About SawtAI",
    ]
)


with speech_tab:
    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown("### Add your audio")
        source_mode = st.radio(
            "Audio source",
            options=["Upload a file", "Record now"],
            horizontal=True,
            label_visibility="collapsed",
        )

        if source_mode == "Upload a file":
            audio_source = st.file_uploader(
                "Upload WAV, MP3, M4A, MP4, MPEG, or MPGA",
                type=["wav", "mp3", "m4a", "mp4", "mpeg", "mpga"],
            )
        else:
            audio_source = st.audio_input("Record your voice")

        selected_language = st.selectbox(
            "Spoken language",
            options=list(LANGUAGE_OPTIONS.keys()),
            index=0,
            help="Use Auto Detect when the spoken language is unknown.",
        )
        selected_model = st.selectbox(
            "Whisper model",
            options=["tiny", "base", "small"],
            index=1,
            help="Tiny is faster. Small is usually more accurate but needs more memory.",
        )
        transcribe_button = st.button(
            "Transcribe audio",
            type="primary",
            use_container_width=True,
        )

    with right:
        st.markdown("### Transcription")
        if transcribe_button:
            if audio_source is None:
                st.warning("Upload or record an audio clip first.")
            else:
                with st.spinner("Listening and converting speech into text..."):
                    try:
                        text, detected_language = transcribe_audio(
                            audio_source=audio_source,
                            model_name=selected_model,
                            language_code=LANGUAGE_OPTIONS[selected_language],
                        )
                        st.session_state.transcription = text
                        st.session_state.detected_language = detected_language
                    except Exception as error:
                        st.error(f"Transcription failed: {error}")

        edited_text = st.text_area(
            "Editable transcription",
            value=st.session_state.transcription,
            height=320,
            placeholder="Your transcription will appear here...",
        )
        st.session_state.transcription = edited_text

        if edited_text.strip():
            metric_left, metric_right = st.columns(2)
            metric_left.metric(
                "Detected language",
                st.session_state.detected_language.upper() or "UNKNOWN",
            )
            metric_right.metric("Word count", len(edited_text.split()))
            st.download_button(
                "Download transcription",
                data=edited_text.encode("utf-8"),
                file_name="sawtai-transcription.txt",
                mime="text/plain",
                use_container_width=True,
            )


with tts_tab:
    left, right = st.columns([1.15, 0.85], gap="large")

    with left:
        st.markdown("### Write or paste text")
        tts_text = st.text_area(
            "Text to convert",
            height=320,
            placeholder="اكتب النص هنا أو paste English text...",
            key="tts_text",
        )

    with right:
        st.markdown("### Voice settings")
        tts_language_name = st.selectbox(
            "Output language",
            options=list(TTS_LANGUAGE_OPTIONS.keys()),
            index=0,
        )
        slow_speech = st.toggle("Slower speaking speed", value=False)
        generate_button = st.button(
            "Generate speech",
            type="primary",
            use_container_width=True,
        )

        if generate_button:
            if not tts_text.strip():
                st.warning("Enter some text first.")
            else:
                with st.spinner("Generating speech..."):
                    try:
                        st.session_state.generated_audio = create_speech(
                            text=tts_text.strip(),
                            language_code=TTS_LANGUAGE_OPTIONS[tts_language_name],
                            slow=slow_speech,
                        )
                    except Exception as error:
                        st.error(f"Speech generation failed: {error}")

        if st.session_state.generated_audio:
            st.audio(st.session_state.generated_audio, format="audio/mp3")
            st.download_button(
                "Download MP3",
                data=st.session_state.generated_audio,
                file_name="sawtai-speech.mp3",
                mime="audio/mpeg",
                use_container_width=True,
            )


with image_tab:
    upload_column, result_column = st.columns([0.9, 1.1], gap="large")

    with upload_column:
        st.markdown("### Upload an image")
        uploaded_image = st.file_uploader(
            "Upload PNG, JPG, JPEG, or WEBP",
            type=["png", "jpg", "jpeg", "webp"],
            key="ocr_image",
        )
        ocr_language_name = st.selectbox(
            "Text language",
            options=list(OCR_LANGUAGE_OPTIONS.keys()),
            index=0,
            help="Choose the main language visible in the image.",
        )
        extract_button = st.button(
            "Extract text from image",
            type="primary",
            use_container_width=True,
        )

        if uploaded_image is not None:
            image = Image.open(uploaded_image).convert("RGB")
            st.image(image, caption="Uploaded image", use_container_width=True)
        else:
            image = None

    with result_column:
        st.markdown("### Extracted text and audio")

        if extract_button:
            if image is None:
                st.warning("Upload an image first.")
            else:
                with st.spinner("Reading text from the image with EasyOCR..."):
                    try:
                        extracted_text = extract_text_from_image(
                            image=image,
                            language_code=OCR_LANGUAGE_OPTIONS[ocr_language_name],
                        )
                        if extracted_text:
                            st.session_state.ocr_text = extracted_text
                            st.session_state.ocr_audio = None
                        else:
                            st.warning(
                                "No readable text was detected. Try a clearer image "
                                "or select the other language."
                            )
                    except Exception as error:
                        st.error(f"Image text extraction failed: {error}")

        editable_ocr_text = st.text_area(
            "Review and edit extracted text",
            value=st.session_state.ocr_text,
            height=270,
            placeholder="Text extracted from the image will appear here...",
            key="editable_ocr_text",
        )
        st.session_state.ocr_text = editable_ocr_text

        slow_image_speech = st.toggle(
            "Slower image reading speed",
            value=False,
        )
        generate_image_audio = st.button(
            "Read extracted text aloud",
            use_container_width=True,
        )

        if generate_image_audio:
            if not editable_ocr_text.strip():
                st.warning("Extract text from an image or enter text first.")
            else:
                with st.spinner("Generating audio from the extracted text..."):
                    try:
                        st.session_state.ocr_audio = create_speech(
                            text=editable_ocr_text.strip(),
                            language_code=OCR_LANGUAGE_OPTIONS[ocr_language_name],
                            slow=slow_image_speech,
                        )
                    except Exception as error:
                        st.error(f"Audio generation failed: {error}")

        if editable_ocr_text.strip():
            st.download_button(
                "Download extracted text",
                data=editable_ocr_text.encode("utf-8"),
                file_name="sawtai-image-text.txt",
                mime="text/plain",
                use_container_width=True,
            )

        if st.session_state.ocr_audio:
            st.audio(st.session_state.ocr_audio, format="audio/mp3")
            st.download_button(
                "Download image audio",
                data=st.session_state.ocr_audio,
                file_name="sawtai-image-speech.mp3",
                mime="audio/mpeg",
                use_container_width=True,
            )


with about_tab:
    st.markdown(
        """
        ### One workspace for speech, text, and images

        SawtAI is a bilingual accessibility and content-conversion application
        developed for Arabic and English.

        - **Speech to Text:** Upload or record audio and convert it into editable text.
        - **Text to Speech:** Turn written content into downloadable MP3 audio.
        - **Image to Speech:** Extract Arabic or English text from an image using
          EasyOCR, review it, and convert it into speech.
        - **Model Control:** Choose between Tiny, Base, and Small Whisper models.
        - **Practical Outputs:** Edit, listen to, and download results directly
          from the browser.

        ### Technologies

        `Python` · `Streamlit` · `OpenAI Whisper` · `EasyOCR` · `gTTS` · `FFmpeg`
        """
    )

st.markdown(
    """
    <p class="footer-note">
        SawtAI · Arabic and English Speech, Text & Image Converter
    </p>
    """,
    unsafe_allow_html=True,
)

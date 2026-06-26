from __future__ import annotations

import os
import tempfile
from io import BytesIO
from pathlib import Path

import streamlit as st
import whisper
from gtts import gTTS

LANGUAGE_OPTIONS = {"Auto Detect": None, "Arabic": "ar", "English": "en"}

st.set_page_config(
    page_title="SawtAI | Speech & Text Converter",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
        .stApp {
            background:
                radial-gradient(circle at 10% 15%, rgba(109, 94, 252, 0.16), transparent 30%),
                radial-gradient(circle at 88% 8%, rgba(0, 207, 255, 0.12), transparent 28%),
                #070b18;
            color: #f4f7ff;
        }
        [data-testid="stHeader"] { background: transparent; }
        .block-container { max-width: 1180px; padding-top: 2.5rem; padding-bottom: 4rem; }
        .hero {
            padding: 2.4rem 2.6rem;
            border: 1px solid rgba(255,255,255,0.10);
            border-radius: 28px;
            background: linear-gradient(135deg, rgba(18, 28, 58, 0.92), rgba(9, 14, 31, 0.90));
            box-shadow: 0 24px 70px rgba(0,0,0,0.30);
            margin-bottom: 1.8rem;
        }
        .eyebrow {
            color: #8b82ff; font-size: 0.82rem; font-weight: 800;
            letter-spacing: 0.18em; text-transform: uppercase; margin-bottom: 0.7rem;
        }
        .hero h1 {
            color: #ffffff; font-size: clamp(2.5rem, 6vw, 5rem); line-height: 0.98;
            margin: 0; letter-spacing: -0.05em;
        }
        .hero h1 span {
            background: linear-gradient(90deg, #8d7cff, #42d9ff);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        .hero p {
            color: #b9c3dc; font-size: 1.08rem; line-height: 1.8;
            max-width: 780px; margin: 1.2rem 0 0;
        }
        .feature-row { display: flex; gap: 0.65rem; flex-wrap: wrap; margin-top: 1.4rem; }
        .feature-pill {
            padding: 0.55rem 0.85rem; border-radius: 999px;
            background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.10);
            color: #dce4ff; font-size: 0.86rem;
        }
        div[data-testid="stTabs"] button { font-weight: 800; font-size: 1rem; }
        div[data-baseweb="tab-list"] { gap: 0.5rem; }
        button[kind="primary"] { border-radius: 12px; font-weight: 800; }
        .stDownloadButton button { width: 100%; border-radius: 12px; }
        div[data-testid="stFileUploader"] { border-radius: 16px; }
        textarea { border-radius: 14px !important; }
        footer { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource(show_spinner="Loading Whisper model...")
def load_whisper_model(model_name: str):
    return whisper.load_model(model_name)


def save_uploaded_audio(uploaded_file) -> str:
    suffix = Path(uploaded_file.name).suffix if getattr(uploaded_file, "name", None) else ".wav"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        temp_file.write(uploaded_file.getbuffer())
        return temp_file.name


def transcribe_audio(audio_source, model_name: str, language_code: str | None) -> tuple[str, str]:
    temp_path = save_uploaded_audio(audio_source)
    try:
        model = load_whisper_model(model_name)
        options = {"fp16": False}
        if language_code:
            options["language"] = language_code
        result = model.transcribe(temp_path, **options)
        return result.get("text", "").strip(), result.get("language", language_code or "unknown")
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


def text_to_speech(text: str, language_code: str, slow: bool) -> bytes:
    output = BytesIO()
    gTTS(text=text, lang=language_code, slow=slow).write_to_fp(output)
    return output.getvalue()


st.markdown(
    """
    <section class="hero">
        <div class="eyebrow">Bilingual Speech Intelligence</div>
        <h1>Sawt<span>AI</span></h1>
        <p>
            Convert Arabic and English audio into editable text, then turn written content
            back into natural speech through one clean browser-based workspace.
        </p>
        <div class="feature-row">
            <span class="feature-pill">Speech Recognition</span>
            <span class="feature-pill">Text-to-Speech</span>
            <span class="feature-pill">Arabic & English</span>
            <span class="feature-pill">Audio Recording</span>
            <span class="feature-pill">Downloadable Results</span>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

speech_tab, tts_tab, about_tab = st.tabs(["🎙️ Speech to Text", "🔊 Text to Speech", "✨ About SawtAI"])

with speech_tab:
    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown("### Add your audio")
        source_type = st.radio(
            "Audio source",
            ["Upload a file", "Record now"],
            horizontal=True,
            label_visibility="collapsed",
        )

        if source_type == "Upload a file":
            audio_source = st.file_uploader(
                "Upload WAV, MP3, M4A, MP4, MPEG, or MPGA audio",
                type=["wav", "mp3", "m4a", "mp4", "mpeg", "mpga"],
            )
        else:
            audio_source = st.audio_input("Record your voice")

        language_name = st.selectbox(
            "Spoken language",
            list(LANGUAGE_OPTIONS.keys()),
            index=0,
            help="Choose Auto Detect when the recording language is unknown.",
        )
        model_name = st.selectbox(
            "Whisper model",
            ["tiny", "base", "small"],
            index=1,
            help="Tiny is faster. Small is more accurate but needs more memory.",
        )
        transcribe_clicked = st.button("Transcribe audio", type="primary", use_container_width=True)

    with right:
        st.markdown("### Transcription")
        if "transcription" not in st.session_state:
            st.session_state.transcription = ""

        if transcribe_clicked:
            if audio_source is None:
                st.warning("Upload or record an audio clip first.")
            else:
                with st.spinner("Listening and converting speech into text..."):
                    try:
                        text, detected_language = transcribe_audio(
                            audio_source,
                            model_name,
                            LANGUAGE_OPTIONS[language_name],
                        )
                        st.session_state.transcription = text
                        st.session_state.detected_language = detected_language
                    except Exception as error:
                        st.error(f"Transcription failed: {error}")

        transcription = st.text_area(
            "Editable transcription",
            value=st.session_state.transcription,
            height=320,
            placeholder="Your transcription will appear here...",
        )
        st.session_state.transcription = transcription

        if transcription:
            metric_1, metric_2 = st.columns(2)
            metric_1.metric("Detected language", str(st.session_state.get("detected_language", "unknown")).upper())
            metric_2.metric("Word count", len(transcription.split()))
            st.download_button(
                "Download transcription",
                data=transcription.encode("utf-8"),
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
        )

    with right:
        st.markdown("### Voice settings")
        tts_language_name = st.selectbox("Output language", ["Arabic", "English"], index=0, key="tts_language")
        slow_voice = st.toggle("Slower speaking speed", value=False)
        create_audio_clicked = st.button("Generate speech", type="primary", use_container_width=True)

        if create_audio_clicked:
            if not tts_text.strip():
                st.warning("Enter some text first.")
            else:
                with st.spinner("Generating speech..."):
                    try:
                        language_code = "ar" if tts_language_name == "Arabic" else "en"
                        st.session_state.generated_audio = text_to_speech(tts_text.strip(), language_code, slow_voice)
                    except Exception as error:
                        st.error(f"Speech generation failed: {error}")

        audio_bytes = st.session_state.get("generated_audio")
        if audio_bytes:
            st.audio(audio_bytes, format="audio/mp3")
            st.download_button(
                "Download MP3",
                data=audio_bytes,
                file_name="sawtai-speech.mp3",
                mime="audio/mpeg",
                use_container_width=True,
            )

with about_tab:
    st.markdown(
        """
        ### One workspace for speech and text

        SawtAI combines two complementary audio-intelligence workflows:

        - **Speech to Text:** Upload or record Arabic and English audio and convert it into editable text using Whisper.
        - **Text to Speech:** Turn written Arabic or English content into downloadable MP3 audio.
        - **Practical output:** Edit, copy, listen to, and download results directly from the browser.

        ### Technologies

        `Python` · `Streamlit` · `OpenAI Whisper` · `gTTS` · `FFmpeg`
        """
    )

st.markdown(
    '<p style="text-align:center;color:#8f9ab6;margin-top:3rem;">SawtAI · Arabic and English Speech & Text Converter</p>',
    unsafe_allow_html=True,
)

from __future__ import annotations

import streamlit as st

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

st.session_state.setdefault("transcription", "")
st.session_state.setdefault("detected_language", "")
st.session_state.setdefault("generated_audio", None)

st.markdown(
    """
    <section class="hero">
        <div class="eyebrow">Bilingual Speech Intelligence</div>
        <h1>Sawt<span>AI</span></h1>
        <p>
            Convert Arabic and English speech into editable text, then transform written
            content back into downloadable audio through one clean browser-based workspace.
        </p>
        <div class="feature-row">
            <span class="feature-pill">Speech Recognition</span>
            <span class="feature-pill">Text-to-Speech</span>
            <span class="feature-pill">Arabic & English</span>
            <span class="feature-pill">Browser Recording</span>
            <span class="feature-pill">Downloadable Results</span>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

speech_tab, tts_tab, about_tab = st.tabs(
    ["🎙️ Speech to Text", "🔊 Text to Speech", "✨ About SawtAI"]
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

with about_tab:
    st.markdown(
        """
        ### One workspace for speech and text

        SawtAI is a bilingual speech-processing application developed for Arabic and English.

        - **Speech to Text:** Upload or record audio and convert it into editable text.
        - **Text to Speech:** Turn written content into downloadable MP3 audio.
        - **Model Control:** Choose between Tiny, Base, and Small Whisper models.
        - **Practical Outputs:** Edit, listen to, and download results directly from the browser.

        ### Technologies

        `Python` · `Streamlit` · `OpenAI Whisper` · `gTTS` · `FFmpeg`
        """
    )

st.markdown(
    '<p class="footer-note">SawtAI · Arabic and English Speech & Text Converter</p>',
    unsafe_allow_html=True,
)

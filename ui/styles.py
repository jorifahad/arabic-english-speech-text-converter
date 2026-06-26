import streamlit as st

def apply_styles() -> None:
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
                color: #8b82ff;
                font-size: 0.82rem;
                font-weight: 800;
                letter-spacing: 0.18em;
                text-transform: uppercase;
                margin-bottom: 0.7rem;
            }
            .hero h1 {
                color: #ffffff;
                font-size: clamp(2.5rem, 6vw, 5rem);
                line-height: 0.98;
                margin: 0;
                letter-spacing: -0.05em;
            }
            .hero h1 span {
                background: linear-gradient(90deg, #8d7cff, #42d9ff);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            .hero p {
                color: #b9c3dc;
                font-size: 1.08rem;
                line-height: 1.8;
                max-width: 780px;
                margin: 1.2rem 0 0;
            }
            .feature-row { display: flex; gap: 0.65rem; flex-wrap: wrap; margin-top: 1.4rem; }
            .feature-pill {
                padding: 0.55rem 0.85rem;
                border-radius: 999px;
                background: rgba(255,255,255,0.06);
                border: 1px solid rgba(255,255,255,0.10);
                color: #dce4ff;
                font-size: 0.86rem;
            }
            div[data-testid="stTabs"] button { font-weight: 800; font-size: 1rem; }
            div[data-baseweb="tab-list"] { gap: 0.5rem; }
            button[kind="primary"] { border-radius: 12px; font-weight: 800; }
            .stDownloadButton button { width: 100%; border-radius: 12px; }
            textarea { border-radius: 14px !important; }
            .footer-note { text-align: center; color: #8f9ab6; font-size: 0.88rem; margin-top: 3rem; }
            footer { visibility: hidden; }
        </style>
        """,
        unsafe_allow_html=True,
    )

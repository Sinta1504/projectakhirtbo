"""
app.py - Streamlit version of MarketBot

This file is designed for Streamlit Community Cloud. The original Flask version
has been kept as app_flask.py for backup or deployment to Flask hosting.
"""

from __future__ import annotations

import streamlit as st

from FSM import OPTIONS, transition
from engine import generate_recommendations

PROMPTS = {
    "q0": "Selamat datang! Saya adalah MarketBot — konsultan pemasaran digital Anda.",
    "q1": "Pertama, apa jenis usaha Anda? Pilih kategori yang paling sesuai:",
    "q2": "Siapa target usia pelanggan utama bisnis Anda?",
    "q3": "Apa profesi target pelanggan Anda?",
    "q4": "Bagaimana gaya hidup target pelanggan Anda?",
    "q5": "Berapa anggaran promosi yang Anda siapkan per bulan?",
    "q6": "Apa tujuan utama pemasaran Anda saat ini?",
    "q7": "Di mana lokasi target pasar Anda?",
    "q8": "Sudah berapa lama bisnis Anda berjalan?",
    "q9": "Media promosi apa yang sudah pernah Anda gunakan?",
    "q10": "Seberapa sering Anda melakukan promosi?",
    "q11": "Bagaimana tingkat persaingan di industri Anda?",
    "q12": "Siapa jenis pelanggan utama bisnis Anda?",
    "q19": "Analisis selesai! Berikut rekomendasi strategi pemasaran untuk bisnis Anda.",
    "q20": "Apakah Anda ingin melakukan konsultasi lagi untuk bisnis lain?",
    "q21": "Terima kasih telah menggunakan MarketBot! Semoga strategi ini membantu bisnis Anda berkembang.",
}

STEP_LABELS = {
    "q1": "Jenis Usaha",
    "q2": "Target Usia",
    "q3": "Profesi",
    "q4": "Gaya Hidup",
    "q5": "Anggaran",
    "q6": "Tujuan",
    "q7": "Lokasi",
    "q8": "Tahap Bisnis",
    "q9": "Media Sebelumnya",
    "q10": "Frekuensi",
    "q11": "Kompetisi",
    "q12": "Jenis Pelanggan",
}

KEY_MAP = {
    "q1": "jenis_usaha",
    "q2": "target_usia",
    "q3": "target_profesi",
    "q4": "gaya_hidup",
    "q5": "anggaran",
    "q6": "tujuan",
    "q7": "lokasi",
    "q8": "tahap_bisnis",
    "q9": "media_sebelumnya",
    "q10": "frekuensi",
    "q11": "tingkat_kompetisi",
    "q12": "jenis_pelanggan",
}

QUESTION_STATES = list(KEY_MAP.keys())
TOTAL_STEPS = len(QUESTION_STATES)


st.set_page_config(
    page_title="MarketBot - Konsultan Pemasaran Digital",
    page_icon="📈",
    layout="wide",
)

st.markdown(
    """
    <style>
    .block-container { padding-top: 2rem; padding-bottom: 3rem; }
    .hero-card {
        padding: 1.4rem 1.6rem;
        border: 1px solid rgba(148, 163, 184, .3);
        border-radius: 18px;
        background: linear-gradient(135deg, rgba(79,70,229,.08), rgba(6,182,212,.08));
        margin-bottom: 1.2rem;
    }
    .small-muted { color: #64748b; font-size: .95rem; }
    .answer-card {
        padding: .8rem 1rem;
        border-radius: 12px;
        border: 1px solid rgba(148, 163, 184, .25);
        background: rgba(248,250,252,.65);
        margin-bottom: .55rem;
    }
    .result-box {
        padding: 1rem 1.2rem;
        border-radius: 14px;
        border: 1px solid rgba(148, 163, 184, .35);
        background: rgba(255,255,255,.7);
        margin-bottom: 1rem;
    }
    div[data-testid="stButton"] > button {
        width: 100%;
        border-radius: 10px;
        min-height: 2.7rem;
        white-space: normal;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def init_state() -> None:
    """Initialize Streamlit session state."""
    defaults = {
        "state": "q0",
        "data": {},
        "history": [],
        "recommendations": None,
        "started": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def restart() -> None:
    """Reset consultation to the first real question."""
    st.session_state.state = "q1"
    st.session_state.data = {}
    st.session_state.history = []
    st.session_state.recommendations = None
    st.session_state.started = True


def finish_consultation() -> None:
    """Generate recommendations after the last question."""
    st.session_state.recommendations = generate_recommendations(st.session_state.data)
    st.session_state.state = "q19"


def handle_answer(state: str, answer: str) -> None:
    """Store answer and move to the next state."""
    if state in KEY_MAP:
        st.session_state.data[KEY_MAP[state]] = answer
        st.session_state.history.append((STEP_LABELS[state], answer))

    next_state = transition(state, answer)

    if next_state in {"q13", "q14", "q15", "q16", "q17", "q18", "q19"}:
        finish_consultation()
    else:
        st.session_state.state = next_state


def get_step_number(state: str) -> int:
    if state in QUESTION_STATES:
        return QUESTION_STATES.index(state) + 1
    if state in {"q19", "q20", "q21"}:
        return TOTAL_STEPS
    return 0


def render_header() -> None:
    st.markdown(
        """
        <div class="hero-card">
            <h1 style="margin-bottom:.25rem;">📈 MarketBot</h1>
            <p class="small-muted" style="margin-bottom:0;">
                Sistem rekomendasi strategi pemasaran digital berbasis Finite State Machine.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_history() -> None:
    if not st.session_state.history:
        st.info("Jawaban Anda akan muncul di sini selama proses konsultasi.")
        return

    st.subheader("Ringkasan Jawaban")
    for label, answer in st.session_state.history:
        st.markdown(
            f"""
            <div class="answer-card">
                <strong>{label}</strong><br>
                <span class="small-muted">{answer}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_option_buttons(state: str) -> None:
    options = OPTIONS.get(state)
    if not options:
        return

    if isinstance(options, dict):
        for group, items in options.items():
            with st.expander(group, expanded=(group == next(iter(options)))):
                cols = st.columns(2)
                for index, item in enumerate(items):
                    with cols[index % 2]:
                        if st.button(item, key=f"{state}-{group}-{item}"):
                            handle_answer(state, item)
                            st.rerun()
        return

    cols = st.columns(2)
    for index, item in enumerate(options):
        with cols[index % 2]:
            if st.button(item, key=f"{state}-{item}"):
                handle_answer(state, item)
                st.rerun()


def render_question() -> None:
    state = st.session_state.state
    step = get_step_number(state)

    st.progress(step / TOTAL_STEPS if TOTAL_STEPS else 0)
    st.caption(f"Langkah {step} dari {TOTAL_STEPS}")

    st.subheader(PROMPTS[state])
    render_option_buttons(state)


def render_results() -> None:
    recs = st.session_state.recommendations or generate_recommendations(st.session_state.data)
    st.session_state.recommendations = recs

    st.success(PROMPTS["q19"])

    left, right = st.columns(2)

    with left:
        st.markdown("### 🎯 Strategi Promosi")
        for item in recs["strategi_promosi"]:
            st.markdown(f"- {item}")

        st.markdown("### 📱 Platform Media Sosial")
        for item in recs["platform_medsos"]:
            st.markdown(f"- {item}")

        st.markdown("### 🌟 Influencer Marketing")
        st.markdown(f"- {recs['influencer']}")

    with right:
        st.markdown("### 🎨 Jenis Konten")
        for item in recs["jenis_konten"]:
            st.markdown(f"- {item}")

        st.markdown("### 🎁 Program Promo")
        for item in recs["program_promo"]:
            st.markdown(f"- {item}")

        st.markdown("### 👥 Segmentasi Pasar")
        for key, value in recs["segmentasi"].items():
            st.markdown(f"- **{key}:** {value}")

    st.divider()
    st.subheader(PROMPTS["q20"])
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Ya, konsultasi lagi", key="restart-after-result"):
            restart()
            st.rerun()
    with col2:
        if st.button("Tidak, selesai", key="finish-after-result"):
            st.session_state.state = "q21"
            st.rerun()


def render_finish() -> None:
    st.balloons()
    st.success(PROMPTS["q21"])
    if st.button("Mulai konsultasi baru"):
        restart()
        st.rerun()


def main() -> None:
    init_state()
    render_header()

    if not st.session_state.started:
        col1, col2 = st.columns([1.3, 1])
        with col1:
            st.subheader("Konsultasi strategi pemasaran digital")
            st.write(
                "Jawab 12 pertanyaan singkat, lalu sistem akan menghasilkan rekomendasi "
                "strategi promosi, media sosial, konten, influencer, promo, dan segmentasi pasar."
            )
            if st.button("Mulai Konsultasi Sekarang →", type="primary"):
                restart()
                st.rerun()
        with col2:
            st.info(PROMPTS["q0"])
        return

    main_col, side_col = st.columns([1.7, 1])
    with main_col:
        if st.session_state.state in QUESTION_STATES:
            render_question()
        elif st.session_state.state == "q19":
            render_results()
        else:
            render_finish()

    with side_col:
        render_history()
        if st.button("Reset konsultasi", key="side-reset"):
            restart()
            st.rerun()


if __name__ == "__main__":
    main()

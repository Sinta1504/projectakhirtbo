"""
app.py - Flask Web Server untuk Chatbot Konsultan Pemasaran Digital
"""

from flask import Flask, render_template, request, jsonify, session
from FSM import STATES, OPTIONS, INITIAL_STATE, FINAL_STATE, transition
from engine import generate_recommendations

app = Flask(__name__)
app.secret_key = "tbo_marketing_chatbot_2026_secret"  # Diperlukan untuk session

# ─── QUESTION PROMPTS ─────────────────────────────────────────────────────────
PROMPTS = {
    "q0":  "Selamat datang! 👋 Saya adalah <strong>MarketBot</strong> — konsultan pemasaran digital Anda. Saya akan membantu menemukan strategi terbaik untuk bisnis Anda melalui beberapa pertanyaan singkat.",
    "q1":  "Pertama, <strong>apa jenis usaha Anda?</strong> Pilih kategori yang paling sesuai:",
    "q2":  "Siapa <strong>target usia</strong> pelanggan utama bisnis Anda?",
    "q3":  "Apa <strong>profesi</strong> target pelanggan Anda?",
    "q4":  "Bagaimana <strong>gaya hidup</strong> target pelanggan Anda?",
    "q5":  "Berapa <strong>anggaran promosi</strong> yang Anda siapkan per bulan?",
    "q6":  "Apa <strong>tujuan utama pemasaran</strong> Anda saat ini?",
    "q7":  "Di mana <strong>lokasi target pasar</strong> Anda?",
    "q8":  "Sudah berapa lama bisnis Anda berjalan? (<strong>tahap perkembangan</strong>)",
    "q9":  "Media promosi apa yang <strong>sudah pernah Anda gunakan</strong>?",
    "q10": "Seberapa sering Anda melakukan <strong>promosi</strong>?",
    "q11": "Bagaimana <strong>tingkat persaingan</strong> di industri Anda?",
    "q12": "Siapa <strong>jenis pelanggan utama</strong> bisnis Anda?",
    "q13": "⚙️ Menganalisis strategi promosi terbaik...",
    "q14": "📱 Menentukan platform media sosial optimal...",
    "q15": "🎨 Merancang jenis konten yang tepat...",
    "q16": "🌟 Menganalisis strategi influencer marketing...",
    "q17": "🎁 Menyusun program promosi yang efektif...",
    "q18": "🎯 Melakukan segmentasi pasar...",
    "q19": "✅ Analisis selesai!",
    "q20": "Apakah Anda ingin melakukan <strong>konsultasi lagi</strong> untuk bisnis lain?",
    "q21": "Terima kasih telah menggunakan <strong>MarketBot</strong>! 🎉 Semoga strategi ini membantu bisnis Anda berkembang. Sukses selalu!",
}

STEP_LABELS = {
    "q1": "Jenis Usaha", "q2": "Target Usia", "q3": "Profesi",
    "q4": "Gaya Hidup", "q5": "Anggaran", "q6": "Tujuan",
    "q7": "Lokasi", "q8": "Tahap Bisnis", "q9": "Media Sebelumnya",
    "q10": "Frekuensi", "q11": "Kompetisi", "q12": "Jenis Pelanggan",
}

# Mapping state ke key data (agar konsisten)
KEY_MAP = {
    "q1": "jenis_usaha", "q2": "target_usia", "q3": "target_profesi", "q4": "gaya_hidup",
    "q5": "anggaran", "q6": "tujuan", "q7": "lokasi", "q8": "tahap_bisnis",
    "q9": "media_sebelumnya", "q10": "frekuensi", "q11": "tingkat_kompetisi", "q12": "jenis_pelanggan",
}

# ─── ROUTES ───────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/start", methods=["POST"])
def start():
    session.clear()
    session["state"] = INITIAL_STATE
    session["data"] = {}
    return jsonify({
        "state": INITIAL_STATE,
        "message": PROMPTS["q0"],
        "next_state": "q1",
        "options": _get_options("q1"),
        "next_prompt": PROMPTS["q1"],
        "step": 0,
        "total_steps": 12,
    })

@app.route("/api/message", methods=["POST"])
def message():
    body = request.get_json()
    user_input = body.get("input", "").strip()
    current_state = session.get("state", INITIAL_STATE)
    data = session.get("data", {})

    # 1. Store user answer
    if current_state in KEY_MAP:
        data[KEY_MAP[current_state]] = user_input
        session["data"] = data

    # 2. Transition state
    next_state = transition(current_state, user_input)
    session["state"] = next_state

    # 3. Analysis states (q13-q18): Auto-advance logic
    if next_state in ["q13", "q14", "q15", "q16", "q17", "q18"]:
        # Generate rekomendasi saat memasuki fase analisis
        recs = generate_recommendations(data)
        session["recs"] = recs
        
        # Langsung set state ke q19 agar frontend menampilkan hasil
        session["state"] = "q19"
        
        return jsonify({
            "state": "q19",
            "message": PROMPTS["q19"],
            "recommendations": recs,
            "options": OPTIONS.get("q20"),
            "next_prompt": PROMPTS["q20"],
            "step": 13,
            "total_steps": 13,
            "type": "result",
        })

    # 4. Result State (q19)
    if next_state == "q19":
        # Fallback jika langsung masuk sini tanpa lewat analisis (seharusnya tidak terjadi)
        recs = session.get("recs", generate_recommendations(data))
        return jsonify({
            "state": "q19",
            "message": PROMPTS["q19"],
            "recommendations": recs,
            "options": OPTIONS.get("q20"),
            "next_prompt": PROMPTS["q20"],
            "step": 13,
            "total_steps": 13,
            "type": "result",
        })

    # 5. Repeat State (q20)
    if next_state == "q20":
        return jsonify({
            "state": "q20",
            "message": PROMPTS["q20"],
            "options": OPTIONS["q20"],
            "step": _state_to_step(next_state),
            "total_steps": 13,
            "type": "question",
        })

    # 6. Final State (q21)
    if next_state == FINAL_STATE:
        return jsonify({
            "state": "q21",
            "message": PROMPTS["q21"],
            "type": "end",
        })

    # 7. Normal Question State (q1 - q12)
    return jsonify({
        "state": next_state,
        "message": PROMPTS.get(next_state, ""),
        "options": _get_options(next_state),
        "step": _state_to_step(next_state),
        "total_steps": 12,
        "type": "question",
        "label": STEP_LABELS.get(next_state, ""),
    })

@app.route("/api/restart", methods=["POST"])
def restart():
    session.clear()
    session["state"] = "q1"
    session["data"] = {}
    return jsonify({
        "state": "q1",
        "message": PROMPTS["q1"],
        "options": _get_options("q1"),
        "step": 1,
        "total_steps": 12,
        "type": "question",
    })

# ─── HELPERS ──────────────────────────────────────────────────────────────────

def _get_options(state: str):
    opts = OPTIONS.get(state)
    if isinstance(opts, dict):
        # Flatten grouped options (q1)
        flat = []
        for group, items in opts.items():
            flat.append({"group": group, "items": items})
        return flat
    return opts  # list or None

def _state_to_step(state: str) -> int:
    mapping = {
        "q1":1, "q2":2, "q3":3, "q4":4, "q5":5, "q6":6,
        "q7":7, "q8":8, "q9":9, "q10":10, "q11":11, "q12":12,
        "q20":13
    }
    return mapping.get(state, 0)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
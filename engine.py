"""
engine.py - Mesin Rekomendasi Pemasaran Digital
Menghasilkan rekomendasi berdasarkan kombinasi input user
"""

# ─── MAPPING TABEL ────────────────────────────────────────────────────────────

# Platform media sosial berdasarkan usia target
PLATFORM_BY_AGE = {
    "Anak-anak (5–8 th)": ["YouTube Kids", "TikTok (parental)"],
    "Anak-anak (9–12 th)": ["YouTube", "TikTok"],
    "Remaja awal (13–15 th)": ["TikTok", "Instagram", "YouTube"],
    "Remaja (16–18 th)": ["TikTok", "Instagram", "YouTube", "Twitter/X"],
    "Mahasiswa awal (19–21 th)": ["Instagram", "TikTok", "Twitter/X", "YouTube"],
    "Mahasiswa akhir (22–24 th)": ["Instagram", "LinkedIn", "TikTok", "YouTube"],
    "Dewasa muda (25–29 th)": ["Instagram", "LinkedIn", "Facebook", "YouTube"],
    "Dewasa muda (30–34 th)": ["Facebook", "Instagram", "LinkedIn", "WhatsApp Business"],
    "Dewasa (35–39 th)": ["Facebook", "WhatsApp Business", "LinkedIn"],
    "Dewasa (40–44 th)": ["Facebook", "WhatsApp Business", "YouTube"],
    "Pra-lansia (45–49 th)": ["Facebook", "WhatsApp Business"],
    "Pra-lansia (50–54 th)": ["Facebook", "WhatsApp Business", "YouTube"],
    "Lansia muda (55–64 th)": ["Facebook", "WhatsApp Business"],
    "Lansia (65+ th)": ["Facebook", "WhatsApp Business"],
    "Semua usia": ["Instagram", "TikTok", "Facebook", "YouTube", "WhatsApp Business"],
}

# Strategi promosi berdasarkan anggaran
STRATEGY_BY_BUDGET = {
    "< Rp250.000": [
        "Fokus pada konten organik media sosial",
        "Manfaatkan WhatsApp Business secara gratis",
        "Gunakan Google My Business untuk visibilitas lokal",
        "Buat konten UGC (User Generated Content) dari pelanggan",
    ],
    "Rp250.000–500.000": [
        "Iklan Instagram/Facebook boosting sederhana",
        "Paid promote di akun lokal yang relevan",
        "Konten organik + 1 paid post per minggu",
    ],
    "Rp500.001–1.000.000": [
        "Facebook & Instagram Ads dengan targeting spesifik",
        "Kolaborasi micro-influencer lokal",
        "Konten video pendek TikTok / Reels",
    ],
    "Rp1–2,5 juta": [
        "Multi-platform ads (Meta + TikTok)",
        "Google Ads untuk search intent",
        "Email marketing campaign",
        "Micro-influencer 2–3 akun",
    ],
    "Rp2,5–5 juta": [
        "Full-funnel marketing (awareness → conversion)",
        "Influencer marketing nano/micro",
        "Retargeting campaign",
        "A/B testing iklan",
    ],
    "Rp5–10 juta": [
        "Influencer marketing kategori mid-tier",
        "Google Ads + Meta Ads terintegrasi",
        "Landing page khusus kampanye",
        "Video production untuk konten iklan",
    ],
    "Rp10–25 juta": [
        "Brand campaign multi-channel",
        "Kolaborasi influencer 5–10 akun",
        "SEO + Content marketing",
        "Podcast advertising",
    ],
    "Rp25–50 juta": [
        "Campaign terintegrasi online + offline",
        "Macro-influencer marketing",
        "Event digital / webinar berbayar",
        "PR digital di media online",
    ],
    "Rp50–100 juta": [
        "Brand ambassador jangka panjang",
        "Multi-channel attribution tracking",
        "Native advertising di media nasional",
        "Programmatic advertising",
    ],
    "Rp100–250 juta": [
        "Celebrity endorsement",
        "TV/radio spot + digital integration",
        "Sponsorship event nasional",
        "Full agency management",
    ],
    "> Rp250 juta": [
        "National brand campaign",
        "360° integrated marketing",
        "Celebrity brand ambassador",
        "Mass media advertising",
    ],
    "Belum menentukan": [
        "Mulai dengan strategi organik tanpa biaya",
        "Tentukan ROI target sebelum berinvestasi",
        "Trial kecil dengan budget Rp100–200k untuk test market",
    ],
}

# Jenis konten berdasarkan gaya hidup target
CONTENT_BY_LIFESTYLE = {
    "Pecinta olahraga": ["Video workout/tips olahraga", "Before-after transformation", "Challenge konten"],
    "Pengguna teknologi aktif": ["Review produk/tutorial", "Tech tips", "Infografis data"],
    "Pecinta traveling": ["Konten wisata lokal", "Tips perjalanan", "Foto destinasi"],
    "Pecinta kuliner": ["Food photography", "Behind-the-scenes masak", "Review & rekomendasi"],
    "Pecinta fashion": ["Outfit of the day (OOTD)", "Style tips", "Fashion haul"],
    "Orang tua muda": ["Parenting tips", "Produk keluarga", "Konten edukatif anak"],
    "Komunitas hobi": ["Tutorial hobi", "Community showcase", "Event komunitas"],
    "Peduli kesehatan": ["Tips kesehatan", "Konten edukatif medis", "Testimoni produk sehat"],
    "Pencari promo/diskon": ["Flash sale announcement", "Voucher & promo", "Perbandingan harga"],
    "Pekerja mobilitas tinggi": ["Quick tips & hack", "Konten singkat 15–30 detik", "Podcast"],
}

# Influencer tier berdasarkan anggaran dan kompetisi
INFLUENCER_BY_BUDGET = {
    "< Rp250.000": "Tidak direkomendasikan (gunakan kolaborasi barter)",
    "Rp250.000–500.000": "Nano-influencer (1K–10K followers) – barter/Rp50–200rb",
    "Rp500.001–1.000.000": "Nano-influencer – Rp200–500rb per post",
    "Rp1–2,5 juta": "Micro-influencer (10K–100K) – Rp500rb–2jt per post",
    "Rp2,5–5 juta": "Micro-influencer – Rp2–5jt, 1–2 kolaborasi",
    "Rp5–10 juta": "Mid-tier influencer (100K–500K) – Rp5–10jt",
    "Rp10–25 juta": "Mid-tier, 2–3 akun – Rp5–10jt per akun",
    "Rp25–50 juta": "Macro-influencer (500K–1M) – Rp20–50jt",
    "Rp50–100 juta": "Macro/Mega influencer – Rp50–100jt",
    "Rp100–250 juta": "Mega-influencer/Selebriti – Rp100–250jt",
    "> Rp250 juta": "Celebrity brand ambassador jangka panjang",
    "Belum menentukan": "Mulai dengan nano-influencer barter untuk test market",
}

# Program promo berdasarkan tujuan pemasaran
PROMO_BY_GOAL = {
    "Meningkatkan penjualan": ["Flash sale 24 jam", "Bundle produk hemat", "Cashback pembelian pertama"],
    "Meningkatkan brand awareness": ["Giveaway challenge", "Konten viral campaign", "Hashtag brand"],
    "Menambah followers": ["Follow & share contest", "Giveaway berhadiah", "Collab dengan kreator lain"],
    "Memperkenalkan produk baru": ["Early bird discount", "Free trial/sample", "Pre-order exclusive"],
    "Meningkatkan loyalitas": ["Loyalty point program", "Member exclusive deal", "Birthday promo"],
    "Menjangkau pasar baru": ["Ads targeting baru", "Influencer di segmen baru", "Event/pameran"],
    "Menghabiskan stok lama": ["Clearance sale", "Bundle stok lama+baru", "Diskon bertingkat"],
    "Meningkatkan engagement": ["Kuis interaktif", "Polling & survey", "Challenge konten"],
    "Meningkatkan traffic website": ["Blog SEO + CTA", "Google Ads search", "Email newsletter"],
    "Mendapatkan leads": ["Free ebook/webinar", "Formulir landing page", "Lead magnet promo"],
    "Meningkatkan reservasi": ["Early booking discount", "Paket spesial weekend", "Referral program"],
    "Mengumpulkan data pelanggan": ["Survey berhadiah", "Loyalty card digital", "Newsletter opt-in"],
    "Meningkatkan repeat order": ["Subscription program", "Reminder notifikasi", "Reward pelanggan setia"],
    "Memperkuat citra merek": ["Storytelling brand", "CSR campaign", "Behind-the-scenes konten"],
    "Mengungguli kompetitor": ["Competitive pricing", "Unique selling proposition campaign", "Comparative ads"],
    "Meningkatkan kunjungan toko": ["Check-in promo", "Geo-targeting ads", "Event toko fisik"],
    "Meningkatkan konversi online": ["Retargeting cart abandonment", "Social proof / review", "One-click checkout promo"],
    "Mengedukasi pelanggan": ["Tutorial konten seri", "Webinar gratis", "FAQ campaign"],
    "Menyiapkan bisnis baru": ["Soft launch campaign", "Waitlist exclusive", "Teaser content 2–4 minggu"],
    "Mempertahankan pangsa pasar": ["Customer retention program", "Competitive monitoring", "Brand defense campaign"],
}

# ─── MAIN RECOMMENDATION ENGINE ───────────────────────────────────────────────

def generate_recommendations(data: dict) -> dict:
    """
    data keys (sesuai state q1–q12):
        jenis_usaha, target_usia, target_profesi, gaya_hidup,
        anggaran, tujuan, lokasi, tahap_bisnis, media_sebelumnya,
        frekuensi, tingkat_kompetisi, jenis_pelanggan
    """
    # Ambil data dengan default value jika kosong
    usia      = data.get("target_usia", "Semua usia")
    anggaran  = data.get("anggaran", "Belum menentukan")
    gaya_hidup= data.get("gaya_hidup", "")
    tujuan    = data.get("tujuan", "Meningkatkan penjualan")
    kompetisi = data.get("tingkat_kompetisi", "Sedang")
    tahap     = data.get("tahap_bisnis", "Baru memulai")
    usaha     = data.get("jenis_usaha", "")

    # q13 – Strategi Promosi
    strategi = list(STRATEGY_BY_BUDGET.get(anggaran, STRATEGY_BY_BUDGET["Belum menentukan"]))
    
    # Tambahkan logika tambahan berdasarkan kompetisi & tahap bisnis
    if kompetisi in ["Tinggi", "Sangat tinggi"]:
        strategi.append("Lakukan competitive analysis mingguan")
        strategi.append("Fokus pada diferensiasi unik produk/jasa Anda")
    
    if tahap == "Baru memulai":
        strategi.insert(0, "Bangun profil media sosial yang konsisten dan profesional terlebih dahulu")

    # q14 – Platform Media Sosial
    platform = list(PLATFORM_BY_AGE.get(usia, ["Instagram", "Facebook", "WhatsApp Business"]))

    # q15 – Jenis Konten
    konten = list(CONTENT_BY_LIFESTYLE.get(gaya_hidup, [
        "Foto produk berkualitas tinggi",
        "Video testimoni pelanggan",
        "Behind-the-scenes proses bisnis",
        "Tips & informasi edukatif seputar industri",
    ]))
    konten += [
        "Konten seasonal (hari besar, momen nasional)",
        "User Generated Content (UGC) dari pelanggan",
    ]

    # q16 – Influencer
    influencer = INFLUENCER_BY_BUDGET.get(anggaran, "Mulai dengan nano-influencer barter")

    # q17 – Program Promo
    promo = list(PROMO_BY_GOAL.get(tujuan, ["Flash sale", "Promo loyalty pelanggan"]))

    # q18 – Segmentasi Pasar
    segmentasi = {
        "Jenis Usaha": usaha,
        "Target Usia": usia,
        "Profesi": data.get("target_profesi", "-"),
        "Gaya Hidup": gaya_hidup,
        "Lokasi": data.get("lokasi", "-"),
        "Tahap Bisnis": tahap,
        "Jenis Pelanggan": data.get("jenis_pelanggan", "-"),
    }

    return {
        "strategi_promosi": strategi,
        "platform_medsos": platform,
        "jenis_konten": konten,
        "influencer": influencer,
        "program_promo": promo,
        "segmentasi": segmentasi,
    }
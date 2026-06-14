"""
FSM.py - Finite State Machine untuk Chatbot Konsultan Pemasaran Digital
Struktur FSM dengan 22 state (q0 - q21)
"""

# ─── STATE DEFINITIONS ────────────────────────────────────────────────────────
STATES = {
    "q0":  "Mulai",
    "q1":  "Pilih Jenis Usaha",
    "q2":  "Pilih Target Usia",
    "q3":  "Pilih Target Profesi",
    "q4":  "Pilih Target Gaya Hidup",
    "q5":  "Pilih Anggaran Promosi",
    "q6":  "Pilih Tujuan Pemasaran",
    "q7":  "Pilih Lokasi Target",
    "q8":  "Pilih Tahap Bisnis",
    "q9":  "Pilih Media Promosi Sebelumnya",
    "q10": "Pilih Frekuensi Promosi",
    "q11": "Pilih Tingkat Kompetisi",
    "q12": "Pilih Jenis Pelanggan",
    "q13": "Analisis Strategi Promosi",
    "q14": "Analisis Media Sosial",
    "q15": "Analisis Jenis Konten",
    "q16": "Analisis Influencer Marketing",
    "q17": "Analisis Program Promo",
    "q18": "Analisis Segmentasi Pasar",
    "q19": "Ringkasan Hasil Konsultasi",
    "q20": "Konsultasi Lagi?",
    "q21": "Selesai",
}

INITIAL_STATE = "q0"
FINAL_STATE   = "q21"

# ─── INPUT OPTIONS PER STATE ──────────────────────────────────────────────────
OPTIONS = {
    "q1": {
        "Makanan & Minuman": ["Restoran","Warung makan","Coffee shop","Bakery","Toko kue","Catering","Minuman kekinian","Frozen food"],
        "Fashion & Kecantikan": ["Toko pakaian pria","Toko pakaian wanita","Toko pakaian anak","Hijab & muslim fashion","Toko sepatu","Toko tas","Toko aksesoris","Skincare","Kosmetik","Klinik kecantikan","Salon","Barbershop"],
        "Jasa": ["Fotografi","Videografi","Desain grafis","Percetakan","Event organizer","Wedding organizer","Cleaning service","Konsultan bisnis","Konsultan pajak","Jasa penerjemah"],
        "Pendidikan": ["Bimbingan belajar","Kursus bahasa","Kursus komputer","Pelatihan kerja","Kursus musik"],
        "Teknologi": ["Software house","Pengembang aplikasi","Produk digital","Toko komputer","Servis komputer"],
        "Lainnya": ["Laundry","Toko furniture","Toko dekorasi rumah","Toko tanaman hias","Bengkel motor","Bengkel mobil","Cuci kendaraan","Rental kendaraan","Pet shop","Agen travel"],
    },
    "q2": ["Anak-anak (5–8 th)","Anak-anak (9–12 th)","Remaja awal (13–15 th)","Remaja (16–18 th)",
           "Mahasiswa awal (19–21 th)","Mahasiswa akhir (22–24 th)","Dewasa muda (25–29 th)",
           "Dewasa muda (30–34 th)","Dewasa (35–39 th)","Dewasa (40–44 th)",
           "Pra-lansia (45–49 th)","Pra-lansia (50–54 th)","Lansia muda (55–64 th)",
           "Lansia (65+ th)","Semua usia"],
    "q3": ["Pelajar","Mahasiswa","Pegawai negeri","Karyawan swasta","Wirausaha","Freelancer",
           "Ibu rumah tangga","Guru dan dosen","Tenaga kesehatan","Pekerja lapangan","Pensiunan","Semua profesi"],
    "q4": ["Pecinta olahraga","Pengguna teknologi aktif","Pecinta traveling","Pecinta kuliner",
           "Pecinta fashion","Orang tua muda","Komunitas hobi","Peduli kesehatan",
           "Pencari promo/diskon","Pekerja mobilitas tinggi"],
    "q5": ["< Rp250.000","Rp250.000–500.000","Rp500.001–1.000.000","Rp1–2,5 juta",
           "Rp2,5–5 juta","Rp5–10 juta","Rp10–25 juta","Rp25–50 juta",
           "Rp50–100 juta","Rp100–250 juta","> Rp250 juta","Belum menentukan"],
    "q6": ["Meningkatkan penjualan","Meningkatkan brand awareness","Menambah followers",
           "Memperkenalkan produk baru","Meningkatkan loyalitas","Menjangkau pasar baru",
           "Menghabiskan stok lama","Meningkatkan engagement","Meningkatkan traffic website",
           "Mendapatkan leads","Meningkatkan reservasi","Mengumpulkan data pelanggan",
           "Meningkatkan repeat order","Memperkuat citra merek","Mengungguli kompetitor",
           "Meningkatkan kunjungan toko","Meningkatkan konversi online","Mengedukasi pelanggan",
           "Menyiapkan bisnis baru","Mempertahankan pangsa pasar"],
    "q7": ["Lingkungan sekitar usaha","Kecamatan","Kabupaten/Kota","Provinsi",
           "Nasional","Asia Tenggara","Internasional","Belum menentukan"],
    "q8": ["Baru memulai","< 1 tahun","1–3 tahun","3–5 tahun","> 5 tahun","Franchise/cabang banyak"],
    "q9": ["Belum pernah promosi","Instagram","TikTok","Facebook","WhatsApp Business",
           "Marketplace","Website","Google Ads","Influencer marketing","Promosi offline"],
    "q10": ["Setiap hari","2–3x seminggu","Seminggu sekali","Sebulan sekali",
            "Saat momen tertentu","Belum pernah promosi"],
    "q11": ["Sangat rendah","Rendah","Sedang","Tinggi","Sangat tinggi"],
    "q12": ["Pelanggan baru","Pelanggan tetap","Pelanggan loyal","Sensitif terhadap harga",
            "Pelanggan premium","Pembeli impulsif","Pelanggan korporat (B2B)","Semua pelanggan"],
    "q20": ["Ya, konsultasi lagi","Tidak, selesai"],
}

# ─── TRANSITION TABLE ─────────────────────────────────────────────────────────
# Format: (current_state, input_type) -> next_state
# input_type: "answer" = jawaban user, "next" = lanjut otomatis

def transition(state: str, _input: str) -> str:
    """Return next state given current state and user input."""
    flow = ["q0","q1","q2","q3","q4","q5","q6","q7","q8","q9","q10","q11","q12",
            "q13","q14","q15","q16","q17","q18","q19","q20"]
    if state in flow:
        idx = flow.index(state)
        if idx + 1 < len(flow):
            return flow[idx + 1]
    
    # Logic khusus untuk q20 (Restart atau Selesai)
    if state == "q20":
        if _input == "Ya, konsultasi lagi":
            return "q1"
        return "q21"
    
    # Default fallback jika state tidak dikenali
    return "q21"
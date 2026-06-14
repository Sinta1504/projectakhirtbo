# MarketBot - Project Akhir TBO

Aplikasi rekomendasi strategi pemasaran digital berbasis Finite State Machine.

## Deploy ke Streamlit Community Cloud

1. Upload semua file ke GitHub.
2. Pastikan file utama adalah `app.py`.
3. Deploy di Streamlit Cloud dengan main file path: `app.py`.

## File penting

- `app.py` = versi Streamlit untuk streamlit.app
- `FSM.py` = definisi state, opsi, dan transisi FSM
- `engine.py` = mesin rekomendasi pemasaran digital
- `app_flask.py` = backup versi Flask lama
- `requirements.txt` = dependency project

## Catatan

Versi sebelumnya gagal di Streamlit Cloud karena `app.py` adalah Flask app dan dependency `flask` tidak tersedia. Versi ini sudah disesuaikan agar langsung berjalan di Streamlit Cloud.

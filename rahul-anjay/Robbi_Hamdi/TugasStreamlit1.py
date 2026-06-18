import streamlit as st
from collections import Counter
import re

st.title("Word Count - Komentar Sosial Media")
st.caption("Masukkan komentar, lihat frekuensi tiap kata.")

# Input komentar
komentar = st.text_area(
    "Masukkan komentar (satu baris = satu komentar)",
    height=150,
    value="""produk ini bagus banget suka banget
pengiriman cepat produk bagus
kualitas bagus harga murah
suka produk ini murah dan bagus
pengiriman lambat tapi produk bagus
harga murah kualitas oke
bagus banget recommended deh""",
)

# Stopword sederhana bahasa Indonesia
STOPWORDS = {"dan", "di", "ke", "yang", "ini", "itu", "tapi", "juga", "deh", "oke"}

# Opsi filter stopword
hapus_stopword = st.checkbox("Hapus stopword umum", value=True)

st.divider()

# ── Proses teks ───────────────────────────────────────────────────────────────
# Ubah ke huruf kecil, ambil hanya kata (huruf), pisah jadi token
semua_kata = re.findall(r"\b[a-zA-Z]+\b", komentar.lower())

if hapus_stopword:
    semua_kata = [k for k in semua_kata if k not in STOPWORDS]

if not semua_kata:
    st.warning("Belum ada kata untuk dihitung.")
    st.stop()

# Hitung frekuensi — Counter otomatis membuat dict {kata: frekuensi}
frekuensi = Counter(semua_kata)

# Urutkan dari yang paling sering muncul
urut = sorted(frekuensi.items(), key=lambda x: x[1], reverse=True)

# ── Tampilkan tabel kata → frekuensi ─────────────────────────────────────────
st.subheader("Frekuensi Tiap Kata")

# Top-N slider
top_n = st.slider(
    "Tampilkan top N kata",
    min_value=3,
    max_value=min(30, len(urut)),
    value=min(10, len(urut)),
)
urut_top = urut[:top_n]

# Tabel sederhana sebagai dict
st.dataframe(
    {"Kata": [k for k, _ in urut_top], "Frekuensi": [v for _, v in urut_top]},
    width="stretch",
    hide_index=True,
)

# ── Bar chart ─────────────────────────────────────────────────────────────────
st.subheader("Grafik Bar")

# st.bar_chart butuh dict atau dataframe dengan index = label
chart_data = {k: v for k, v in urut_top}
st.bar_chart(chart_data)

# ── Info ringkasan ─────────────────────────────────────────────────────────────
st.divider()
st.write(f"Total kata unik: **{len(frekuensi)}** | Total token: **{len(semua_kata)}**")

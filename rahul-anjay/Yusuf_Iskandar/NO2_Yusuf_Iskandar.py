import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import re
import string

st.set_page_config(page_title="Word Count Komentar", layout="centered")
st.title("📊 Word Count Komentar Media Sosial")
st.markdown("Analisis frekuensi kata dari komentar media sosial. Masukkan teks komentar atau unggah file teks.")

# Input teks langsung
komentar_input = st.text_area("Masukkan komentar (pisahkan baris atau satu teks panjang)", height=200)

# Atau upload file
uploaded_file = st.file_uploader("Atau unggah file teks (.txt)", type=["txt"])

# Gabungkan teks
full_text = ""
if komentar_input:
    full_text = komentar_input
elif uploaded_file is not None:
    full_text = uploaded_file.read().decode("utf-8")

if full_text:
    # Preprocessing teks
    text_clean = full_text.lower()
    text_clean = re.sub(f'[{re.escape(string.punctuation)}]', ' ', text_clean)  # hapus tanda baca
    text_clean = re.sub(r'\d+', '', text_clean)  # hapus angka
    words = text_clean.split()

    # Stopword sederhana (dapat ditambah sesuai kebutuhan)
    stopwords = set([
        "dan", "atau", "yang", "di", "ke", "dari", "dengan", "untuk", "pada", "ini", "itu",
        "tersebut", "saja", "sudah", "akan", "bisa", "adalah", "dalam", "sebagai", "juga",
        "karena", "tidak", "saya", "anda", "kita", "mereka", "pada", "oleh", "sebuah", "seorang"
    ])
    words = [w for w in words if w not in stopwords and len(w) > 1]

    # Hitung frekuensi
    word_counts = Counter(words)
    df = pd.DataFrame(word_counts.items(), columns=["Kata", "Frekuensi"])
    df = df.sort_values("Frekuensi", ascending=False)

    # Statistik
    st.subheader("📈 Statistik")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Kata", len(words))
    col2.metric("Kata Unik", len(word_counts))
    col3.metric("Kata Teratas", df.iloc[0]["Kata"] if not df.empty else "-")

    # Tabel 10 kata teratas
    st.subheader("🏆 10 Kata Teratas")
    st.dataframe(df.head(10), use_container_width=True)

    # Bar chart top 15
    st.subheader("📊 Bar Chart Frekuensi Kata (Top 15)")
    fig, ax = plt.subplots(figsize=(10, 6))
    top15 = df.head(15)
    ax.bar(top15["Kata"], top15["Frekuensi"], color='skyblue')
    ax.set_xlabel("Kata")
    ax.set_ylabel("Frekuensi")
    ax.set_title("Frekuensi Kata pada Komentar")
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)

    # Download hasil
    st.subheader("💾 Download Hasil")
    csv = df.to_csv(index=False)
    st.download_button(label="Download CSV", data=csv, file_name="word_count.csv", mime="text/csv")
else:
    st.info("Silakan masukkan komentar atau unggah file teks untuk memulai analisis.")

st.caption("Catatan: Stopwords sederhana digunakan untuk menyaring kata umum. Anda dapat menyesuaikan stopwords di kode.")
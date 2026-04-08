import streamlit as st
import pandas as pd
from collections import Counter
import re

# Konfigurasi Halaman
st.set_page_config(page_title="Word Count - Struktur Data", layout="wide")
st.title("📝 Word Count Komentar")

# Input Teks - Di sini bagian yang diubah menjadi kosong
teks_input = st.text_area(
    label="Masukkan Komentar Sosmed:", 
    value="", # Nilai awal dikosongkan
    placeholder="Ketik atau tempel komentar di sini (contoh: belajar struktur data itu seru sekali)...",
    height=150
)

# Tombol Proses
if st.button("Proses Word Count"):
    if teks_input.strip(): # Menggunakan .strip() untuk memastikan bukan cuma spasi
        # 1. Membersihkan teks (hapus tanda baca & kecilkan huruf)
        # Regex ini akan menghapus karakter selain huruf dan angka
        clean_text = re.sub(r'[^\w\s]', '', teks_input.lower())
        list_kata = clean_text.split()
        
        # 2. Struktur Data Dictionary (Counter)
        # Menghitung frekuensi kemunculan tiap kata
        counts = Counter(list_kata)
        
        # 3. Ubah ke Tabel (DataFrame) untuk visualisasi
        df = pd.DataFrame(counts.items(), columns=['Kata (Key)', 'Frekuensi (Value)'])
        df = df.sort_values(by='Frekuensi (Value)', ascending=False).reset_index(drop=True)

        # 4. Tampilkan Hasil dengan layout kolom
        st.markdown("---")
        col_tabel, col_grafik = st.columns([1, 2])
        
        with col_tabel:
            st.subheader("🗄️ Tabel Frekuensi")
            st.dataframe(df, use_container_width=True)
            
        with col_grafik:
            st.subheader("📈 Grafik Batang")
            st.bar_chart(data=df, x='Kata (Key)', y='Frekuensi (Value)')
            
        st.success(f"Analisis Selesai! Ditemukan **{len(counts)}** kata unik dari total **{len(list_kata)}** kata.")
    else:
        st.warning("Silakan masukkan teks terlebih dahulu sebelum menekan tombol proses.")

# Footer sederhana
st.sidebar.info("Aplikasi ini menggunakan Dictionary (Counter) untuk memproses struktur data teks.")
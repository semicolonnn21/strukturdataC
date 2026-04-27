import streamlit as st
import pandas as pd

st.title("💬 Word Count Komentar")

# 1. Input manual dari user
komentar = st.text_input("Ketik komentar di sini:", "Besok adalah hari jumat berkah")

if komentar:
    # 2. Proses Hitung (Key: Kata, Value: Jumlah)
    # Pecah kalimat menjadi list kata (huruf kecil semua)
    kata_list = komentar.lower().split()
    
    # Hitung frekuensi tiap kata unik
    data_hitung = {kata: kata_list.count(kata) for kata in set(kata_list)}

    # 3. Tampilkan Grafik
    st.write("### Grafik Frekuensi Kata")
    df = pd.DataFrame(data_hitung.items(), columns=["Kata", "Frekuensi"])
    
    # Visualisasi Bar Chart
    st.bar_chart(df.set_index("Kata"))

    # 4. Tampilkan Tabel Data
    st.write("### Detail Angka")
    st.table(df)

if st.button("Selesai ❄️"):
    st.snow()
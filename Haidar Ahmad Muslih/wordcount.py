import streamlit as st
from collections import Counter
import pandas as pd

st.title("Word Count Komentar Sosial Media")

# Input teks
text = st.text_area("Masukkan komentar:")

if text:
    # Preprocessing sederhana
    words = text.lower().split()

    # Hitung frekuensi
    word_count = Counter(words)

    st.subheader("Hasil Word Count (Key: Kata, Value: Frekuensi)")
    st.write(dict(word_count))

    # Konversi ke DataFrame untuk visualisasi
    df = pd.DataFrame(word_count.items(), columns=["Kata", "Frekuensi"])
    df = df.sort_values(by="Frekuensi", ascending=False)

    st.subheader("Visualisasi")
    for key in word_count:
      st.write(f"{key} : {word_count[key]}")
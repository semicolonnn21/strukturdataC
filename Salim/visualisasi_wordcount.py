import streamlit as st
from collections import Counter
import pandas as pd

st.title("Visualisasi Word Count Komentar Sosial Media")

text = st.text_area("Masukkan komentar:")

if st.button("Hitung Word Count"):

    words = text.lower().split()

    count = Counter(words)

    df = pd.DataFrame(count.items(), columns=["Kata", "Frekuensi"])

    st.subheader("Tabel Word Count")
    st.dataframe(df)

    st.subheader("Grafik Frekuensi Kata")
    st.bar_chart(df.set_index("Kata"))
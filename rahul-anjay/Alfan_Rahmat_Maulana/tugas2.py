import streamlit as st
from collections import Counter

st.title("Word Count Komentar/Analisis Frekuensi Kata")
komentar = st.text_area("Tulis apapun yang loe mau di sini...")

if st.button("Analisis"):

    kata = komentar.lower().split()

    hasil = Counter(kata)

    st.subheader("Frekuensi Kata")

    for k, v in hasil.items():
        st.write(k, ":", v)
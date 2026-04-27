import streamlit as st
from collections import Counter
import re

st.set_page_config(page_title="Word Count", layout="centered")

st.title("Word Count Komentar Media Sosial")

st.write("Masukkan komentar")

# Input teks
text = st.text_area("Komentar", "Saya sekarat saya butuh medkit, terimakasih")

# Proses word count
words = text.lower().split()
words = re.findall(r'\b\w+\b', text.lower())
word_count = Counter(words)

st.write("---")
st.write("Hasil Word Count:")

# Tampilkan hasil
for word, count in word_count.items():
    st.write(f"{word} : {count}")

st.write("---")
st.write("Total kata:", len(words))
import streamlit as st

st.title("Visualisasi Operasi Set")

# Input user
st.subheader("Masukkan data")
input_a = st.text_input("Set A (pisahkan dengan koma)", "1,2,3,4")
input_b = st.text_input("Set B (pisahkan dengan koma)", "3,4,5,6")

# Ubah ke set
set_a = set(map(int, input_a.split(",")))
set_b = set(map(int, input_b.split(",")))

# Operasi
union = set_a | set_b
intersection = set_a & set_b
difference = set_a - set_b
sym_diff = set_a ^ set_b

# Output
st.subheader("Hasil Operasi")
st.write("Union:", union)
st.write("Intersection:", intersection)
st.write("Difference (A - B):", difference)
st.write("Symmetric Difference:", sym_diff)

import streamlit as st
from collections import Counter

st.title("Visualisasi Word Count")

# Input teks
text = st.text_area("Masukkan komentar:")

if text:
    # Preprocessing
    words = text.lower().split()

    # Hitung frekuensi
    word_count = Counter(words)

    st.subheader("Hasil Word Count")
    st.write(dict(word_count))
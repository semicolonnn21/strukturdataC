import streamlit as st
from collections import Counter

# =========================
# OPERASI SET
# =========================

st.title("Aplikasi Operasi Set dan Word Count")

st.header("Operasi Set")

data_set1 = st.text_input(
    "Masukkan elemen Set A (pisahkan dengan koma)",
    "1,2,3,4"
)

data_set2 = st.text_input(
    "Masukkan elemen Set B (pisahkan dengan koma)",
    "3,4,5,6"
)

try:
    himpunan_a = {int(item.strip()) for item in data_set1.split(",")}
    himpunan_b = {int(item.strip()) for item in data_set2.split(",")}

    hasil_union = himpunan_a.union(himpunan_b)
    hasil_intersection = himpunan_a.intersection(himpunan_b)
    hasil_difference = himpunan_a.difference(himpunan_b)
    hasil_symdiff = himpunan_a.symmetric_difference(himpunan_b)

    st.subheader("Hasil Operasi Set")
    st.write("Union :", hasil_union)
    st.write("Intersection :", hasil_intersection)
    st.write("Difference (A - B) :", hasil_difference)
    st.write("Symmetric Difference :", hasil_symdiff)

except ValueError:
    st.error("Masukkan angka yang dipisahkan dengan koma.")

# =========================
# WORD COUNT
# =========================

st.markdown("---")

st.header("Word Count")

kalimat = st.text_area("Masukkan teks atau komentar")

if kalimat:
    daftar_kata = kalimat.lower().split()

    frekuensi_kata = Counter(daftar_kata)

    st.subheader("Hasil Perhitungan Kata")
    st.write(dict(frekuensi_kata))
import streamlit as st
from collections import Counter
import matplotlib.pyplot as plt

st.set_page_config(page_title="Visualisasi Set & Word Count", layout="wide")

menu = st.sidebar.selectbox("Pilih Fitur", ["Operasi Himpunan", "Word Count"])

# OPERASI HIMPUNAN
if menu == "Operasi Himpunan":
    st.title("Operasi Himpunan")

    st.write("Masukkan elemen himpunan (pisahkan dengan koma)")
    set_a_input = st.text_input("Himpunan A", " ")
    set_b_input = st.text_input("Himpunan B", " ")

    # Konversi
    set_a = set(map(str.strip, set_a_input.split(",")))
    set_b = set(map(str.strip, set_b_input.split(",")))

    st.subheader("Hasil Operasi")

    union = set_a.union(set_b)
    intersection = set_a.intersection(set_b)
    difference_ab = set_a.difference(set_b)
    difference_ba = set_b.difference(set_a)
    symmetric_diff = set_a.symmetric_difference(set_b)

    col1, col2 = st.columns(2)

    with col1:
        st.write("Union (A ∪ B):", union)
        st.write("Intersection (A ∩ B):", intersection)

    with col2:
        st.write("Difference (A - B):", difference_ab)
        st.write("Difference (B - A):", difference_ba)
        st.write("Symmetric Difference:", symmetric_diff)

# WORD COUNT
elif menu == "Word Count":
    st.title("Word Count Komentar")

    text_input = st.text_area("Masukkan komentar sosial media:", 
                                " ")
                              
    # Preprocessing (data cleaning & normalisasi data)
    words = text_input.lower().split()
    words = [word.strip(".,!?()-_=+/") for word in words]

    word_count = Counter(words)

    st.subheader("Hasil Word Count")
    st.write(dict(word_count))

# FOOTER
st.sidebar.info("created by: Dava Revanza Joan Putra")
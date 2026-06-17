import streamlit as st

st.title("Visualisasi Operasi Himpunan")

st.write("Masukkan elemen himpunan dipisahkan dengan koma")

A_input = st.text_input("Himpunan A", " ")
B_input = st.text_input("Himpunan B", " ")

A = set(A_input.split(","))
B = set(B_input.split(","))

if st.button("Hitung Operasi Himpunan"):

    union = A | B
    intersection = A & B
    difference = A - B
    sym_diff = A ^ B

    st.subheader("Hasil Operasi")

    st.write("Union (A ∪ B): ", union)
    st.write("Intersection (A ∩ B): ", intersection)
    st.write("Difference (A - B): ", difference)
    st.write("Symmetric Difference (A Δ B): ", sym_diff)
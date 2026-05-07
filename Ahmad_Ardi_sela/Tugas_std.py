import streamlit as st

st.title("Visualisasi Operasi Set")

# Input
set1_input = st.text_input("Masukkan elemen Set A (pisahkan dengan koma):")
set2_input = st.text_input("Masukkan elemen Set B (pisahkan dengan koma):")

if set1_input and set2_input:
    setA = set(set1_input.split(","))
    setB = set(set2_input.split(","))

    st.write("Set A:", setA)
    st.write("Set B:", setB)

    # Operasi
    union = setA | setB
    intersection = setA & setB
    difference = setA - setB
    sym_diff = setA ^ setB

    st.subheader("Hasil Operasi:")
    st.write("Union (A ∪ B):", union)
    st.write("Intersection (A ∩ B):", intersection)
    st.write("Difference (A - B):", difference)
    st.write("Symmetric Difference (A △ B):", sym_diff)


import streamlit as st

st.header("Operasi Set")

A_input = st.text_input("Masukkan Set A (menggunakan koma)", "")
B_input = st.text_input("Masukkan Set B (menggunakan koma)", "")
    
A = set(A_input.split(","))
B = set(B_input.split(","))

st.write("A =", A)
st.write("B =", B)

col1, col2 = st.columns(2)

st.subheader("Hasil")
st.write("Union =", A | B)
st.write("Intersection =", A & B)
st.write("Difference =", A - B)
st.write("Symmetric Difference =", A ^ B)
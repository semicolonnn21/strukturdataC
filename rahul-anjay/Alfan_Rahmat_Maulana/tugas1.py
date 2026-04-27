import streamlit as st

st.title("Visualisasi Operasi Set")
st.write("Masukkan angka dengan koma (contoh: 1,2,3)")

input_A = st.text_input("Set A", "11,12,13,14")
input_B = st.text_input("Set B", "13,14,15,16")

if st.button("Proses Operasi Set"):

    set_A = set(map(int, input_A.split(",")))
    set_B = set(map(int, input_B.split(",")))

    union = set_A | set_B
    intersection = set_A & set_B
    difference = set_A - set_B
    sym_diff = set_A ^ set_B

    st.subheader("Hasil Operasi")

    st.write("Union :", union)
    st.write("Intersection :", intersection)
    st.write("Difference (A - B) :", difference)
    st.write("Symmetric Difference :", sym_diff)
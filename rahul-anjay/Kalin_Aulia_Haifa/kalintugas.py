import streamlit as st

st.title("Operasi Set dengan Streamlit")

set1 = st.text_input("Masukkan elemen Set A (pisahkan dengan koma)" , "10,20,30,40")
set2 = st.text_input("Masukkan elemen Set B (pisahkan dengan koma" , "30,40,50,60")

A = set(set1.split(","))
B = set(set2.split(","))

st.write("Union:", A.union(B))
st.write("Intersection:", A.intersection(B))
st.write("Difference (A - B):", A.difference(B))
st.write("Symmetric Difference:", A.symmetric_difference(B))
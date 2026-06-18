import streamlit as st

st.title("Operasi Himpunan")

a_input = st.text_input("Himpunan A (pisah dengan koma)", "1, 2, 3, 4")
b_input = st.text_input("Himpunan B (pisah dengan koma)", "3, 4, 5, 6")

A = set(x.strip() for x in a_input.split(",") if x.strip())
B = set(x.strip() for x in b_input.split(",") if x.strip())

st.write(f"**A** = {sorted(A)}")
st.write(f"**B** = {sorted(B)}")

st.divider()

st.subheader("Union  (A ∪ B)")
st.success(f"{sorted(A | B)}")
st.caption("Semua elemen dari A dan B digabung.")

st.subheader("Intersection  (A ∩ B)")
st.info(f"{sorted(A & B)}")
st.caption("Hanya elemen yang ada di A sekaligus B.")

st.subheader("Difference  (A − B)")
st.warning(f"{sorted(A - B)}")
st.caption("Elemen A yang tidak ada di B.")

st.subheader("Symmetric Difference  (A △ B)")
st.error(f"{sorted(A ^ B)}")
st.caption("Elemen yang ada di A atau B, tapi tidak di keduanya.")


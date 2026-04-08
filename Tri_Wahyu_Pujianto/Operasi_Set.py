import streamlit as st

st.set_page_config(page_title="Visualisasi Operasi Set", layout="centered")

st.title("Visualisasi Operasi Set")

st.write("Masukkan elemen himpunan dipisahkan dengan koma (contoh:1,2,3)")

#Input
set_a_input=st.text_input("Himpunan A", "1,2,3")
set_b_input=st.text_input("HImpunan B", "3,4,5")

#Konvert string ke set
def parse_set(input_str):
    return set(item.strip()for item in input_str.split(",") if item.strip() !="")

A = parse_set(set_a_input)
B = parse_set(set_b_input)

st.subheader("Hasil Operasi")

#Operasi
union = A.union(B)
intersection= A.intersection(B)
difference_ab = A.difference(B)
difference_ba = B.difference(A)
symmetric_diff = A.symmetric_difference(B)

st.write("---")
st.write(f"Union (A ∪ B): {union}")
st.write(f"Intersection (A ∩ B): {intersection}")
st.write(f"Difference (A - B): {difference_ab}")
st.write(f"Difference (B - A): {difference_ba}")
st.write(f"Symmetric Difference (A Δ B): {symmetric_diff}")

#Visual sederhana

col1,col2 = st.columns(2)

with col1:
    st.write("Elemen hanya di A")
    st.success(difference_ab)

with col2:
    st.write("Elemen hanya di B")
    st.success(difference_ba)

st.write("Elemen Yang Sama (intersection)")
st.info(intersection)

st.write("semua elemen (union)")
st.warning(union)

st.write("Symmetric Difference (Tidak termasuk yang sama)")
st.error(symmetric_diff)

st.caption("Dibuat sambil ngopi")
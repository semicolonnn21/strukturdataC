import streamlit as st
import matplotlib.pyplot as plt
from matplotlib_venn import venn2
import re

st.set_page_config(page_title="Visualisasi Operasi Himpunan", layout="centered")
st.title("🔢 Visualisasi Operasi Himpunan")
st.markdown("Masukkan dua himpunan, dan lihat hasil operasi Union, Intersection, Difference, dan Symmetric Difference.")

# Input dari pengguna
col1, col2 = st.columns(2)
with col1:
    set_a_str = st.text_input("Himpunan A", value="1,2,3,4")
with col2:
    set_b_str = st.text_input("Himpunan B", value="3,4,5,6")

# Fungsi untuk mengubah string menjadi set
def parse_set(s):
    # Hapus spasi, split dengan koma
    items = [item.strip() for item in s.split(',') if item.strip()]
    # Konversi ke angka jika memungkinkan, jika tidak tetap string
    parsed = []
    for item in items:
        try:
            parsed.append(int(item))
        except ValueError:
            parsed.append(item)
    return set(parsed)

try:
    A = parse_set(set_a_str)
    B = parse_set(set_b_str)
except Exception as e:
    st.error(f"Error parsing input: {e}")
    st.stop()

st.write(f"*Himpunan A:* {A}")
st.write(f"*Himpunan B:* {B}")

# Operasi himpunan
union = A | B
intersection = A & B
diff_ab = A - B
diff_ba = B - A
sym_diff = A ^ B

st.subheader("📊 Hasil Operasi")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Union", len(union))
col2.metric("Intersection", len(intersection))
col3.metric("Difference A - B", len(diff_ab))
col4.metric("Symmetric Diff", len(sym_diff))

with st.expander("Lihat detail anggota"):
    st.write(f"*Union (A ∪ B):* {union}")
    st.write(f"*Intersection (A ∩ B):* {intersection}")
    st.write(f"*Difference (A - B):* {diff_ab}")
    st.write(f"*Difference (B - A):* {diff_ba}")
    st.write(f"*Symmetric Difference (A Δ B):* {sym_diff}")

# Diagram Venn
st.subheader("🟡 Diagram Venn")
fig, ax = plt.subplots(figsize=(6, 4))
venn2([set(A), set(B)], set_labels=('A', 'B'), ax=ax)
st.pyplot(fig)

st.caption("Catatan: Diagram Venn hanya mendukung dua himpunan. Untuk himpunan dengan lebih dari 2 set, gunakan library lain.")

import streamlit as st

st.title("📊 Operasi Himpunan Simpel")

# 1. Input Langsung (Manual)
A_input = st.text_input("Input Set A (pisahkan koma):", "1, 2, 3")
B_input = st.text_input("Input Set B (pisahkan koma):", "3, 4, 5")

# 2. Logika Set (Satu Baris)
A = set([x.strip() for x in A_input.split(",") if x.strip()])
B = set([x.strip() for x in B_input.split(",") if x.strip()])

# 3. Tampilkan Hasil
st.divider()
st.write(f"**Gabungan (A ∪ B):** {A | B}")
st.write(f"**Irisan (A ∩ B):** {A & B}")
st.write(f"**Selisih (A - B):** {A - B}")
st.write(f"**Beda Setangkup (A Δ B):** {A ^ B}")

# 4. Efek Salju
if st.button("Selesai ❄️"):
    st.snow()
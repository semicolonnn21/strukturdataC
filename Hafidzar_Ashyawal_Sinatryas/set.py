import streamlit as st

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Struktur Data👌👌", layout="wide")

st.title("🧮 Operasi Himpunan")

# Garis Pembatas
st.divider()

# Identitas
col_nama, col_nim, col_mk, col_class = st.columns(4)
with col_nama:
    st.write("**Nama:** Hafidzar Ashyawal Sinatryas")
with col_nim:
    st.write("**NIM:** 2530801075")
with col_mk:
    st.write("**Mata kuliah:** Struktur Data")
with col_class:
    st.write("**Kelas:** 2/C")

st.divider()


# Menggunakan kolom agar rapi
col1, col2 = st.columns(2)

with col1:
    input_A = st.text_input("Anggota Himpunan A")
    set_A = set([x.strip() for x in input_A.split(",") if x.strip()])

with col2:
    input_B = st.text_input("Anggota Himpunan B")
    set_B = set([x.strip() for x in input_B.split(",") if x.strip()])

# Menggunakan Selectbox untuk memilih operasi
operasi = st.selectbox("Pilih Operasi:", ["Intersection", "Union", "Difference (A-B)", "Symetric diff"])

if st.button("Hitung sekarang"):
    if operasi == "Intersection":
        hasil = set_A & set_B
    elif operasi == "Union":
        hasil = set_A | set_B
    elif operasi == "Difference (A-B)":
        hasil = set_A - set_B
    elif operasi == "Symetric diff":
        hasil = set_A ^ set_B
    
    st.success(f"Hasil {operasi}: {hasil}")
    st.toast ("SELAMAT ANDA JACKPOT")
    st.balloons()
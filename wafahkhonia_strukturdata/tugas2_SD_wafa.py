import streamlit as st
from collections import deque

# Membuat queue jika belum ada
if "daftar_pasien" not in st.session_state:
    st.session_state.daftar_pasien = deque()

st.title("Aplikasi Antrian Klinik")
st.write("Materi: Struktur Data - Queue (FIFO) (By: Wafah Khonia)")

# Input data pasien
input_pasien = st.text_input("Nama Pasien")

col1, col2 = st.columns(2)

with col1:
    if st.button("Tambah Antrian"):
        if input_pasien.strip():
            st.session_state.daftar_pasien.append(input_pasien)
            st.success(f"{input_pasien} berhasil ditambahkan ke antrian.")
        else:
            st.warning("Masukkan nama pasien terlebih dahulu.")

with col2:
    if st.button("Panggil Pasien"):
        if st.session_state.daftar_pasien:
            pasien_selanjutnya = st.session_state.daftar_pasien.popleft()
            st.info(f"Pasien yang sedang dilayani: {pasien_selanjutnya}")
        else:
            st.error("Tidak ada pasien dalam antrian.")

st.divider()

st.subheader("Antrian Pasien")

if st.session_state.daftar_pasien:

    total_pasien = len(st.session_state.daftar_pasien)

    for posisi, nama in enumerate(st.session_state.daftar_pasien, start=1):

        keterangan = ""

        if posisi == 1:
            keterangan += " ← FRONT"

        if posisi == total_pasien:
            keterangan += " ← REAR"

        st.write(f"{posisi}. {nama}{keterangan}")

    st.divider()

    st.write(
        f"Pasien berikutnya yang akan dilayani: **{st.session_state.daftar_pasien[0]}**"
    )

else:
    st.info("Antrian masih kosong.")
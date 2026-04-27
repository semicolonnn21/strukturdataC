import streamlit as st
from collections import deque

# 1. Inisialisasi Antrian 
if 'antrian_klinik' not in st.session_state:
    st.session_state.antrian_klinik = deque()

st.title("Sistem Antrian Klinik")
st.write("Materi: Struktur Data - Queue (FIFO) (By: Azhalia Mozaik)")

# 2. Input Pasien
nama_pasien = st.text_input("Masukkan Nama Pasien:")

# Tombol Enqueue dan Dequeue
if st.button("Pasien Datang (Enqueue)"):
    if nama_pasien:
        st.session_state.antrian_klinik.append(nama_pasien)
        st.success(f"Pasien {nama_pasien} masuk ke dalam antrian.")
    else:
        st.warning("Isi nama pasien terlebih dahulu.")

if st.button("Layani Pasien (Dequeue)"):
    if len(st.session_state.antrian_klinik) > 0:
        pasien_dilayani = st.session_state.antrian_klinik.popleft()
        st.info(f"Melayani pasien: {pasien_dilayani}")
    else:
        st.error("Antrian kosong!")

# 3. Menampilkan Status Antrian
st.write("---")
st.subheader("Daftar Antrian Saat Ini:")

if st.session_state.antrian_klinik:
    for i, pasien in enumerate(st.session_state.antrian_klinik):
        # Menandai Front dan Rear dengan teks biasa
        status = ""
        if i == 0:
            status = "(FRONT)"
        if i == len(st.session_state.antrian_klinik) - 1:
            status += " (REAR)"
            
        st.write(f"{i}. {pasien} {status}")
else:
    st.info("Belum ada pasien dalam antrian.")

# 4. Operasi Front 
if len(st.session_state.antrian_klinik) > 0:
    st.write("---")
    st.write(f"Pasien terdepan yang akan dilayani: **{st.session_state.antrian_klinik[0]}**")

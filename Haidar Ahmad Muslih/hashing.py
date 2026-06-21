import streamlit as st
import time

st.set_page_config(page_title="Project Hashing🔍", layout="wide")

st.title("🔍 Searching Algoritma and Hashing")
st.caption("***Untuk memenuhi Tugas Mata kuliah: Struktur Data😁***")

st.divider()

col_nama, col_nim, col_mk, col_class = st.columns(4)
with col_nama:
    st.write("**Nama:** Abil Ghinaya Azka")
with col_nim:
    st.write("**NIM:** 2530801056")
with col_mk:
    st.write("**Mata kuliah:** Struktur Data")
with col_class:
    st.write("**Kelas:** II C")

st.divider()

menu = st.sidebar.selectbox("Pilih Tugas", ["Searching", "Hashing"])

#searching algoritmanya
if menu == "Searching":
    st.subheader("Visualisasi Linear Search")
    data = [10, 20, 30, 40, 50]
    target = st.number_input("Cari angka (10-50):", value=30)
    
    if st.button("Mulai Cari"):
        for i, val in enumerate(data):
            st.write(f"Memeriksa indeks ke-{i}: {val}")
            time.sleep(0.5)
            if val == target:
                st.success(f"Ketemu di indeks ke-{i}!")
                break
        else:
            st.error("Data tidak ditemukan.")

#hashing
elif menu == "Hashing":
    st.subheader("Simulasi Hash Table (Modulo 5)")
    if "table" not in st.session_state:
        st.session_state.table = [None] * 5
        
    angka = st.number_input("Masukkan Angka:", value=0)
    if st.button("Insert"):
        index = angka % 5
        st.session_state.table[index] = angka
        st.success(f"Angka {angka} masuk ke indeks {index}")
        
    st.write("Isi Hash Table saat ini:", st.session_state.table)
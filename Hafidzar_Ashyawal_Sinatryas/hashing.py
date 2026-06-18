import streamlit as st
import time

st.title("Tugas Struktur Data: Searching & Hashing")

# ==========================================
# VISUALISASI SEARCHING
# ==========================================
st.header("1. Visualisasi Linear Search")

# Input data dan target
data = [10, 23, 45, 70, 11, 15, 88, 65]
st.write(f"Data: {data}")
target = st.number_input("Cari Angka:", value=70)

if st.button("Jalankan Linear Search"):
    status_placeholder = st.empty()
    jarjar = False
    
    for indeks, nilai in enumerate(data):
        # Tampilkan proses pengecekan saat ini
        status_placeholder.write(f"Memeriksa indeks ke-{indeks}: Apakah {nilai} == {target}?")
        time.sleep(0.5) # Efek jeda visualisasi
        
        if nilai == target:
            st.success(f"🎉 Ketemu! Angka {target} ada di indeks ke-{indeks}")
            jarjar = True
            break
            
    if not jarjar:
        st.error(f"❌ Angka {target} tidak ditemukan.")

st.markdown("---")

# ==========================================
# IMPLEMENTASI HASHING
# ==========================================
st.header("2. Implementasi Hashing (Linear Probing)")

# Inisialisasi tempat penyimpanan data (Hash Table) ukuran 10
if 'hash_table' not in st.session_state:
    st.session_state.hash_table = [None] * 10

# Input angka yang ingin dimasukkan ke hash table
input_hash = st.number_input("Masukkan Angka ke Hash Table:", value=0, key="hash_in")

if st.button("Simpan di Hash Table"):
    ukuran = 10
    indeks_asli = input_hash % ukuran
    indeks_cek = indeks_asli
    berhasil = False
    
    # Cari posisi kosong menggunakan Linear Probing jika terjadi tabrakan (kolisi)
    for i in range(ukuran):
        indeks_cek = (indeks_asli + i) % ukuran
        if st.session_state.hash_table[indeks_cek] is None:
            st.session_state.hash_table[indeks_cek] = input_hash
            st.success(f"Data {input_hash} disimpan di indeks {indeks_cek} (Rumus asli: {indeks_asli})")
            berhasil = True
            break
            
    if not berhasil:
        st.error("Hash Table sudah penuh!")

# Cetak isi Hash Table saat ini
st.write("Isi Hash Table Sekarang:")
st.json(st.session_state.hash_table)

if st.button("Reset Hash Table"):
    st.session_state.hash_table = [None] * 10
    st.rerun()
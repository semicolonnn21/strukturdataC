import streamlit as st
import time

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Tugas 5 Struktur Data - Azhalia Mozaik", layout="centered")

# ==========================================
# LOGIKA PENCARIAN (DENGAN TAMPILAN PROSES)
# ==========================================

# Sequential Search
def sequential_search(list_data, target):
    st.subheader("Proses Linear (Satu per Satu):")
    indeks_ketemu = -1
    
    for i in range(len(list_data)):
        # Logika pengecekan
        if list_data[i] == target:
            st.write(f"Cek Indeks {i} (Nilai: {list_data[i]}) → ✅ Cocok!")
            indeks_ketemu = i
            break
        else:
            st.write(f"Cek Indeks {i} (Nilai: {list_data[i]}) → ❌ Bukan")
        
        time.sleep(0.3) # Efek loading biar keren
    return indeks_ketemu

# Binary Search
def binary_search(list_data, target):
    st.subheader("Proses Binary Search:")
    awal = 0
    akhir = len(list_data) - 1
    langkah = 1
    
    while awal <= akhir:
        tengah = (awal + akhir) // 2
        st.write(f"Langkah {langkah}: Tengah di indeks {tengah} (Nilai: {list_data[tengah]})")
        
        if list_data[tengah] == target:
            return tengah
        elif list_data[tengah] < target:
            awal = tengah + 1
        else:
            akhir = tengah - 1
        
        langkah += 1
        time.sleep(0.5)
            
    return -1

# ==========================================
# TAMPILAN UTAMA (UI)
# ==========================================

st.sidebar.title("📌 Menu Navigasi")
menu = st.sidebar.radio("Pilih Materi:", ["Searching", "Hashing Table"])

if menu == "Searching":
    st.title("🔍 Visualisasi Algoritma Searching 🔍")
    
    teks_input = st.text_input("Masukkan angka (pisahkan dengan koma):", "25, 30, 80, 10, 59")
    angka_target = st.text_input("Ketik angka yang ingin dicari:", "10")
    metode = st.selectbox("Pilih Metode:", ["Sequential Search", "Binary Search"])

    if st.button("Mulai Cari"):
        try:
            data = [int(i.strip()) for i in teks_input.split(",")]
            target = int(angka_target)

            if metode == "Sequential Search":
                hasil = sequential_search(data, target)
            else:
                data = sorted(data)
                st.info(f"Data diurutkan: {data}")
                hasil = binary_search(data, target)

            # Hasil Akhir
            if hasil != -1:
                st.success(f"Ketemu! Angka {target} ada di indeks {hasil}.")
            else:
                st.error(f"Angka {target} tidak ditemukan dalam list.")
        except:
            st.warning("Input harus berupa angka!")

else:
    # Hashing
    st.title("🗄️ Visualisasi Hashing (Mod 7)")
    if 'tabel_hash' not in st.session_state:
        st.session_state.tabel_hash = [[] for _ in range(7)]

    input_angka = st.text_input("Ketik angka:", "14")
    if st.button("Simpan"):
        n = int(input_angka)
        idx = n % 7
        if n not in st.session_state.tabel_hash[idx]:
            st.session_state.tabel_hash[idx].append(n)
    
    for i in range(7):
        st.write(f"Index {i}: {st.session_state.tabel_hash[i]}")

st.sidebar.divider()
st.sidebar.caption("Azhalia Mozaik | NIM: 2530801059")
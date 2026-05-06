import streamlit as st
import time

st.set_page_config(page_title="Visualisasi Searching", layout="centered")

st.title("🔍 Visualisasi Algoritma Pencarian")
st.write("Implementasi Sequential Search dan Binary Search")

# Meminta input dari pengguna
input_data = st.text_input("Masukkan deret angka (pisahkan dengan koma):", "10, 50, 30, 70, 80, 60, 20, 90, 40")
target_input = st.number_input("Masukkan angka yang ingin dicari (Key):", value=30)
algoritma = st.radio("Pilih Algoritma Pencarian:", ["Sequential Search", "Binary Search"])

# Mengubah input string menjadi list integer
try:
    arr = [int(x.strip()) for x in input_data.split(",")]
except ValueError:
    st.error("Pastikan input hanya berisi angka dan koma.")
    st.stop()

if st.button("Mulai Pencarian"):
    tempat_visual = st.empty()
    
    if algoritma == "Sequential Search":
        # Sequential Search: Mencari dari indeks awal sampai akhir 
        ditemukan = False
        for i in range(len(arr)):
            # Visualisasi status saat ini
            tampilan = f"**Mencari Key: {target_input}**\n\n"
            for j, val in enumerate(arr):
                if j == i:
                    tampilan += f"👉 **[{val}]** " # Menandai elemen yang sedang dicek (Cur) [cite: 42]
                else:
                    tampilan += f" {val} "
            
            tempat_visual.markdown(tampilan)
            time.sleep(0.8) # Memberi jeda agar animasi terlihat
            
            if arr[i] == target_input:
                st.success(f"Angka {target_input} ditemukan pada indeks ke-{i}!")
                ditemukan = True
                break
                
        if not ditemukan:
            st.error(f"Angka {target_input} tidak ditemukan dalam list.")

    elif algoritma == "Binary Search":
        # Binary Search mewajibkan data dalam keadaan terurut [cite: 89]
        arr.sort()
        st.info(f"Data diurutkan terlebih dahulu: {arr}")
        
        low = 0
        high = len(arr) - 1
        ditemukan = False
        
        while low <= high:
            mid = (low + high) // 2 # Mencari posisi tengah [cite: 90]
            
            # Visualisasi status Low, Mid, High [cite: 138]
            tampilan = f"**Mencari Key: {target_input}** | Low: {low}, Mid: {mid}, High: {high}\n\n"
            for j, val in enumerate(arr):
                if j == mid:
                    tampilan += f"🎯 **[{val}]** "
                elif low <= j <= high:
                    tampilan += f" `{val}` "
                else:
                    tampilan += f" {val} "
                    
            tempat_visual.markdown(tampilan)
            time.sleep(1.2)
            
            if arr[mid] == target_input:
                st.success(f"Angka {target_input} ditemukan pada indeks ke-{mid} (setelah diurutkan)!")
                ditemukan = True
                break
            elif arr[mid] < target_input:
                low = mid + 1 # Jika lebih besar, cari di separuh kanan [cite: 98]
            else:
                high = mid - 1 # Jika lebih kecil, cari di separuh kiri [cite: 99]
                
        if not ditemukan:
            st.error(f"Angka {target_input} tidak ditemukan dalam list.")
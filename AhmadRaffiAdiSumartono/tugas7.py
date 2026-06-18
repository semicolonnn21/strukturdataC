import streamlit as st
import time

st.set_page_config(page_title="Visualisasi Searching - Struktur Data", layout="wide")

st.title("🔍 Visualisasi Algoritma Searching")
st.write("Presented by Muhammad Iszul Wilsa, S.Si., M.Cs")

# Input Data
data_input = st.text_input("Masukkan angka (pisahkan dengan koma):", "10, 50, 30, 70, 80, 60, 20, 90, 40")
target = st.number_input("Cari angka:", value=30)
method = st.selectbox("Pilih Metode:", ["Sequential Search", "Binary Search"])

if st.button("Mulai Pencarian"):
    arr = [int(x.strip()) for x in data_input.split(",")]
    
    if method == "Sequential Search":
        st.subheader("Proses Sequential Search")
        found = False
        cols = st.columns(len(arr))
        
        for i in range(len(arr)):
            time.sleep(0.5) # Efek animasi
            with cols[i]:
                if arr[i] == target:
                    st.success(f"[{arr[i]}]")
                    st.write("Match!")
                    found = True
                    break
                else:
                    st.warning(f"{arr[i]}")
                    st.write("No")
        
        if found:
            st.success(f"Data {target} ditemukan pada indeks ke-{i}")
        else:
            st.error("Data tidak ditemukan")

    else: # Binary Search
        st.subheader("Proses Binary Search (Data diurutkan terlebih dahulu)")
        arr.sort()
        st.write("Sorted Array:", arr)
        
        low = 0
        high = len(arr) - 1
        found = False
        step = 1
        
        while low <= high:
            mid = (low + high) // 2
            st.write(f"**Langkah {step}:** Low={low}, High={high}, Mid Index={mid}, Mid Value={arr[mid]}")
            
            if arr[mid] == target:
                st.success(f"Target {target} ditemukan di indeks {mid}!")
                found = True
                break
            elif arr[mid] < target:
                st.info(f"{arr[mid]} < {target}, geser Low ke arah kanan.")
                low = mid + 1
            else:
                st.info(f"{arr[mid]} > {target}, geser High ke arah kiri.")
                high = mid - 1
            step += 1
            time.sleep(1)

        if not found:
            st.error("Data tidak ditemukan")
import streamlit as st
import time

st.set_page_config(page_title="Visualisasi Searching", layout="centered")

st.title("🔍 Visualisasi Algoritma Searching")

# Input data
data_input = st.text_input("Masukkan data (pisahkan dengan koma)", "7,2,9,4,6,3,10,8")
key = st.number_input("Masukkan angka yang dicari", step=1)

data = [int(x.strip()) for x in data_input.split(",")]

# Pilih metode
metode = st.selectbox("Pilih metode", ["Sequential Search", "Binary Search"])

st.write("Data:", data)

# Tombol mulai
if st.button("Mulai Pencarian"):

    if metode == "Sequential Search":
        st.subheader("🔎 Sequential Search")

        found = False
        for i in range(len(data)):
            st.write(f"Cek index {i} → {data[i]}")
            time.sleep(0.5)

            if data[i] == key:
                st.success(f"✅ Data ditemukan di index {i}")
                found = True
                break

        if not found:
            st.error("❌ Data tidak ditemukan")

    else:
        st.subheader("⚡ Binary Search")

        data.sort()
        st.write("Data diurutkan:", data)

        low = 0
        high = len(data) - 1
        found = False

        while low <= high:
            mid = (low + high) // 2
            st.write(f"Tengah index {mid} → {data[mid]}")
            time.sleep(0.7)

            if data[mid] == key:
                st.success(f"✅ Data ditemukan di index {mid}")
                found = True
                break
            elif data[mid] < key:
                st.write("➡️ Ke kanan")
                low = mid + 1
            else:
                st.write("⬅️ Ke kiri")
                high = mid - 1

        if not found:
            st.error("❌ Data tidak ditemukan")
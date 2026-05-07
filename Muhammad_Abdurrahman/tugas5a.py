import streamlit as st
import time

st.title("Binary Search Visualization")

data_input = st.text_input("Masukkan data (pisahkan dengan koma)", "7,2,9,4,6,3,10,8")
key = st.number_input("Masukkan nilai yang dicari", step=1)

data = list(map(int, data_input.split(",")))

if st.button("Cari"):
    data.sort()
    st.write("Data setelah sorting:", data)

    low = 0
    high = len(data) - 1
    found = False

    while low <= high:
        mid = (low + high) // 2
        st.write(f"Cek index {mid}: {data[mid]}")
        time.sleep(0.5)

        if data[mid] == key:
            st.success(f"Data ditemukan di index {mid}")
            found = True
            break
        elif data[mid] < key:
            low = mid + 1
        else:
            high = mid - 1

    if not found:
        st.error("Data tidak ditemukan")
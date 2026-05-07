import streamlit as st

st.title("Visualisasi Binary Search")

# Input data
data_input = st.text_input("Masukkan angka (pisahkan dengan koma)", "1,3,5,7,9,11,13")
target = st.number_input("Masukkan angka yang dicari", step=1)

# Proses data
data = list(map(int, data_input.split(",")))
data.sort()

st.write("Data setelah diurutkan:", data)

def binary_search(arr, target):
    steps = []
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        steps.append((left, mid, right))

        if arr[mid] == target:
            return mid, steps
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1, steps

if st.button("Cari"):
    result, steps = binary_search(data, target)

    for i, (l, m, r) in enumerate(steps):
        st.write(f"Langkah {i+1}: left={l}, mid={m}, right={r}, nilai tengah={data[m]}")

    if result != -1:
        st.success(f"Data ditemukan di index {result}")
    else:
        st.error("Data tidak ditemukan")

import streamlit as st

st.title("Visualisasi Algoritma Searching")

# Input data
data_input = st.text_input("Masukkan angka (pisahkan dengan koma)", "1,2,4,5,7,9")
target = st.number_input("Angka yang dicari", step=1)

data = [int(x) for x in data_input.split(",")]

# PILIH ALGORITMA
algo = st.selectbox("Pilih Algoritma", ["Linear Search", "Binary Search"])

# ======================
# LINEAR SEARCH
# ======================
def linear_search(arr, target):
    steps = []
    for i in range(len(arr)):
        steps.append(f"Cek index {i}: {arr[i]}")
        if arr[i] == target:
            return i, steps
    return -1, steps

# ======================
# BINARY SEARCH
# ======================
def binary_search(arr, target):
    arr.sort()
    low = 0
    high = len(arr) - 1
    steps = []

    while low <= high:
        mid = (low + high) // 2
        steps.append(f"Low={low}, High={high}, Mid={mid} -> {arr[mid]}")

        if arr[mid] == target:
            return mid, steps
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1, steps

# ======================
# EKSEKUSI
# ======================
if st.button("Cari"):
    if algo == "Linear Search":
        index, steps = linear_search(data, target)
    else:
        index, steps = binary_search(data, target)

    st.subheader("Langkah-langkah:")
    for step in steps:
        st.write(step)

    if index != -1:
        st.success(f"Ditemukan di index {index}")
    else:
        st.error("Tidak ditemukan")

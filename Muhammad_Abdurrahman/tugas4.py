import streamlit as st
import random
import time
import matplotlib.pyplot as plt

def bubble_sort(arr):
    a = arr.copy()
    n = len(a)
    for i in range(n):
        for j in range(0, n-i-1):
            if a[j] > a[j+1]:
                a[j], a[j+1] = a[j+1], a[j]
    return a

def insertion_sort(arr):
    a = arr.copy()
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j+1] = a[j]
            j -= 1
        a[j+1] = key
    return a

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

st.title("Benchmark Sorting")

size = st.slider("Ukuran Data", 100, 10000, 1000)

if "results" not in st.session_state:
    st.session_state.results = {"bubble": None, "insertion": None, "merge": None}

if "sorted_data" not in st.session_state:
    st.session_state.sorted_data = {"bubble": None, "insertion": None, "merge": None}

data = [random.randint(1, 100000) for _ in range(size)]
st.write("Data awal:", data)

if st.button("Run Bubble Sort"):
    start = time.time()
    result = bubble_sort(data)
    end = time.time()
    st.session_state.results["bubble"] = end - start
    st.session_state.sorted_data["bubble"] = result

if st.button("Run Insertion Sort"):
    start = time.time()
    result = insertion_sort(data)
    end = time.time()
    st.session_state.results["insertion"] = end - start
    st.session_state.sorted_data["insertion"] = result

if st.button("Run Merge Sort"):
    start = time.time()
    result = merge_sort(data)
    end = time.time()
    st.session_state.results["merge"] = end - start
    st.session_state.sorted_data["merge"] = result

st.subheader("Waktu Eksekusi")
st.write(st.session_state.results)

st.subheader("Hasil Sorting (Full Data)")

for key, val in st.session_state.sorted_data.items():
    if val is not None:
        st.write(f"{key}:", val)

if any(v is not None for v in st.session_state.results.values()):
    labels = []
    values = []

    for key, val in st.session_state.results.items():
        if val is not None:
            labels.append(key)
            values.append(val)

    fig, ax = plt.subplots()
    ax.bar(labels, values)
    ax.set_xlabel("Algoritma")
    ax.set_ylabel("Waktu (detik)")
    ax.set_title("Perbandingan Waktu Sorting")

    st.pyplot(fig)
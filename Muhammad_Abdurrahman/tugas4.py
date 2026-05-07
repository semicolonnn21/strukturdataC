import streamlit as st
import random
import time
import matplotlib.pyplot as plt
import pandas as pd

def bubble_sort(arr):
    a = arr.copy()
    for i in range(len(a)):
        for j in range(len(a)-i-1):
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
    mid = len(arr)//2
    return merge(merge_sort(arr[:mid]), merge_sort(arr[mid:]))

def merge(l, r):
    res = []
    i = j = 0
    while i < len(l) and j < len(r):
        if l[i] < r[j]:
            res.append(l[i]); i+=1
        else:
            res.append(r[j]); j+=1
    return res + l[i:] + r[j:]

st.title("Benchmark Sorting (Final)")

n = st.slider("Jumlah Data (n)", 100, 10000, 1000)
runs = st.number_input("Jumlah Run", 1, 10, 3)

data = [random.randint(1,100000) for _ in range(n)]
st.write("Data awal:", data)

if "table" not in st.session_state:
    st.session_state.table = []

def benchmark(name, func):
    times = []
    result = None
    for _ in range(runs):
        arr = data.copy()
        start = time.time()
        result = func(arr)
        end = time.time()
        times.append(end - start)

    avg = sum(times)/len(times)

    row = {
        "Algoritma": name,
        "n": n,
    }

    for i, t in enumerate(times):
        row[f"Run {i+1}"] = t

    row["Avg"] = avg

    st.session_state.table.append(row)

    return result, avg

if st.button("Run Bubble Sort"):
    res, avg = benchmark("Bubble", bubble_sort)
    st.write("Hasil:", res)

if st.button("Run Insertion Sort"):
    res, avg = benchmark("Insertion", insertion_sort)
    st.write("Hasil:", res)

if st.button("Run Merge Sort"):
    res, avg = benchmark("Merge", merge_sort)
    st.write("Hasil:", res)

st.subheader("Tabel Benchmark")

if st.session_state.table:
    df = pd.DataFrame(st.session_state.table)
    st.dataframe(df)

st.subheader("Grafik")

if st.session_state.table:
    df = pd.DataFrame(st.session_state.table)
    fig, ax = plt.subplots()
    ax.bar(df["Algoritma"], df["Avg"])
    ax.set_xlabel("Algoritma")
    ax.set_ylabel("Avg Waktu")
    st.pyplot(fig)
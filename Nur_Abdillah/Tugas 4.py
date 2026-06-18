import streamlit as st
import random
import time
import pandas as pd

# ======================
# UI
# ======================
st.title("📊 Sorting Benchmark")
st.write("Perbandingan Bubble, Selection, dan Insertion Sort")

# ======================
# SORTING
# ======================
def bubble_sort(arr):
    a = arr.copy()
    n = len(a)
    for i in range(n):
        for j in range(n-i-1):
            if a[j] > a[j+1]:
                a[j], a[j+1] = a[j+1], a[j]
    return a

def selection_sort(arr):
    a = arr.copy()
    n = len(a)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if a[j] < a[min_idx]:
                min_idx = j
        a[i], a[min_idx] = a[min_idx], a[i]
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

# ======================
# BENCHMARK
# ======================
def benchmark(sort_func, data):
    times = []
    for _ in range(3):
        arr = data.copy()
        start = time.time()
        sort_func(arr)
        end = time.time()
        times.append(end - start)
    return sum(times) / 3

# ======================
# SESSION STATE
# ======================
if "results" not in st.session_state:
    st.session_state.results = []

# ======================
# DATA SIZE (AMAN)
# ======================
sizes = [100, 1000, 5000, 10000]

st.subheader("Jalankan per ukuran data")

for size in sizes:
    if st.button(f"Run n = {size}"):

        with st.spinner(f"Processing n={size}... sabar ya 😭"):

            data = [random.randint(1, 100000) for _ in range(size)]

            bubble = benchmark(bubble_sort, data)
            selection = benchmark(selection_sort, data)
            insertion = benchmark(insertion_sort, data)

            st.session_state.results.append({
                "Ukuran": size,
                "Bubble": bubble,
                "Selection": selection,
                "Insertion": insertion
            })

            st.success(f"Selesai n={size}")

# ======================
# TAMPILKAN HASIL
# ======================
if st.session_state.results:
    df = pd.DataFrame(st.session_state.results)

    st.subheader("Tabel Benchmark")
    st.dataframe(df)

    # ======================
    # GRAFIK STREAMLIT (NO MATPLOTLIB)
    # ======================
    st.subheader("Grafik Performa")
    chart_df = df.set_index("Ukuran")
    st.line_chart(chart_df)

    # ======================
    # ANALISIS
    # ======================
    st.subheader("Analisis")

    avg = df[["Bubble", "Selection", "Insertion"]].mean()
    fastest = avg.idxmin()

    st.write(f" Algoritma tercepat: **{fastest}**")

    st.write("""
 **Mengapa?**  
Insertion Sort cenderung lebih cepat karena lebih efisien dalam pergeseran elemen dibanding Bubble dan Selection.

 **Apakah sesuai Big O?**  
Ya. Ketiga algoritma memiliki kompleksitas O(n²).  
Namun dalam praktik, performa bisa berbeda karena jumlah operasi nyata tidak sama.
""")

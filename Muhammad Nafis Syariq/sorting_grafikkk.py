import streamlit as st
import random
import time
import pandas as pd

st.set_page_config(page_title="Grafik Sorting", layout="centered")

st.title("📈 Grafik Perbandingan Algoritma Sorting")


def selection_sort(arr):
    data = arr.copy()
    for i in range(len(data)):
        min_idx = i
        for j in range(i+1, len(data)):
            if data[j] < data[min_idx]:
                min_idx = j
        data[i], data[min_idx] = data[min_idx], data[i]
    return data


def insertion_sort(arr):
    data = arr.copy()
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        while j >= 0 and data[j] > key:
            data[j+1] = data[j]
            j -= 1
        data[j+1] = key
    return data


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

sizes = [100, 1000, 10000, 50000]
repeat = 3

results = []
progress = st.progress(0)

total_steps = len(sizes) * 3  # 3 algoritma
step = 0

for size in sizes:
    data = random.sample(range(size * 10), size)

    times = []
    for _ in range(repeat):
        start = time.perf_counter()
        selection_sort(data)
        times.append(time.perf_counter() - start)
    selection_avg = sum(times) / repeat

    step += 1
    progress.progress(step / total_steps)

    times = []
    for _ in range(repeat):
        start = time.perf_counter()
        insertion_sort(data)
        times.append(time.perf_counter() - start)
    insertion_avg = sum(times) / repeat

    step += 1
    progress.progress(step / total_steps)
    
    times = []
    for _ in range(repeat):
        start = time.perf_counter()
        merge_sort(data)
        times.append(time.perf_counter() - start)
    merge_avg = sum(times) / repeat

    step += 1
    progress.progress(step / total_steps)

    results.append({
        "Ukuran Data": size,
        "Selection Sort": selection_avg,
        "Insertion Sort": insertion_avg,
        "Merge Sort": merge_avg
    })

df = pd.DataFrame(results)

st.subheader("📊 Grafik Perbandingan Waktu Eksekusi")
st.line_chart(df.set_index("Ukuran Data"))
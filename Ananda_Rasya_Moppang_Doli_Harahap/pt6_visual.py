import streamlit as st
import random
import time
import pandas as pd

st.set_page_config(page_title="Grafik Sorting", layout="centered")

st.title("📈 Benchmark Sorting (Versi Interaktif)")

st.info("Klik tombol untuk mulai benchmarking")
st.warning("Data 50.000 akan lama untuk Selection & Insertion ⚠️")

# ======================
# SORTING
# ======================

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


# ======================
# MAIN BUTTON
# ======================

if st.button("🚀 Jalankan Benchmark"):

    sizes = [100, 1000, 10000, 50000]
    repeat = 3

    progress = st.progress(0)
    status = st.empty()

    results = []
    total_steps = len(sizes) * 3
    step = 0

    for size in sizes:
        status.write(f"🔄 Memproses data {size}...")

        data = random.sample(range(size * 10), size)

        # Selection
        times = []
        for _ in range(repeat):
            start = time.perf_counter()
            selection_sort(data)
            times.append(time.perf_counter() - start)
        selection_avg = sum(times) / repeat

        step += 1
        progress.progress(step / total_steps)

        # Insertion
        times = []
        for _ in range(repeat):
            start = time.perf_counter()
            insertion_sort(data)
            times.append(time.perf_counter() - start)
        insertion_avg = sum(times) / repeat

        step += 1
        progress.progress(step / total_steps)

        # Merge
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
            "Selection": selection_avg,
            "Insertion": insertion_avg,
            "Merge": merge_avg
        })

    status.success("✅ Selesai!")

    df = pd.DataFrame(results)

    st.subheader("📊 Grafik Hasil")
    st.line_chart(df.set_index("Ukuran Data"))
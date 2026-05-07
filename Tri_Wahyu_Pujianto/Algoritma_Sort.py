import time
import random
import streamlit as st
import pandas as pd

#  ALGORITMA SORTING

def bubble_sort(arr):
    n = len(arr)
    arr = arr.copy()
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def selection_sort(arr):
    n = len(arr)
    arr = arr.copy()
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


def merge_sort(arr):
    if len(arr) <= 1:
        return arr[:]
    mid = len(arr) // 2
    left  = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)

def _merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

#  HELPER

def ukur_waktu(func, data):
    start = time.perf_counter()
    func(data)
    return time.perf_counter() - start

def fmt(detik):
    return f"{detik:.6f} s"

ALGORITMA = {
    "Bubble Sort"   : bubble_sort,
    "Selection Sort": selection_sort,
    "Merge Sort"    : merge_sort,
}

st.set_page_config(page_title="Sorting Benchmark", layout="wide")

st.title("Sorting Benchmark")
st.caption("Struktur Data / Tri Wahyu Pujianto")
st.divider()

with st.sidebar:
    st.header("Konfigurasi")

    ukuran_pilihan = st.multiselect(
        "Ukuran Data (n)",
        options=[100, 1_000, 10_000, 50_000, 100_000, 1_000_000],
        default=[100, 1_000, 10_000],
    )

    algoritma_pilihan = st.multiselect(
        "Algoritma",
        options=list(ALGORITMA.keys()),
        default=list(ALGORITMA.keys()),
    )

    jumlah_run = st.slider("Jumlah Run", min_value=1, max_value=5, value=3)

    jalankan = st.button(" Jalankan Benchmark", type="primary", use_container_width=True)

# Validasi
if not ukuran_pilihan or not algoritma_pilihan:
    st.warning("Pilih minimal satu ukuran data dan satu algoritma.")
    st.stop()

# Benchmark
if jalankan:
    hasil = {nama: {} for nama in algoritma_pilihan}

    progress_bar = st.progress(0, text="Memulai benchmark...")
    total_steps  = len(ukuran_pilihan) * len(algoritma_pilihan)
    step = 0

    for ukuran in ukuran_pilihan:
        data_asli = [random.randint(0, 1_000_000) for _ in range(ukuran)]

        for nama in algoritma_pilihan:
            func = ALGORITMA[nama]
            runs = [ukur_waktu(func, data_asli.copy()) for _ in range(jumlah_run)]
            hasil[nama][ukuran] = runs

            step += 1
            progress_bar.progress(step / total_steps, text=f"Selesai: {nama} — n={ukuran:,}")

    progress_bar.empty()
    st.success("Benchmark selesai!")
    st.divider()

    # ukuran data
    st.subheader("Hasil Per Ukuran Data")

    for ukuran in ukuran_pilihan:
        st.markdown(f"**n = {ukuran:,} elemen**")
        run_cols = [f"Run {i+1}" for i in range(jumlah_run)]
        rows = []
        for nama in algoritma_pilihan:
            val  = hasil[nama][ukuran]
            rata = sum(val) / len(val)
            row  = {"Algoritma": nama}
            for i, v in enumerate(val):
                row[f"Run {i+1}"] = fmt(v)
            row["Rata-rata"] = fmt(rata)
            rows.append(row)

        df = pd.DataFrame(rows).set_index("Algoritma")
        st.dataframe(df, use_container_width=True)

    st.divider()

    # Tabel rangkuman
    st.subheader("Rangkuman Rata-rata Waktu Eksekusi")

    rows2 = []
    for nama in algoritma_pilihan:
        row = {"Algoritma": nama}
        for ukuran in ukuran_pilihan:
            val = hasil[nama][ukuran]
            row[f"n={ukuran:,}"] = fmt(sum(val) / len(val))
        rows2.append(row)

    df2 = pd.DataFrame(rows2).set_index("Algoritma")
    st.dataframe(df2, use_container_width=True)

    st.divider()

    # Grafik rata-rata
    st.subheader("Grafik Perbandingan Rata-rata Waktu")

    chart_data = {}
    for nama in algoritma_pilihan:
        chart_data[nama] = [
            sum(hasil[nama][u]) / len(hasil[nama][u])
            for u in ukuran_pilihan
        ]

    df_chart = pd.DataFrame(chart_data, index=[str(u) for u in ukuran_pilihan])
    df_chart.index.name = "Ukuran Data (n)"
    st.line_chart(df_chart, use_container_width=True)

else:
    st.info("Atur konfigurasi di sidebar and run -Tapi Ngotak mas milih datanya, kasian laptonya.------")
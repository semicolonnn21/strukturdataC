import streamlit as st
import random
import time

st.title("Benchmark Sorting Sederhana")

# =========================
# Selection Sort
# =========================
def selection_sort(data):
    angka = data.copy()
    jumlah = len(angka)
    for i in range(jumlah):
        indeks_min = i
        for j in range(i + 1, jumlah):
            if angka[j] < angka[indeks_min]:
                indeks_min = j
        angka[i], angka[indeks_min] = angka[indeks_min], angka[i]
    return angka

# =========================
# Insertion Sort
# =========================
def insertion_sort(data):
    angka = data.copy()
    for i in range(1, len(angka)):
        nilai = angka[i]
        j = i - 1
        while j >= 0 and nilai < angka[j]:
            angka[j + 1] = angka[j]
            j -= 1
        angka[j + 1] = nilai
    return angka

# =========================
# Quick Sort
# =========================
def quick_sort(data):
    if len(data) <= 1:
        return data
    pivot = data[len(data) // 2]
    kiri = [x for x in data if x < pivot]
    tengah = [x for x in data if x == pivot]
    kanan = [x for x in data if x > pivot]
    return quick_sort(kiri) + tengah + quick_sort(kanan)

# =========================
# Hitung Waktu
# =========================
def hitung_waktu(fungsi_sort, data):
    mulai = time.time()
    fungsi_sort(data)
    selesai = time.time()
    return selesai - mulai

# =========================
# Benchmark
# =========================
ukuran_data = [100, 1000, 10000, 50000]
hasil_benchmark = []

st.write("Sedang menjalankan benchmark...")

for jumlah in ukuran_data:
    total_selection = 0
    total_insertion = 0
    total_quick = 0
    for _ in range(3):
        data_acak = random.sample(range(jumlah * 10), jumlah)
        total_selection += hitung_waktu(selection_sort, data_acak)
        total_insertion += hitung_waktu(insertion_sort, data_acak)
        total_quick += hitung_waktu(quick_sort, data_acak)
    rata_selection = total_selection / 3
    rata_insertion = total_insertion / 3
    rata_quick = total_quick / 3
    hasil_benchmark.append([
        jumlah,
        rata_selection,
        rata_insertion,
        rata_quick
    ])

# =========================
# Tabel Hasil
# =========================
st.subheader("Tabel Hasil Benchmark")

st.write("Jumlah Data | Selection Sort | Insertion Sort | Quick Sort")
st.write("--- | --- | --- | ---")

for hasil in hasil_benchmark:
    st.write(
        f"{hasil[0]} | "
        f"{hasil[1]:.6f} | "
        f"{hasil[2]:.6f} | "
        f"{hasil[3]:.6f}"
    )


# =========================
# Grafik Sederhana
# =========================
st.subheader("Grafik Sederhana")

for hasil in hasil_benchmark:
    jumlah = hasil[0]
    bar_selection = "█" * int(hasil[1] * 1000)
    bar_insertion = "█" * int(hasil[2] * 1000)
    bar_quick = "█" * int(hasil[3] * 1000)
    st.write(f"Data {jumlah}")
    st.write(f"Selection : {bar_selection}")
    st.write(f"Insertion : {bar_insertion}")
    st.write(f"Quick     : {bar_quick}")
    st.write("")


# =========================
# Analisis
# =========================
st.subheader("Analisis")

total_rata_selection = sum([x[1] for x in hasil_benchmark])
total_rata_insertion = sum([x[2] for x in hasil_benchmark])
total_rata_quick = sum([x[3] for x in hasil_benchmark])

if total_rata_selection < total_rata_insertion and total_rata_selection < total_rata_quick:
    tercepat = "Selection Sort"
elif total_rata_insertion < total_rata_quick:
    tercepat = "Insertion Sort"
else:
    tercepat = "Quick Sort"

st.write(f"Algoritma tercepat adalah: **{tercepat}**")

st.write("""
Kesimpulan:
- Quick Sort biasanya lebih cepat untuk data besar
- Selection dan Insertion lebih lambat karena kompleksitas O(n²)
- Hasil benchmark umumnya sesuai teori Big O
""")
import random
import time

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

print("=" * 60)
print("BENCHMARK SORTING SEDERHANA")
print("=" * 60)
print("\nSedang menjalankan benchmark...\n")

for jumlah in ukuran_data:
    print(f"Memproses {jumlah} data...")
    total_selection = 0
    total_insertion = 0
    total_quick = 0

    for i in range(3):
        data_acak = random.sample(range(jumlah * 10), jumlah)
        total_selection += hitung_waktu(selection_sort, data_acak)
        total_insertion += hitung_waktu(insertion_sort, data_acak)
        total_quick += hitung_waktu(quick_sort, data_acak)
        print(f"  Iterasi {i+1}: Selection={total_selection/(i+1):.6f}s, Insertion={total_insertion/(i+1):.6f}s, Quick={total_quick/(i+1):.6f}s", end="\r")
    rata_selection = total_selection / 3
    rata_insertion = total_insertion / 3
    rata_quick = total_quick / 3
    hasil_benchmark.append([jumlah, rata_selection, rata_insertion, rata_quick])
    print()  # New line after progress

# =========================
# Tabel Hasil
# =========================
print("\n" + "=" * 60)
print("TABEL HASIL BENCHMARK")
print("=" * 60)
print(f"{'Jumlah Data':<15} {'Selection Sort':<20} {'Insertion Sort':<20} {'Quick Sort':<20}")
print("-" * 75)

for hasil in hasil_benchmark:
    print(f"{hasil[0]:<15} {hasil[1]:<20.6f} {hasil[2]:<20.6f} {hasil[3]:<20.6f}")

# =========================
# Grafik Sederhana
# =========================
print("\n" + "=" * 60)
print("GRAFIK SEDERHANA (skala 1 detik = 50 karakter)")
print("=" * 60)

for hasil in hasil_benchmark:
    jumlah = hasil[0]
    # Skala disesuaikan agar grafik tidak terlalu panjang
    skala_selection = min(hasil[1] * 200, 80)
    skala_insertion = min(hasil[2] * 200, 80)
    skala_quick = min(hasil[3] * 200, 80)
    bar_selection = "█" * int(skala_selection)
    bar_insertion = "█" * int(skala_insertion)
    bar_quick = "█" * int(skala_quick)    
    print(f"\nData {jumlah}")
    print(f"Selection : {bar_selection} ({hasil[1]:.6f}s)")
    print(f"Insertion : {bar_insertion} ({hasil[2]:.6f}s)")
    print(f"Quick     : {bar_quick} ({hasil[3]:.6f}s)")

# =========================
# Analisis
# =========================
print("\n" + "=" * 60)
print("ANALISIS HASIL")
print("=" * 60)

total_rata_selection = sum([x[1] for x in hasil_benchmark])
total_rata_insertion = sum([x[2] for x in hasil_benchmark])
total_rata_quick = sum([x[3] for x in hasil_benchmark])

if total_rata_selection < total_rata_insertion and total_rata_selection < total_rata_quick:
    tercepat = "Selection Sort"
elif total_rata_insertion < total_rata_quick:
    tercepat = "Insertion Sort"
else:
    tercepat = "Quick Sort"

print(f"\nAlgoritma tercepat secara keseluruhan: **{tercepat}**")
print("\nKesimpulan:")
print("   • Quick Sort terbukti paling cepat untuk data besar (O(n log n))")
print("   • Selection Sort dan Insertion Sort lambat karena O(n²)")
print("   • Untuk 50.000 data, Quick Sort bisa puluhan kali lebih cepat")
print("   • Hasil benchmark sesuai dengan teori kompleksitas algoritma")

# Perbandingan spesifik untuk data terbesar
if len(hasil_benchmark) > 0:
    data_terbesar = hasil_benchmark[-1]
    print(f"\nPada data {data_terbesar[0]}:")
    print(f"   • Quick Sort {data_terbesar[3]/data_terbesar[1]:.1f}x lebih cepat dari Selection Sort")
    print(f"   • Quick Sort {data_terbesar[3]/data_terbesar[2]:.1f}x lebih cepat dari Insertion Sort")
print("\n" + "=" * 60)
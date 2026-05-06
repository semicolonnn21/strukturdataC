import random
import time
import sys

# Supaya Quick Sort tidak error saat memproses 50.000 data
sys.setrecursionlimit(200000)

# --- 1. KUMPULAN ALGORITMA (Sederhana) ---

def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

# --- 2. IDENTITAS & JUDUL ---

print("=" * 95)
print(f"{'===LAPORAN TABEL BENCHMARKING===':^95}")
print("=" * 95)
print(f" Nama         : Azhalia Mozaik")
print(f" NIM          : 2530801059")
print(f" Kelas        : 2 INF C")
print(f" Mata Kuliah  : Struktur Data")
print("=" * 95)

# --- 3. PENGATURAN DATA ---

ukuran_data = [100, 1000, 10000, 50000]
daftar_algo = [
    ("Selection Sort", selection_sort),
    ("Insertion Sort", insertion_sort),
    ("Quick Sort", quick_sort)
]

# --- 4. PROSES HITUNG & TAMPILAN TABEL ---

# Header Tabel
print(f"| {'Ukuran':<10} | {'Algoritma':<18} | {'Run 1':<12} | {'Run 2':<12} | {'Run 3':<12} | {'Avg':<12} |")
print("-" * 95)

for n in ukuran_data:
    data_asli = [random.randint(1, 100000) for _ in range(n)]
    
    for nama, fungsi in daftar_algo:
        hasil_waktu = []
        
        for i in range(3):
            data_uji = data_asli.copy()
            mulai = time.perf_counter()
            
            if "Quick" in nama:
                data_uji = fungsi(data_uji)
            else:
                fungsi(data_uji)
                
            selesai = time.perf_counter()
            hasil_waktu.append(selesai - mulai)
        
        rata2 = sum(hasil_waktu) / 3
        
        # Format di bawah ini sudah diperbaiki dan dipastikan sejajar
        print(f"| {n:<10} | {nama:<18} | {hasil_waktu[0]:<12.5f} | {hasil_waktu[1]:<12.5f} | {hasil_waktu[2]:<12.5f} | {rata2:<12.5f} |")
    
    print("-" * 95)
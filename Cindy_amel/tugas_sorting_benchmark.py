import time
import random
import sys
import matplotlib.pyplot as plt

# Tambah limit rekursi untuk Quick Sort pada data besar
sys.setrecursionlimit(100000)

# --- IDENTITAS ---
nama_mhs = "Cindy Amelia"
nim_mhs  = "2530801071"
kelas    = "Informatika 2C"

# --- FUNGSI SORTING ---
def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i-1
        while j >= 0 and key < arr[j]:
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

# --- TAMPILAN HEADER ---
print("="*95)
print(f"{'ANALISIS ALGORITMA SORTING STRUKTUR DATA':^95}")
print("="*95)
print(f" Nama  : {nama_mhs}")
print(f" NIM   : {nim_mhs}")
print(f" Kelas : {kelas}")
print("="*95)

# --- KONFIGURASI PENGUJIAN ---
sizes = [100, 1000, 10000, 50000]
algorithms = ["Selection Sort", "Insertion Sort", "Quick Sort"]
results = {name: [] for name in algorithms}

# Header tabel dengan jarak yang sudah diperlebar agar Avg kelihatan
print(f"| {'Ukuran':<8} | {'Algoritma':<18} | {'Run 1':<12} | {'Run 2':<12} | {'Run 3':<12} | {'Avg':<12} |")
print("-" * 95)

# --- PROSES BENCHMARKING ---
for size in sizes:
    data_original = [random.randint(0, 100000) for _ in range(size)]
    
    for name in algorithms:
        runs = []
        for _ in range(3):
            data_test = data_original.copy()
            start = time.time()
            
            if name == "Selection Sort": 
                selection_sort(data_test)
            elif name == "Insertion Sort": 
                insertion_sort(data_test)
            elif name == "Quick Sort": 
                data_test = quick_sort(data_test)
            
            end = time.time()
            runs.append(end - start)
        
        avg = sum(runs) / 3
        results[name].append(avg)
        
        # Cetak baris dengan format 5 angka di belakang koma agar muat
        print(f"| {size:<8} | {name:<18} | {runs[0]:<12.5f} | {runs[1]:<12.5f} | {runs[2]:<12.5f} | {avg:<12.5f} |")
    
    print("-" * 95)

print(f"\n{'PENGUJIAN SELESAI':^95}")
print("="*95)

# --- VISUALISASI GRAFIK ---
plt.figure(figsize=(10, 6))
for name in algorithms:
    plt.plot(sizes, results[name], marker='o', linewidth=2, label=name)

plt.title(f'Sorting Benchmark - {nama_mhs}', fontsize=14)
plt.xlabel('Ukuran Data (n)', fontsize=12)
plt.ylabel('Waktu Eksekusi (detik)', fontsize=12)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.show()

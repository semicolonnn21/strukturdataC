import time
import random
import sys

# Meningkatkan batas rekursi agar Quick Sort aman untuk data besar
sys.setrecursionlimit(100000)


# --- Algoritma Bubble Sort ---
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr


# --- Algoritma Insertion Sort ---
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


# --- Algoritma Quick Sort ---
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + right


# --- Fungsi Benchmark ---
def run_benchmark(algorithms, sizes):
    for algo_name, algo_func in algorithms.items():
        print(f"\n=== Menjalankan Benchmark: {algo_name} ===")
        print(f"{'Jumlah Data':<15} | {'Percobaan':<10} | {'Waktu (Detik)':<15}")
        print("-" * 45)

        for size in sizes:
            for i in range(1, 4):  # 3 kali eksekusi sesuai permintaan
                # Generate data acak baru untuk setiap ukuran (tapi konsisten antar algoritma)
                data = [random.randint(0, 100000) for _ in range(size)]

                start_time = time.time()
                algo_func(
                    data.copy()
                )  # Menggunakan .copy() agar list asli tidak berubah
                end_time = time.time()

                durasi = end_time - start_time
                print(f"{size:<15,} | Ke-{i:<8} | {durasi:<15.6f}")
            print("-" * 15 + " | " + "-" * 10 + " | " + "-" * 15)


# Konfigurasi Dataset
test_sizes = [100, 1000, 10000, 50000]

# Daftar Algoritma
algos = {
    "Bubble Sort": bubble_sort,
    "Insertion Sort": insertion_sort,
    "Quick Sort": quick_sort,
}

# Mulai Tes
run_benchmark(algos, test_sizes)

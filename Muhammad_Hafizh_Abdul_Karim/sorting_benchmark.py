import time
import random

# ============================================================
# ALGORITMA SORTING
# ============================================================

def insertion_sort(arr):
    arr = arr.copy()
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def selection_sort(arr):
    arr = arr.copy()
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

def quick_sort(arr):
    arr = arr.copy()
    _quick_sort_helper(arr, 0, len(arr) - 1)
    return arr

def _quick_sort_helper(arr, low, high):
    if low < high:
        pi = _partition(arr, low, high)
        _quick_sort_helper(arr, low, pi - 1)
        _quick_sort_helper(arr, pi + 1, high)

def _partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

# ============================================================
# BENCHMARK
# ============================================================

data_sizes = [100, 1000, 10000]  # 50000 dilewati
algorithms = {
    "Insertion Sort": insertion_sort,
    "Selection Sort": selection_sort,
    "Quick Sort":     quick_sort,
}
RUNS = 3

print("=" * 65)
print(f"{'SORTING BENCHMARK':^65}")
print("=" * 65)
print(f"Dijalankan {RUNS}x per algoritma per ukuran data")
print(f"Angka di-random berbeda setiap run")
print("=" * 65)

results = {}  # results[algo][size] = avg_time

for algo_name, algo_func in algorithms.items():
    results[algo_name] = {}
    print(f"\n>>> {algo_name}")
    print("-" * 65)

    for size in data_sizes:
        times = []

        for run in range(1, RUNS + 1):
            data = random.sample(range(1, size * 10), size)  # angka random berbeda tiap run
            start = time.perf_counter()
            algo_func(data)
            elapsed = time.perf_counter() - start
            times.append(elapsed)
            print(f"  n={size:>6} | Run {run}: {elapsed:.6f} detik")

        avg = sum(times) / RUNS
        results[algo_name][size] = avg
        print(f"  n={size:>6} | Rata-rata: {avg:.6f} detik  <<<")

# ============================================================
# TABEL RINGKASAN
# ============================================================

print("\n")
print("=" * 65)
print(f"{'TABEL RATA-RATA WAKTU EKSEKUSI (detik)':^65}")
print("=" * 65)
header = f"{'Algoritma':<20}" + "".join(f"{'n='+str(s):>15}" for s in data_sizes)
print(header)
print("-" * 65)
for algo_name in algorithms:
    row = f"{algo_name:<20}"
    for size in data_sizes:
        row += f"{results[algo_name][size]:>15.6f}"
    print(row)
print("=" * 65)

print("\n[INFO] Ukuran data n=50.000 tidak dijalankan (terlalu berat untuk Insertion Sort & Selection Sort).")
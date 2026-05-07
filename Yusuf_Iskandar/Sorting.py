import random
import time

# ============================================================
#  SORTING FUNCTIONS
# ============================================================

def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def quick_sort(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)
        quick_sort(arr, low, pi - 1)
        quick_sort(arr, pi + 1, high)
    return arr

def partition(arr, low, high):
    mid = (low + high) // 2
    arr[mid], arr[high] = arr[high], arr[mid]
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

# ============================================================
#  KONFIGURASI
# ============================================================

SIZES   = [100, 1000, 10000]
RUNS    = 3
METHODS = {
    "Selection Sort": lambda a: selection_sort(a),
    "Insertion Sort": lambda a: insertion_sort(a),
    "Quick Sort"    : lambda a: quick_sort(a, 0, len(a) - 1),
}

# results[size][method] = [r1, r2, r3]
results = {size: {m: [] for m in METHODS} for size in SIZES}

# ============================================================
#  JALANKAN BENCHMARK
# ============================================================

for size in SIZES:
    for run in range(1, RUNS + 1):
        data_fresh = [random.randint(1, 100_000) for _ in range(size)]
        for method_name, sort_fn in METHODS.items():
            data_copy = data_fresh.copy()
            start     = time.perf_counter()
            sort_fn(data_copy)
            elapsed   = time.perf_counter() - start
            results[size][method_name].append(elapsed)

# ============================================================
#  TABEL BENCHMARKING LENGKAP
# ============================================================

SEP = "+" + "-"*18 + "+" + "-"*13 + "+" + "-"*13 + "+" + "-"*13 + "+" + "-"*13 + "+"

print("=" * 75)
print("   TABEL BENCHMARKING LENGKAP (waktu dalam detik)")
print("=" * 75)

for size in SIZES:
    print(f"\n  [[ {size:,} DATA ]]")
    print(f"  {SEP}")
    print(f"  | {'Metode':<16} | {'Run 1':>11} | {'Run 2':>11} | {'Run 3':>11} | {'Rata-rata':>11} |")
    print(f"  {SEP}")
    for method_name in METHODS:
        times = results[size][method_name]
        avg   = sum(times) / RUNS
        r1, r2, r3 = times
        print(f"  | {method_name:<16} | {r1:>11.6f} | {r2:>11.6f} | {r3:>11.6f} | {avg:>11.6f} |")
    print(f"  {SEP}")

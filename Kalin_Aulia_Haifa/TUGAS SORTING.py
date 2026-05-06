import time
import random

# Algoritma

def selection_sort(arr):
    arr = arr[:]
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

def insertion_sort(arr):
    arr = arr[:]
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left  = [x for x in arr if x < pivot]
    mid   = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + mid + quick_sort(right)



DATA_SIZES = [100, 1_000, 10_000, 50_000]
REPEAT     = 3
ALGORITHMS = [
    ("Selection", selection_sort),
    ("Insertion", insertion_sort),
    ("Quick Sort",     quick_sort),
]

#Benchmark 

results = {name: {n: [] for n in DATA_SIZES} for name, _ in ALGORITHMS}

for size in DATA_SIZES:
    data = [random.randint(0, 1_000_000) for _ in range(size)]
    for name, func in ALGORITHMS:
        for _ in range(REPEAT):
            start = time.perf_counter()
            func(data)
            results[name][size].append(time.perf_counter() - start)

#Tabel

C       = 12
headers = ["Algorithm", "Data Size", "Run 1", "Run 2", "Run 3", "Rata-rata"]
sep     = "+" + "+".join("-" * (C + 2) for _ in headers) + "+"
sep_eq  = sep.replace("-", "=")

print(sep)
print("|" + "|".join(f" {h:^{C}} " for h in headers) + "|")
print(sep_eq)

for algo_name, _ in ALGORITHMS:
    for i, size in enumerate(DATA_SIZES):
        times = results[algo_name][size]
        avg   = sum(times) / len(times)
        label = algo_name if i == 0 else ""
        cols  = [f" {label:^{C}} ", f" {size:>{C},} "]
        cols += [f" {t:>{C}.6f} " for t in times]
        cols += [f" {avg:>{C}.6f} "]
        print("|" + "|".join(cols) + "|")
    print(sep)
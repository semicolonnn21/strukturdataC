import time
import random

def selection_sort(arr):
    arr = arr.copy()
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

def insertion_sort(arr):
    arr = arr.copy()
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = key
    return arr

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr)//2]
    left = [x for x in arr if x < pivot]
    mid  = [x for x in arr if x == pivot]
    right= [x for x in arr if x > pivot]
    return quick_sort(left) + mid + quick_sort(right)

def benchmark(func, data):
    start = time.perf_counter()
    func(data)
    end = time.perf_counter()
    return (end - start) * 1000  # ms

sizes = [100, 1000, 10000, 50000]
algorithms = {
    "Selection": selection_sort,
    "Insertion": insertion_sort,
    "Quick": quick_sort
}

results = {}

print("\nTABEL HASIL BENCHMARK (ms)")
print("-"*50)
print(f"{'Ukuran':>8} | {'Selection':>10} | {'Insertion':>10} | {'Quick':>10}")
print("-"*50)

for size in sizes:
    data = random.sample(range(size*10), size)
    results[size] = {}

    for name, func in algorithms.items():
        times = []
        for _ in range(3):
            times.append(benchmark(func, data))
        avg = sum(times) / 3
        results[size][name] = avg

    print(f"{size:>8} | {results[size]['Selection']:>10.2f} | {results[size]['Insertion']:>10.2f} | {results[size]['Quick']:>10.2f}")

print("\nGRAFIK SEDERHANA")
print("-"*50)

for size in sizes:
    print(f"\nUkuran {size}:")
    max_val = max(results[size].values())

    for name in algorithms:
        val = results[size][name]
        bar = "█" * int((val / max_val) * 30)
        print(f"{name:<10}: {bar} ({val:.2f} ms)")
import random
import time

def selection_sort(arr):
    a = arr.copy()
    n = len(a)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if a[j] < a[min_idx]:
                min_idx = j
        a[i], a[min_idx] = a[min_idx], a[i]
    return a

sizes = [100, 1000, 10000, 50000]

print("=== Selection Sort ===")

for size in sizes:
    if size == 60000:
        print(f"\nSize {size}: SKIPPED (terlalu lama)")
        continue

    data = [random.randint(1, 100000) for _ in range(size)]
    times = []

    print(f"\nSize {size}:")

    for i in range(3):
        start = time.perf_counter()
        selection_sort(data)
        end = time.perf_counter()

        duration = end - start
        times.append(duration)

        print(f"Run {i+1}: {duration:.6f} detik")

    avg = sum(times) / 3
    print(f"Rata-rata: {avg:.6f} detik")
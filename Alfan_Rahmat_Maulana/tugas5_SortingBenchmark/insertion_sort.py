import random
import time

def insertion_sort(arr):
    a = arr.copy()
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and key < a[j]:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a

sizes = [100, 1000, 10000, 50000]

print("=== Insertion Sort ===")

for size in sizes:
    if size == 100000:
        print(f"\nSize {size}: SKIPPED (terlalu lama)")
        continue

    data = [random.randint(1, 100000) for _ in range(size)]
    times = []

    print(f"\nSize {size}:")

    for i in range(3):
        start = time.perf_counter()
        insertion_sort(data)
        end = time.perf_counter()

        duration = end - start
        times.append(duration)

        print(f"Run {i+1}: {duration:.6f} detik")

    avg = sum(times) / 3
    print(f"Rata-rata: {avg:.6f} detik")
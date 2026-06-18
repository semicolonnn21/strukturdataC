import random
import time

def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result

sizes = [100, 1000, 10000, 50000]

print("=== Merge Sort ===")

for size in sizes:
    data = [random.randint(1, 100000) for _ in range(size)]
    times = []

    print(f"\nSize {size}:")

    for i in range(3):
        start = time.perf_counter()
        merge_sort(data)
        end = time.perf_counter()

        duration = end - start
        times.append(duration)

        print(f"Run {i+1}: {duration:.6f} detik")

    avg = sum(times) / 3
    print(f"Rata-rata: {avg:.6f} detik")
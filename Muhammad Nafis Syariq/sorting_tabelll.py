import random
import time

def selection_sort(arr):
    data = arr.copy()
    for i in range(len(data)):
        min_idx = i
        for j in range(i+1, len(data)):
            if data[j] < data[min_idx]:
                min_idx = j
        data[i], data[min_idx] = data[min_idx], data[i]
    return data


def insertion_sort(arr):
    data = arr.copy()
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        while j >= 0 and data[j] > key:
            data[j+1] = data[j]
            j -= 1
        data[j+1] = key
    return data


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
repeat = 3

print("\n=== TABEL BENCHMARKING ===")
print("-" * 95)
print(f"{'Ukuran':<8} | {'Algoritma':<15} | {'Run 1':<10} | {'Run 2':<10} | {'Run 3':<10} | {'Avg':<10}")
print("-" * 95)

for size in sizes:
    data = random.sample(range(size * 10), size)

    times = []
    for _ in range(repeat):
        start = time.perf_counter()
        selection_sort(data)
        times.append(time.perf_counter() - start)
    avg = sum(times) / repeat

    print(f"{size:<8} | {'Selection Sort':<15} | {times[0]:<10.6f} | {times[1]:<10.6f} | {times[2]:<10.6f} | {avg:<10.6f}")

    times = []
    for _ in range(repeat):
        start = time.perf_counter()
        insertion_sort(data)
        times.append(time.perf_counter() - start)
    avg = sum(times) / repeat

    print(f"{'':<8} | {'Insertion Sort':<15} | {times[0]:<10.6f} | {times[1]:<10.6f} | {times[2]:<10.6f} | {avg:<10.6f}")

    times = []
    for _ in range(repeat):
        start = time.perf_counter()
        merge_sort(data)
        times.append(time.perf_counter() - start)
    avg = sum(times) / repeat

    print(f"{'':<8} | {'Merge Sort':<15} | {times[0]:<10.6f} | {times[1]:<10.6f} | {times[2]:<10.6f} | {avg:<10.6f}")

    print("-" * 95)
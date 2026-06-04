import random
import time

# ======================
# SORTING
# ======================

def selection_sort(arr):
    a = arr.copy()
    for i in range(len(a)):
        min_idx = i
        for j in range(i+1, len(a)):
            if a[j] < a[min_idx]:
                min_idx = j
        a[i], a[min_idx] = a[min_idx], a[i]
    return a


def insertion_sort(arr):
    a = arr.copy()
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j+1] = a[j]
            j -= 1
        a[j+1] = key
    return a


def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr)//2]
    left = [x for x in arr if x < pivot]
    mid = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + mid + right


# ======================
# BENCHMARK
# ======================

sizes = [100, 1000, 10000, 50000]

algorithms = {
    "Selection": selection_sort,
    "Insertion": insertion_sort,
    "Quick": quick_sort
}

print("\n=== HASIL BENCHMARK SORTING ===\n")

for size in sizes:
    print(f"\nUkuran Data: {size}")
    print("-" * 60)
    print(f"{'Algoritma':<12} {'Run 1':<10} {'Run 2':<10} {'Run 3':<10} {'AVG':<10}")
    print("-" * 60)

    data = [random.randint(1, 100000) for _ in range(size)]

    for name, func in algorithms.items():
        times = []

        for i in range(3):
            arr_copy = data.copy()
            start = time.perf_counter()
            func(arr_copy)
            end = time.perf_counter()
            times.append(end - start)

        avg = sum(times) / 3

        print(f"{name:<12} "
              f"{times[0]:<10.6f} "
              f"{times[1]:<10.6f} "
              f"{times[2]:<10.6f} "
              f"{avg:<10.6f}")

    print("-" * 60)
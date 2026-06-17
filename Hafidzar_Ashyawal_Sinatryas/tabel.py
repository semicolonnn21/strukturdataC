import time
import random

# 1. Selection Sort
def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

# 2. Insertion Sort
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

# 3. Quick Sort
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

def run_benchmark():
    sizes = [100, 1000, 10000, 50000]
    algorithms = [
        ("Selection Sort", selection_sort),
        ("Insertion Sort", insertion_sort),
        ("Quick Sort", quick_sort)
    ]

    print(f"{'Algoritma':<20} | {'Ukuran Data':<12} | {'Rata-rata Waktu (detik)':<25}")
    print("-" * 65)

    for name, algo in algorithms:
        for size in sizes:
            times = []
            # Menjalankan 3 kali sesuai instruksi
            for _ in range(3):
                test_data = [random.randint(0, 100000) for _ in range(size)]
                start_time = time.time()
                algo(test_data)
                end_time = time.time()
                times.append(end_time - start_time)
            
            avg_time = sum(times) / len(times)
            print(f"{name:<20} | {size:<12} | {avg_time:<25.6f}")

if __name__ == "__main__":
    run_benchmark()
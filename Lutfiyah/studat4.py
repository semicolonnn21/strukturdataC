import random
import time
import sys

sys.setrecursionlimit(200000)

def selection_sort(lst):
    arr = lst.copy()
    n = len(arr)
    for i in range(n - 1):
        min_index = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_index]:
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]
    return arr

def insertion_sort(lst):
    arr = lst.copy()
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def quick_sort(lst):
    if len(lst) <= 1:
        return lst
    pivot = lst[len(lst) // 2]
    left = [x for x in lst if x < pivot]
    middle = [x for x in lst if x == pivot]
    right = [x for x in lst if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

def jalankan_tes():
    daftar_ukuran = [100, 1000, 10000, 50000]
    
    print("=== HASIL BENCHMARK SORTING ===")
    # Header Utama hanya sekali di atas
    print("-" * 75)
    print(f"{'Data':<8} | {'Algoritma':<12} | {'Run 1':<10} | {'Run 2':<10} | {'Run 3':<10} | {'AVG':<10}")
    print("-" * 75)

    for size in daftar_ukuran:
        data_acak = [random.randint(1, 100000) for _ in range(size)]
        
        algoritma_list = [
            ("Selection", selection_sort),
            ("Insertion", insertion_sort),
            ("Quick", quick_sort)
        ]

        for nama, fungsi in algoritma_list:
            waktu_per_run = []
            for _ in range(3):
                test_data = data_acak.copy()
                mulai = time.perf_counter()
                fungsi(test_data)
                selesai = time.perf_counter()
                waktu_per_run.append(selesai - mulai)
            
            rata_rata = sum(waktu_per_run) / 3
            # Ukuran data hanya ditampilkan di baris pertama tiap blok
            size_label = size if nama == "Selection" else ""
            print(f"{size_label:<8} | {nama:<12} | {waktu_per_run[0]:.5f} | {waktu_per_run[1]:.5f} | {waktu_per_run[2]:.5f} | {rata_rata:.5f}")
        
        print("-" * 75) # Garis pemisah antar ukuran data

if __name__ == "__main__":
    jalankan_tes()
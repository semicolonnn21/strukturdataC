import time
import random
import sys

sys.setrecursionlimit(100000)

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

print("=== UJI QUICK SORT ===")
ukuran = int(input("Masukkan jumlah data yang ingin diuji: "))

data_acak = [random.randint(1, 100000) for _ in range(ukuran)]

print(f"\nData Sebelum Diurutkan:\n{data_acak}\n")
print("Memulai pengurutan...")

waktu_mulai = time.perf_counter()
data_terurut = quick_sort(data_acak.copy())
waktu_selesai = time.perf_counter()

print(f"\nData Sesudah Diurutkan:\n{data_terurut}\n")

waktu_eksekusi = waktu_selesai - waktu_mulai
print(f"Selesai! Waktu yang dibutuhkan: {waktu_eksekusi:.5f} detik")
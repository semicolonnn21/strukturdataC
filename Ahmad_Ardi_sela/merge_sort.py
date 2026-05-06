import time
import random

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
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

print("=== UJI MERGE SORT ===")
ukuran = int(input("Masukkan jumlah data yang ingin diuji: "))

data_acak = [random.randint(1, 100) for _ in range(ukuran)]

print(f"\nData Sebelum Diurutkan:\n{data_acak}\n")
print("Memulai pengurutan...")

waktu_mulai = time.perf_counter()
data_terurut = merge_sort(data_acak.copy())
waktu_selesai = time.perf_counter()

print(f"\nData Sesudah Diurutkan:\n{data_terurut}\n")

waktu_eksekusi = waktu_selesai - waktu_mulai
print(f"Selesai! Waktu yang dibutuhkan: {waktu_eksekusi:.5f} detik")
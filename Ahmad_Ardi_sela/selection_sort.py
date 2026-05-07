import time
import random

def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

print("=== UJI SELECTION SORT ===")
ukuran = int(input("Masukkan jumlah data yang ingin diuji: "))

data_acak = [random.randint(1, 100000) for _ in range(ukuran)]

print(f"\nData Sebelum Diurutkan:\n{data_acak}\n")
print("Memulai pengurutan...")


waktu_mulai = time.perf_counter()
data_terurut = selection_sort(data_acak.copy()) 
waktu_selesai = time.perf_counter()

print(f"\nData Sesudah Diurutkan:\n{data_terurut}\n")


waktu_eksekusi = waktu_selesai - waktu_mulai
print(f"Selesai! Waktu yang dibutuhkan: {waktu_eksekusi:.5f} detik")
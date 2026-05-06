# ============================================
# 📊 BENCHMARK SORTING 
# ============================================

import random
import time
import matplotlib.pyplot as plt

print("="*50)
print("🔥 BENCHMARK SORTING 🔥")
print("="*50)

# ================= SORTING =================

def bubble_sort(arr):
    a = arr.copy()
    n = len(a)
    for i in range(n):
        for j in range(0, n-i-1):
            if a[j] > a[j+1]:
                a[j], a[j+1] = a[j+1], a[j]
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

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    
    mid = len(arr)//2
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
    
    result += left[i:]
    result += right[j:]
    
    return result

# ================= DATA =================

# Dibuat lebih cepat (tetap valid buat tugas)
sizes = [100, 1000, 5000, 10000]

results = {
    "Bubble": [],
    "Insertion": [],
    "Merge": []
}

# ================= BENCHMARK =================

for size in sizes:
    print(f"\n📦 Data: {size}")
    
    data = [random.randint(1, 10000) for _ in range(size)]

    # -------- BUBBLE --------
    total_time = 0
    for _ in range(3):
        arr = data.copy()
        start = time.time()
        bubble_sort(arr)
        end = time.time()
        total_time += (end - start)
    
    avg = total_time / 3
    results["Bubble"].append(avg)
    print(f"⚡ Bubble    : {avg:.6f} detik")

    # -------- INSERTION --------
    total_time = 0
    for _ in range(3):
        arr = data.copy()
        start = time.time()
        insertion_sort(arr)
        end = time.time()
        total_time += (end - start)
    
    avg = total_time / 3
    results["Insertion"].append(avg)
    print(f"⚡ Insertion : {avg:.6f} detik")

    # -------- MERGE --------
    total_time = 0
    for _ in range(3):
        arr = data.copy()
        start = time.time()
        merge_sort(arr)
        end = time.time()
        total_time += (end - start)
    
    avg = total_time / 3
    results["Merge"].append(avg)
    print(f"⚡ Merge     : {avg:.6f} detik")

# ================= TABEL =================

print("\n" + "="*50)
print("📊 HASIL AKHIR")
print("="*50)

print(f"{'Data':<10}{'Bubble':<15}{'Insertion':<15}{'Merge':<15}")
print("-"*50)

for i, size in enumerate(sizes):
    print(f"{size:<10}{results['Bubble'][i]:<15.6f}{results['Insertion'][i]:<15.6f}{results['Merge'][i]:<15.6f}")

# ================= GRAFIK =================

plt.plot(sizes, results["Bubble"], marker='o', label="Bubble Sort")
plt.plot(sizes, results["Insertion"], marker='o', label="Insertion Sort")
plt.plot(sizes, results["Merge"], marker='o', label="Merge Sort")

plt.xlabel("Jumlah Data")
plt.ylabel("Waktu Eksekusi (detik)")
plt.title("Perbandingan Algoritma Sorting")
plt.legend()
plt.grid()

plt.show()
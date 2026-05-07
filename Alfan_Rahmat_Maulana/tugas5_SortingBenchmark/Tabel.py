import random
import time

# =========================
# Sorting Algorithms
# =========================

def selection_sort(arr):
    a = arr.copy()
    n = len(a)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if a[j] < a[min_idx]:
                min_idx = j
        a[i], a[min_idx] = a[min_idx], a[i]
    return a

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

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr)//2
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

# =========================
# Benchmark
# =========================

sizes = [100, 1000, 10000, 50000]

results = {
    "Selection": [],
    "Insertion": [],
    "Merge": []
}

for size in sizes:
    data = [random.randint(1, 100000) for _ in range(size)]

    # Selection Sort
    if size == 50000:
        results["Selection"].append("-")
    else:
        times = []
        for _ in range(3):
            start = time.perf_counter()
            selection_sort(data)
            end = time.perf_counter()
            times.append(end - start)
        results["Selection"].append(sum(times)/3)

    # Insertion Sort
    if size == 50000:
        results["Insertion"].append("-")
    else:
        times = []
        for _ in range(3):
            start = time.perf_counter()
            insertion_sort(data)
            end = time.perf_counter()
            times.append(end - start)
        results["Insertion"].append(sum(times)/3)

    # Merge Sort
    times = []
    for _ in range(3):
        start = time.perf_counter()
        merge_sort(data)
        end = time.perf_counter()
        times.append(end - start)
    results["Merge"].append(sum(times)/3)

# =========================
# TABEL HASIL
# =========================

print("\n=== TABEL HASIL BENCHMARKING ===")
print("Ukuran\tSelection\tInsertion\tMerge")

for i in range(len(sizes)):
    sel = results["Selection"][i]
    ins = results["Insertion"][i]
    mer = results["Merge"][i]

    sel_str = f"{sel:.6f}" if sel != "-" else "-"
    ins_str = f"{ins:.6f}" if ins != "-" else "-"
    mer_str = f"{mer:.6f}"

    print(f"{sizes[i]}\t{sel_str}\t\t{ins_str}\t\t{mer_str}")
import random
import time

data = random.sample(range(1, 50001), 50000)

print("Data awal: ",data)

def selection(lst):
    n = len(lst)
    for i in range(n - 1):
        min_index = i
        for j in range(i + 1, n):
            if lst[j] < lst[min_index]:
                min_index = j
        lst[i], lst[min_index] = lst[min_index], lst[i]
    return lst


start = time.perf_counter()
data = selection(data)
end = time.perf_counter()
execution = end - start

print("Data setelah diurutkan: ", data)
print(f"waktu eksekusi: {execution:.6f} detik")
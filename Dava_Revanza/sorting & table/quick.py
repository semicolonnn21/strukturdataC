import random
import time

data = random.sample(range(1, 50001), 50000)

print("Data awal: ",data)

def quick(lst):
    if len(lst) <= 1:
        return lst
    else:
        pivot = lst[len(lst) // 2] 
        left = [x for x in lst if x < pivot]
        middle = [x for x in lst if x == pivot]
        right = [x for x in lst if x > pivot]
        return quick(left) + middle + quick(right)

start = time.perf_counter()
data = quick(data)
end = time.perf_counter()
execution = end - start

print("Data setelah diurutkan: ", data)
print(f"waktu eksekusi: {execution:.6f} detik")
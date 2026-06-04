import random
import time

data = random.sample(range(1, 50001), 50000)

print("Data awal: ",data)

def insertion(lst):
    for i in range(1, len(lst)):
        key = lst[i]
        j = i - 1
        while j >= 0 and lst[j] > key:
            lst[j + 1] = lst[j]
            j -= 1
        lst[j + 1] = key
    return lst

start = time.perf_counter()
data = insertion(data)
end = time.perf_counter()
execution = end - start

print("Data setelah diurutkan: ", data)
print(f"waktu eksekusi: {execution:.6f} detik")
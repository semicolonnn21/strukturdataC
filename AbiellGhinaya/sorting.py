import random
import time
import sys

#proses bubble sort
def bubble_sort(lis):
    for i in range(len(lis)-1, 0, -1):
        swap = False
        for j in range(i):
            if lis[j] > lis[j+1]:
                temp = lis[j]
                lis[j] = lis[j+1]
                lis[j+1] = temp
                swap = True
            
        if not swap:
            break

#proses merge sort
def merge_sort(serot):
    if len(serot) > 1: #pengecekan index nya ada lebih dari 1
        mmin = len(serot)//2
        kiri = serot[: mmin]
        kanan = serot[mmin :]

        merge_sort(kiri)
        merge_sort(kanan) # fungsi rekusrsif
    
        i = 0
        j = 0
        k = 0

        while i < len(kiri) and j < len(kanan): #pengecekan array kiri dan kanan
            if kiri[i] < kanan[j]:
                serot[k] = kiri[i]
                i += 1
            else:
                serot[k] = kanan[j]
                j += 1
            k += 1
            
        #membersihkan sisa di list kiri
        while i < len(kiri):
            serot[k] = kiri[i]
            i += 1
            k += 1

        #membersihkan sisa di list kanan
        while j < len(kanan):
            serot[k] = kanan[j]
            j += 1
            k += 1

#proses quick sort
def quick_sort(arr, kiri, kanan):
    if kiri < kanan: #pengecekan indeks nya ada lebih satu
        posisi_pivot = eksekusi(arr, kiri, kanan) #memanggi fungsi eksekusi
        quick_sort(arr, kiri, posisi_pivot - 1) #membereskan sisi kiri (sebelum pivot)
        quick_sort(arr, posisi_pivot + 1, kanan) #membereskan sisi kanan (setelah pivot)

def eksekusi(arr, kiri, kanan):
    i = kiri
    j = kanan - 1
    pivot = arr[kanan]

    while i <= j:
        while i <= j and arr[i] < pivot:
            i += 1
        while i <= j and arr[j] >= pivot:
            j -= 1

        if i < j:
            temp = arr[i]
            arr[i] = arr[j]
            arr[j] = temp
    
    if arr[i] > pivot:
        temp = arr[i]
        arr[i] = arr[kanan]
        arr[kanan] = temp

    return i

# --- PROSES BENCHMARKING ---

def run_benchmark():
    ukuran_data = [100, 1000, 10000]
    hasil = {"Bubble": [], "Merge": [], "Quick": []}

    print(f"\n{'UKURAN':<10} | {'BUBBLE (s)':<12} | {'MERGE (s)':<12} | {'QUICK (s)':<12}")
    print("-" * 60)

    for n in ukuran_data:
        t_bubble, t_merge, t_quick = [], [], [] #list untuk menyimpan waktu sorting

        for _ in range(3): 
            #proses pembuatan data random sesuai ukuran yang diminta
            data_asli = [random.randint(1, 100000) for _ in range(n)]

            #test Bubble
            copy_b = data_asli.copy() #mengcopy data agar bisa dipakai banyak sorting
            mulai = time.time()
            bubble_sort(copy_b)
            t_bubble.append(time.time() - mulai) #waktu selesai - waktu muali

            #test Merge
            copy_m = data_asli.copy()
            mulai = time.time()
            merge_sort(copy_m)
            t_merge.append(time.time() - mulai)

            #test Quick
            copy_q = data_asli.copy()
            sys.setrecursionlimit(20000)
            mulai = time.time()
            quick_sort(copy_q, 0, len(copy_q)-1)
            t_quick.append(time.time() - mulai)

        #simpan rata-rata
        jml_b = sum(t_bubble)/3 #menghitung jumlah waktu yang diulang sebanyak 3 kali
        jml_m = sum(t_merge)/3
        jml_q = sum(t_quick)/3

        hasil["Bubble"].append(jml_b) #menambahkan hasil jumlah tadi ke dalam dictionary
        hasil["Merge"].append(jml_m)
        hasil["Quick"].append(jml_q)

        print(f"{n:<10} | {jml_b:<12.5f} | {jml_m:<12.5f} | {jml_q:<12.5f}")

# --- VISUALISASI ---
    print("\nVISUALISASI PERFORMA")
    print("Semakin panjang '#' semakin lambat")
    print("-" * 60)
    
    #kita pakai Bubble Sort 10.000 sebagai patokan panjang bar (skala)
    skala = 50 / max(hasil["Bubble"]) if max(hasil["Bubble"]) > 0 else 1
    
    for nama, data_waktu in hasil.items():
        waktu_akhir = data_waktu[-1] #ambil hasil di 10.000 data
        bar = "#" * int(waktu_akhir * skala)
        print(f"{nama:<10} | {bar} ({waktu_akhir:.5f} s)")

if __name__ == "__main__":
    run_benchmark()
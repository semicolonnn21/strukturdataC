import random
import time

# ==================================
# SELECTION SORT
# ==================================

def sort_selection(data_input):
    data = data_input.copy()
    panjang = len(data)

    for posisi in range(panjang):
        minimum = posisi

        for cek in range(posisi + 1, panjang):
            if data[cek] < data[minimum]:
                minimum = cek

        data[posisi], data[minimum] = data[minimum], data[posisi]

    return data


# ==================================
# INSERTION SORT
# ==================================

def sort_insertion(data_input):
    data = data_input.copy()

    for i in range(1, len(data)):
        current = data[i]
        j = i - 1

        while j >= 0 and current < data[j]:
            data[j + 1] = data[j]
            j -= 1

        data[j + 1] = current

    return data


# ==================================
# QUICK SORT
# ==================================

def sort_quick(data_input):

    if len(data_input) <= 1:
        return data_input

    pivot = data_input[len(data_input) // 2]

    bagian_kiri = [x for x in data_input if x < pivot]
    bagian_tengah = [x for x in data_input if x == pivot]
    bagian_kanan = [x for x in data_input if x > pivot]

    return (
        sort_quick(bagian_kiri)
        + bagian_tengah
        + sort_quick(bagian_kanan)
    )


# ==================================
# MENGUKUR WAKTU EKSEKUSI
# ==================================

def ukur_waktu(fungsi, dataset):
    awal = time.time()
    fungsi(dataset)
    akhir = time.time()

    return akhir - awal


# ==================================
# BENCHMARK
# ==================================

jumlah_data = [100, 1000, 10000, 50000]

rekap_hasil = []

print("=" * 65)
print("PENGUJIAN PERFORMA ALGORITMA SORTING")
print("=" * 65)

for ukuran in jumlah_data:

    print(f"\nMenguji dataset sebanyak {ukuran} data")

    waktu_selection = 0
    waktu_insertion = 0
    waktu_quick = 0

    for percobaan in range(3):

        angka_random = random.sample(
            range(ukuran * 10),
            ukuran
        )

        waktu_selection += ukur_waktu(
            sort_selection,
            angka_random
        )

        waktu_insertion += ukur_waktu(
            sort_insertion,
            angka_random
        )

        waktu_quick += ukur_waktu(
            sort_quick,
            angka_random
        )

    rata_selection = waktu_selection / 3
    rata_insertion = waktu_insertion / 3
    rata_quick = waktu_quick / 3

    rekap_hasil.append(
        [
            ukuran,
            rata_selection,
            rata_insertion,
            rata_quick
        ]
    )

# ==================================
# MENAMPILKAN TABEL
# ==================================

print("\n")
print("=" * 65)
print("HASIL BENCHMARK")
print("=" * 65)

print(
    f"{'Data':<12}"
    f"{'Selection':<18}"
    f"{'Insertion':<18}"
    f"{'Quick':<18}"
)

print("-" * 65)

for item in rekap_hasil:

    print(
        f"{item[0]:<12}"
        f"{item[1]:<18.6f}"
        f"{item[2]:<18.6f}"
        f"{item[3]:<18.6f}"
    )

# ==================================
# VISUALISASI SEDERHANA
# ==================================

print("\n")
print("=" * 65)
print("VISUALISASI WAKTU EKSEKUSI")
print("=" * 65)

for item in rekap_hasil:

    ukuran = item[0]

    grafik_sel = "█" * int(min(item[1] * 200, 80))
    grafik_ins = "█" * int(min(item[2] * 200, 80))
    grafik_qck = "█" * int(min(item[3] * 200, 80))

    print(f"\nDataset : {ukuran}")

    print(
        f"Selection : {grafik_sel} "
        f"({item[1]:.6f}s)"
    )

    print(
        f"Insertion : {grafik_ins} "
        f"({item[2]:.6f}s)"
    )

    print(
        f"Quick     : {grafik_qck} "
        f"({item[3]:.6f}s)"
    )

# ==================================
# ANALISIS
# ==================================

print("\n")
print("=" * 65)
print("KESIMPULAN")
print("=" * 65)

total_selection = sum(x[1] for x in rekap_hasil)
total_insertion = sum(x[2] for x in rekap_hasil)
total_quick = sum(x[3] for x in rekap_hasil)

hasil_total = {
    "Selection Sort": total_selection,
    "Insertion Sort": total_insertion,
    "Quick Sort": total_quick
}

algoritma_tercepat = min(
    hasil_total,
    key=hasil_total.get
)

print(
    f"\nAlgoritma tercepat: "
    f"{algoritma_tercepat}"
)

print("\nPenjelasan:")

print(
    "- Quick Sort umumnya unggul "
    "untuk jumlah data besar."
)

print(
    "- Selection Sort dan "
    "Insertion Sort memiliki "
    "kompleksitas O(n²)."
)

print(
    "- Semakin besar data, "
    "perbedaan waktu akan semakin terlihat."
)

if rekap_hasil:

    terbesar = rekap_hasil[-1]

    print(
        f"\nPerbandingan pada "
        f"{terbesar[0]} data:"
    )

    print(
        f"- Quick Sort sekitar "
        f"{terbesar[1] / terbesar[3]:.1f}x "
        f"lebih cepat dibanding Selection Sort"
    )

    print(
        f"- Quick Sort sekitar "
        f"{terbesar[2] / terbesar[3]:.1f}x "
        f"lebih cepat dibanding Insertion Sort"
    )

print("\n" + "=" * 65)
print("By: Wafah Khonia")
print("=" * 65)

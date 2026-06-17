# ================================
# IMPLEMENTASI HASHING SEDERHANA
# ================================

UKURAN_TABEL = 10

def fungsi_hash(kunci):
    return kunci % UKURAN_TABEL

def buat_tabel():
    return [None] * UKURAN_TABEL

def simpan_data(tabel, kunci, nilai):
    indeks = fungsi_hash(kunci)
    indeks_awal = indeks

    while tabel[indeks] is not None:
        if tabel[indeks][0] == kunci:
            tabel[indeks] = (kunci, nilai)
            print("Data berhasil diperbarui")
            return
        indeks = (indeks + 1) % UKURAN_TABEL
        if indeks == indeks_awal:
            print("Tabel penuh")
            return
    tabel[indeks] = (kunci, nilai)
    print("Data berhasil disimpan")

def cari_data(tabel, kunci):
    indeks = fungsi_hash(kunci)
    indeks_awal = indeks
    while tabel[indeks] is not None:
        if tabel[indeks][0] == kunci:
            return tabel[indeks][1]
        indeks = (indeks + 1) % UKURAN_TABEL
        if indeks == indeks_awal:
            break
    return None


def hapus_data(tabel, kunci):
    indeks = fungsi_hash(kunci)
    indeks_awal = indeks

    while tabel[indeks] is not None:
        if tabel[indeks][0] == kunci:
            tabel[indeks] = None
            print("Data berhasil dihapus")
            return
        indeks = (indeks + 1) % UKURAN_TABEL
        if indeks == indeks_awal:
            break
    print("Data tidak ditemukan")

def tampilkan_tabel(tabel):
    print("\nIsi Tabel Hash:")
    for i in range(UKURAN_TABEL):
        if tabel[i] is None:
            print(f"Indeks {i}: Kosong")
        else:
            print(f"Indeks {i}: {tabel[i]}")

# Program utama
tabel_hash = buat_tabel()

while True:
    print("\n=== MENU HASHING ===")
    print("1. Simpan Data")
    print("2. Cari Data")
    print("3. Hapus Data")
    print("4. Tampilkan Tabel")
    print("5. Keluar")

    pilihan = input("Pilih menu: ")

    if pilihan == "1":
        kunci = int(input("Masukkan kunci: "))
        nilai = input("Masukkan nilai: ")
        simpan_data(tabel_hash, kunci, nilai)
    elif pilihan == "2":
        kunci = int(input("Masukkan kunci yang dicari: "))
        hasil = cari_data(tabel_hash, kunci)
        if hasil:
            print("Data ditemukan:", hasil)
        else:
            print("Data tidak ditemukan")
    elif pilihan == "3":
        kunci = int(input("Masukkan kunci yang dihapus: "))
        hapus_data(tabel_hash, kunci)
    elif pilihan == "4":
        tampilkan_tabel(tabel_hash)
    elif pilihan == "5":
        print("Program selesai")
        break
    else:
        print("Pilihan tidak valid")
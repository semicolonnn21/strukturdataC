class Buku:
    def __init__(self, code, judul, pengarang, genre, stok=1, dipinjam=0):
        self.code = code
        self.judul = judul
        self.pengarang = pengarang
        self.genre = genre
        self.stok = stok
        self.dipinjam = dipinjam

    def tersedia(self):
        return self.stok - self.dipinjam

daftar = [
    Buku(101, "Laskar Pelangi", "Andrea Hirata", "Fiksi", stok=7, dipinjam=3),
    Buku(102, "Filosofi Teras", "Henry Manampiring", "Non-Fiksi", stok=9, dipinjam=1),
    Buku(103, "Bumi Manusia", "Pramoedya Ananta Toer", "Sejarah Fiksi", stok=5, dipinjam=2),
    Buku(104, "Negeri 5 Menara", "A. Fuadi", "Fiksi Remaja", stok=8, dipinjam=4),
    Buku(105, "Sapiens", "Yuval Noah Harari", "Non-Fiksi", stok=6, dipinjam=2),
    Buku(106, "Perahu Kertas", "Dee Lestari", "Romantis", stok=10, dipinjam=5),
    Buku(107, "Atomic Habits", "James Clear", "Pengembangan Diri", stok=12, dipinjam=3),
    Buku(108, "Ayat-Ayat Cinta", "Habiburrahman El Shirazy", "Religi", stok=4, dipinjam=1),
    Buku(109, "Rich Dad Poor Dad", "Robert T. Kiyosaki", "Keuangan", stok=7, dipinjam=2),
    Buku(110, "Cantik Itu Luka", "Eka Kurniawan", "Magical Realism", stok=3, dipinjam=1),
    Buku(111, "Deep Work", "Cal Newport", "Produktivitas", stok=5, dipinjam=0),
    Buku(112, "Sang Pemimpi", "Andrea Hirata", "Fiksi Remaja", stok=9, dipinjam=6)
]

def line(c, n):
    print(c * n)

def bersihkan():
    print("\033[2J\033[1;1H", end="")  

def tambah():
    bersihkan()

    print("Tambah Buku Baru")
    line("=", 40)

    try:
        code = int(input("Kode Buku      : "))
    except ValueError:
        print("Kode harus berupa angka.")
        return

    judul = input("Judul Buku     : ")
    pengarang = input("Pengarang      : ")
    genre = input("Genre          : ")
    try:
        stok = int(input("Stok           : "))
        if stok < 0:
            print("Stok tidak boleh negatif.")
            return
    except ValueError:
        print("Stok harus berupa angka.")
        return

    b = Buku(code, judul, pengarang, genre, stok=stok)
    daftar.append(b)

    print("\nBuku berhasil ditambahkan.")

def tampilSemua():
    bersihkan()

    if len(daftar) == 0:
        print("Tidak ada buku.")
        return

    print("DAFTAR BUKU")
    line("=", 120)

    print(f"{'Kode':<8}{'Judul':<30}{'Pengarang':<30}{'Genre':<25}{'Stok':<7}{'Dipinjam':<11}{'Status':<12}")
    line("=", 120)

    for b in daftar:
        status = "Kosong" if b.tersedia() == 0 else ("Tersedia" if b.tersedia() > 0 else "Tidak tersedia")
        print(f"{b.code:<8}{b.judul:<30}{b.pengarang:<30}{b.genre:<25}{b.stok:<7}{b.dipinjam:<11}{status:<12}")

    line("=", 120)

def cari(kode):
    for i in range(len(daftar)):
        if daftar[i].code == kode:
            return i
    return -1

def pinjam():
    bersihkan()

    try:
        kode = int(input("Masukkan kode buku yang ingin dipinjam: "))
    except ValueError:
        print("Kode harus berupa angka.")
        return

    i = cari(kode)

    if i == -1:
        print("Buku tidak ditemukan.")
    else:
        buku = daftar[i]
        if buku.tersedia() == 0:
            print("Stok kosong. Buku tidak dapat dipinjam.")
        else:
            buku.stok -= 1
            buku.dipinjam += 1
            print("Buku berhasil dipinjam.")

def kembali():
    bersihkan()

    try:
        kode = int(input("Masukkan kode buku yang dikembalikan: "))
    except ValueError:
        print("Kode harus berupa angka.")
        return

    i = cari(kode)

    if i == -1:
        print("Buku tidak ditemukan.")
    else:
        buku = daftar[i]
        if buku.dipinjam == 0:
            print("Tidak ada salinan buku ini yang sedang dipinjam.")
        else:
            buku.dipinjam -= 1
            buku.stok += 1
            print("Buku berhasil dikembalikan.")

def update():
    bersihkan()
    
    try:
        kode = int(input("Masukkan kode buku yang ingin diupdate: "))
    except ValueError:
        print("Kode harus berupa angka.")
        return

    i = cari(kode)

    if i == -1:
        print("Buku tidak ditemukan.")
        return

    print("\nData Buku")
    print("Judul    :", daftar[i].judul)
    print("Pengarang:", daftar[i].pengarang)
    print("Genre    :", daftar[i].genre)
    print("Stok     :", daftar[i].stok)
    print("Dipinjam :", daftar[i].dipinjam)

    line("=", 40)

    print("Kosongkan jika tidak ingin diubah.")

    judul = input("\nJudul Baru     : ")
    if judul != "":
        daftar[i].judul = judul

    pengarang = input("Pengarang Baru : ")
    if pengarang != "":
        daftar[i].pengarang = pengarang

    genre = input("Genre Baru     : ")
    if genre != "":
        daftar[i].genre = genre

    stok_input = input("Stok Baru (angka) : ")
    if stok_input != "":
        try:
            stok_baru = int(stok_input)
            if stok_baru < 0:
                print("Stok tidak boleh negatif. Perubahan stok dibatalkan.")
            else:
                if stok_baru < daftar[i].dipinjam:
                    print("Stok baru tidak boleh kurang dari jumlah yang sedang dipinjam.")
                else:
                    daftar[i].stok = stok_baru
        except ValueError:
            print("Input stok tidak valid. Perubahan stok dibatalkan.")

    print("\nData buku diperbarui.")

def hapus():
    bersihkan()

    try:
        kode = int(input("Masukkan kode buku yang ingin dihapus: "))
    except ValueError:
        print("Kode harus berupa angka.")
        return

    i = cari(kode)

    if i == -1:
        print("Buku tidak ditemukan.")
        return

    daftar.pop(i)

    print("Buku berhasil dihapus.")

def main():

    while True:

        bersihkan()

        print("===== MENU PERPUSTAKAAN =====")
        print("1. Tambah Buku")
        print("2. Tampilkan Semua Buku")
        print("3. Pinjam Buku")
        print("4. Kembalikan Buku")
        print("5. Update Buku")
        print("6. Hapus Buku")
        print("0. Keluar")

        pilih = input("Pilih menu: ")

        if pilih == "1":
            tambah()
        elif pilih == "2":
            tampilSemua()
        elif pilih == "3":
            pinjam()
        elif pilih == "4":
            kembali()
        elif pilih == "5":
            update()
        elif pilih == "6":
            hapus()
        elif pilih == "0":
            print("Keluar...")
            break
        else:
            print("Pilihan tidak valid.")

        input("\nTekan ENTER untuk kembali ke menu...")

if __name__ == "__main__":
    main()
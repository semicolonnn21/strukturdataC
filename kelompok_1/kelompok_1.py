# ============================================================
# app.py - Aplikasi Benchmarking Struktur Data
# Mata Kuliah: Struktur Data
# Judul: Benchmarking Performa Struktur Data untuk Operasi
#        Searching, Insertion, dan Deletion Menggunakan Streamlit
# ============================================================

# Import library yang dibutuhkan
import streamlit as st         # Framework untuk membuat web app
import random                  # Untuk generate dataset acak
import time                    # Untuk mengukur waktu eksekusi
import pandas as pd            # Untuk manipulasi data dan tabel
import matplotlib.pyplot as plt # Untuk membuat grafik
import numpy as np             # Untuk operasi matematika
import sys                     # Untuk mengatur batas rekursi

# Naikkan batas rekursi Python agar tidak error saat BST dengan data besar
sys.setrecursionlimit(20000)


# ============================================================
# BAGIAN 1: STRUKTUR DATA - ARRAY/LIST
# Kompleksitas:
#   - Search (Linear): O(n)  → harus cek semua elemen
#   - Insert (append): O(1)  → langsung tambah ke akhir
#   - Delete          : O(n) → cari dulu baru hapus
# ============================================================

def array_linear_search(arr, value):
    """
    Linear search pada array.
    Cara kerja: cek satu per satu dari indeks 0 sampai akhir.
    Jika ketemu, kembalikan indeksnya. Jika tidak, kembalikan -1.
    Time Complexity: O(n) — semakin besar array, semakin lama.
    """
    for i in range(len(arr)):   # Loop tiap elemen
        if arr[i] == value:     # Cek apakah elemen ini yang dicari
            return i            # Kembalikan posisi jika ditemukan
    return -1                   # Nilai tidak ditemukan


def array_insert(arr, value):
    """
    Insert (tambah) nilai ke akhir array.
    Time Complexity: O(1) — langsung append ke belakang.
    """
    arr.append(value)   # Tambahkan ke akhir list
    return arr


def array_delete(arr, value):
    """
    Delete (hapus) nilai pertama yang cocok dari array.
    Python harus mencari nilai dulu, baru menghapus dan menggeser elemen.
    Time Complexity: O(n) — butuh pencarian sebelum penghapusan.
    """
    if value in arr:       # Cek apakah nilai ada di array
        arr.remove(value)  # Hapus kemunculan pertama nilai tersebut
    return arr


# ============================================================
# BAGIAN 2: STRUKTUR DATA - BINARY SEARCH TREE (BST)
# Kompleksitas (rata-rata):
#   - Search: O(log n)
#   - Insert: O(log n)
#   - Delete: O(log n)
# Worst Case (data sudah terurut → pohon jadi miring):
#   - Semua operasi: O(n)
# ============================================================

class BSTNode:
    """
    Representasi satu node dalam Binary Search Tree.
    Setiap node memiliki: nilai, anak kiri, dan anak kanan.
    Properti BST: nilai kiri < nilai node ≤ nilai kanan.
    """
    def __init__(self, value):
        self.value = value   # Nilai yang disimpan
        self.left = None     # Pointer ke anak kiri (nilai lebih kecil)
        self.right = None    # Pointer ke anak kanan (nilai lebih besar)


class BST:
    """
    Implementasi Binary Search Tree (BST) secara iteratif.
    Iteratif digunakan (bukan rekursif) agar tidak terjadi
    RecursionError saat dataset besar dan pohon miring.
    """
    def __init__(self):
        self.root = None    # Tree awalnya kosong (tidak ada root)

    def insert(self, value):
        """
        Masukkan nilai baru ke BST.
        Cara kerja: mulai dari root, bandingkan nilai,
        belok kiri jika lebih kecil, kanan jika lebih besar.
        Ulangi hingga slot kosong ditemukan.
        Time Complexity: O(log n) rata-rata, O(n) worst case.
        """
        new_node = BSTNode(value)       # Buat node baru

        if self.root is None:           # Jika tree masih kosong
            self.root = new_node        # Node baru langsung jadi root
            return

        current = self.root             # Mulai dari root
        while True:
            if value < current.value:           # Nilai lebih kecil → ke kiri
                if current.left is None:        # Slot kiri kosong?
                    current.left = new_node     # Letakkan di sini
                    break
                current = current.left          # Belum kosong → terus ke kiri
            else:                               # Nilai lebih besar/sama → ke kanan
                if current.right is None:       # Slot kanan kosong?
                    current.right = new_node    # Letakkan di sini
                    break
                current = current.right         # Belum kosong → terus ke kanan

    def search(self, value):
        """
        Cari nilai di BST.
        Cara kerja: mulai root, bandingkan, belok kiri/kanan sesuai nilai.
        Lebih efisien dari linear search karena memotong setengah data di tiap langkah.
        Time Complexity: O(log n) rata-rata.
        """
        current = self.root             # Mulai dari root
        while current:
            if value == current.value:  # Nilai ditemukan!
                return True
            elif value < current.value: # Nilai lebih kecil → cari ke kiri
                current = current.left
            else:                       # Nilai lebih besar → cari ke kanan
                current = current.right
        return False                    # Sampai akhir, tidak ditemukan

    def _find_min_node(self, node):
        """
        Cari node dengan nilai terkecil di subtree tertentu.
        Caranya: terus ke kiri sampai tidak ada anak kiri lagi.
        Digunakan saat proses penghapusan node dengan 2 anak.
        """
        while node.left:                # Selama ada anak kiri
            node = node.left            # Terus ke kiri
        return node                     # Node paling kiri = nilai terkecil

    def delete(self, value):
        """
        Hapus nilai dari BST.
        Time Complexity: O(log n) rata-rata.
        """
        self.root = self._delete_rec(self.root, value)

    def _delete_rec(self, node, value):
        """
        Fungsi rekursif untuk menghapus node dari BST.
        Ada 3 kasus penghapusan:
        1. Node tidak punya anak → langsung hapus
        2. Node punya 1 anak → sambungkan anak ke parent
        3. Node punya 2 anak → ganti dengan inorder successor
        """
        if node is None:                    # Node tidak ditemukan
            return None

        if value < node.value:              # Nilai ada di subtree kiri
            node.left = self._delete_rec(node.left, value)
        elif value > node.value:            # Nilai ada di subtree kanan
            node.right = self._delete_rec(node.right, value)
        else:                               # Nilai ditemukan di node ini!
            # KASUS 1: Node adalah daun (tidak punya anak)
            if node.left is None and node.right is None:
                return None

            # KASUS 2: Node hanya punya satu anak
            elif node.left is None:         # Hanya ada anak kanan
                return node.right           # Sambungkan anak kanan ke parent
            elif node.right is None:        # Hanya ada anak kiri
                return node.left            # Sambungkan anak kiri ke parent

            # KASUS 3: Node punya dua anak
            else:
                # Cari inorder successor (nilai terkecil di subtree kanan)
                successor = self._find_min_node(node.right)
                node.value = successor.value                                # Salin nilainya
                node.right = self._delete_rec(node.right, successor.value) # Hapus duplikat

        return node


# ============================================================
# BAGIAN 3: STRUKTUR DATA - HASH TABLE
# Kompleksitas (rata-rata):
#   - Search: O(1)
#   - Insert: O(1)
#   - Delete: O(1)
# Worst Case (banyak collision): O(n)
# Collision diatasi dengan Separate Chaining (tiap bucket = list)
# ============================================================

class HashTable:
    """
    Implementasi Hash Table dengan Separate Chaining.
    Separate Chaining: setiap bucket menyimpan list (chain)
    untuk menangani collision (dua nilai memiliki hash yang sama).
    """
    def __init__(self, capacity=2048):
        self.capacity = capacity                        # Jumlah total bucket
        self.buckets = [[] for _ in range(capacity)]   # Setiap bucket adalah list kosong
        self.size = 0                                   # Jumlah elemen yang tersimpan

    def _hash_function(self, value):
        """
        Fungsi hash: mengubah nilai menjadi indeks bucket.
        Menggunakan built-in hash() Python + modulo capacity.
        Hasil: angka antara 0 sampai capacity-1.
        Time Complexity: O(1).
        """
        return hash(value) % self.capacity

    def insert(self, value):
        """
        Masukkan nilai ke hash table.
        Cara kerja: hitung hash → temukan bucket → tambahkan nilai (jika belum ada).
        Time Complexity: O(1) rata-rata.
        """
        index = self._hash_function(value)  # Hitung posisi bucket
        bucket = self.buckets[index]        # Ambil bucket yang sesuai

        if value not in bucket:             # Cegah duplikat
            bucket.append(value)            # Tambahkan ke chain di bucket ini
            self.size += 1

    def search(self, value):
        """
        Cari nilai di hash table.
        Cara kerja: hitung hash → cek apakah nilai ada di bucket tersebut.
        Time Complexity: O(1) rata-rata (langsung ke bucket yang tepat).
        """
        index = self._hash_function(value)      # Hitung posisi bucket
        return value in self.buckets[index]     # Cek di chain bucket tersebut

    def delete(self, value):
        """
        Hapus nilai dari hash table.
        Cara kerja: hitung hash → temukan bucket → hapus nilai dari chain.
        Time Complexity: O(1) rata-rata.
        """
        index = self._hash_function(value)  # Hitung posisi bucket
        bucket = self.buckets[index]        # Ambil bucket

        if value in bucket:                 # Jika nilai ada
            bucket.remove(value)            # Hapus dari chain
            self.size -= 1


# ============================================================
# BAGIAN 4: STRUKTUR DATA - AVL TREE
# Kompleksitas (DIJAMIN untuk semua kasus):
#   - Search: O(log n)
#   - Insert: O(log n)
#   - Delete: O(log n)
# AVL Tree = BST yang secara otomatis menjaga keseimbangan
# menggunakan rotasi setiap kali insert/delete dilakukan.
# ============================================================

class AVLNode:
    """
    Node untuk AVL Tree.
    Memiliki atribut 'height' tambahan untuk menghitung
    balance factor dan menentukan kapan rotasi perlu dilakukan.
    """
    def __init__(self, value):
        self.value = value    # Nilai node
        self.left = None      # Anak kiri
        self.right = None     # Anak kanan
        self.height = 1       # Tinggi node (node daun = 1)


class AVLTree:
    """
    Implementasi AVL Tree (Adelson-Velsky and Landis, 1962).
    Self-balancing BST yang menjaga |balance factor| ≤ 1 di setiap node.
    Balance factor = tinggi(kiri) - tinggi(kanan).
    """
    def __init__(self):
        self.root = None    # Tree kosong pada awal

    def _get_height(self, node):
        """Ambil tinggi node. Return 0 jika node adalah None."""
        return 0 if node is None else node.height

    def _get_balance(self, node):
        """
        Hitung balance factor = tinggi anak kiri - tinggi anak kanan.
        Nilai:
          > 1  → pohon terlalu condong ke kiri (Left Heavy)
          < -1 → pohon terlalu condong ke kanan (Right Heavy)
          -1, 0, 1 → seimbang (OK)
        """
        if node is None:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _update_height(self, node):
        """
        Perbarui tinggi node berdasarkan tinggi anak-anaknya.
        tinggi = 1 + max(tinggi_kiri, tinggi_kanan)
        """
        if node:
            node.height = 1 + max(
                self._get_height(node.left),
                self._get_height(node.right)
            )

    def _rotate_right(self, y):
        """
        Rotasi kanan: digunakan saat pohon condong ke kiri (Left Heavy).
        Sebelum rotasi:       Setelah rotasi:
              y                    x
             / \\                  / \\
            x   C     →          A   y
           / \\                      / \\
          A   B                    B   C
        x naik menggantikan y sebagai root subtree.
        """
        x = y.left          # x akan naik menggantikan y
        B = x.right         # Simpan subtree kanan x (akan dipindahkan)

        # Lakukan rotasi
        x.right = y         # y turun ke kanan x
        y.left = B          # B jadi anak kiri y (menggantikan x)

        # Update tinggi (y dulu karena kini lebih rendah dari x)
        self._update_height(y)
        self._update_height(x)

        return x            # x adalah root baru setelah rotasi

    def _rotate_left(self, x):
        """
        Rotasi kiri: digunakan saat pohon condong ke kanan (Right Heavy).
        Sebelum rotasi:       Setelah rotasi:
            x                      y
           / \\                    / \\
          A   y         →         x   C
             / \\                 / \\
            B   C               A   B
        y naik menggantikan x sebagai root subtree.
        """
        y = x.right         # y akan naik menggantikan x
        B = y.left          # Simpan subtree kiri y

        # Lakukan rotasi
        y.left = x          # x turun ke kiri y
        x.right = B         # B jadi anak kanan x

        # Update tinggi (x dulu karena kini lebih rendah dari y)
        self._update_height(x)
        self._update_height(y)

        return y            # y adalah root baru setelah rotasi

    def _rebalance(self, node):
        """
        Periksa apakah node perlu di-rebalance, dan lakukan rotasi jika perlu.
        Ada 4 kasus ketidakseimbangan:
          1. Left-Left   → rotasi kanan
          2. Left-Right  → rotasi kiri-kanan (double rotation)
          3. Right-Right → rotasi kiri
          4. Right-Left  → rotasi kanan-kiri (double rotation)
        """
        self._update_height(node)           # Perbarui tinggi node dulu
        balance = self._get_balance(node)   # Hitung balance factor

        # KASUS 1: Left-Left (condong kiri, anak kiri juga condong kiri)
        if balance > 1 and self._get_balance(node.left) >= 0:
            return self._rotate_right(node)

        # KASUS 2: Left-Right (condong kiri, anak kiri condong kanan)
        if balance > 1 and self._get_balance(node.left) < 0:
            node.left = self._rotate_left(node.left)    # Rotasi kiri dulu
            return self._rotate_right(node)             # Lalu rotasi kanan

        # KASUS 3: Right-Right (condong kanan, anak kanan juga condong kanan)
        if balance < -1 and self._get_balance(node.right) <= 0:
            return self._rotate_left(node)

        # KASUS 4: Right-Left (condong kanan, anak kanan condong kiri)
        if balance < -1 and self._get_balance(node.right) > 0:
            node.right = self._rotate_right(node.right) # Rotasi kanan dulu
            return self._rotate_left(node)              # Lalu rotasi kiri

        return node     # Node sudah seimbang, tidak perlu rotasi

    def insert(self, value):
        """Masukkan nilai ke AVL Tree. Otomatis rebalance setelah insert. O(log n)."""
        self.root = self._insert_rec(self.root, value)

    def _insert_rec(self, node, value):
        """
        Rekursif insert: masukkan nilai seperti BST biasa,
        lalu panggil rebalance saat kembali (backtracking).
        """
        if node is None:                    # Posisi kosong ditemukan
            return AVLNode(value)           # Buat node baru di sini

        if value < node.value:              # Nilai lebih kecil → masuk ke kiri
            node.left = self._insert_rec(node.left, value)
        elif value > node.value:            # Nilai lebih besar → masuk ke kanan
            node.right = self._insert_rec(node.right, value)
        else:
            return node                     # Nilai duplikat diabaikan

        return self._rebalance(node)        # Rebalance saat kembali ke atas

    def search(self, value):
        """
        Cari nilai di AVL Tree secara iteratif.
        Sama seperti BST search, tapi tinggi pohon dijamin O(log n).
        """
        node = self.root
        while node:
            if value == node.value:         # Ditemukan
                return True
            elif value < node.value:        # Ke kiri
                node = node.left
            else:                           # Ke kanan
                node = node.right
        return False                        # Tidak ditemukan

    def delete(self, value):
        """Hapus nilai dari AVL Tree. Otomatis rebalance setelah delete. O(log n)."""
        self.root = self._delete_rec(self.root, value)

    def _delete_rec(self, node, value):
        """
        Rekursif delete: hapus seperti BST biasa,
        lalu panggil rebalance saat kembali (backtracking).
        """
        if node is None:
            return None

        if value < node.value:              # Cari di kiri
            node.left = self._delete_rec(node.left, value)
        elif value > node.value:            # Cari di kanan
            node.right = self._delete_rec(node.right, value)
        else:                               # Node ditemukan!
            if node.left is None:           # Tidak ada anak kiri
                return node.right
            elif node.right is None:        # Tidak ada anak kanan
                return node.left

            # Ada dua anak → ganti dengan nilai terkecil subtree kanan
            min_node = node.right
            while min_node.left:
                min_node = min_node.left
            node.value = min_node.value                                 # Salin nilai
            node.right = self._delete_rec(node.right, min_node.value)  # Hapus duplikat

        return self._rebalance(node)        # Rebalance saat kembali ke atas


# ============================================================
# BAGIAN 5: FUNGSI GENERATE DATASET
# ============================================================

def generate_dataset(size, dataset_type):
    """
    Buat dataset sesuai ukuran dan tipe yang dipilih pengguna.

    Parameter:
        size (int)        : Jumlah elemen (100, 1000, 10000)
        dataset_type (str): Tipe data (Acak / Terurut Naik / Terurut Turun)

    Return:
        list: Dataset berupa list of int
    """
    if dataset_type == "Acak (Random)":
        # random.sample → ambil 'size' angka unik dari range yang lebih besar
        # Menghasilkan data tanpa duplikat dan tidak berurutan
        return random.sample(range(1, size * 10), size)

    elif dataset_type == "Terurut Naik (Ascending)":
        # Data 1, 2, 3, ..., size — sudah terurut dari kecil ke besar
        # Ini adalah WORST CASE untuk BST biasa (pohon jadi miring ke kanan)
        return list(range(1, size + 1))

    elif dataset_type == "Terurut Turun (Descending)":
        # Data size, size-1, ..., 1 — terurut dari besar ke kecil
        # Juga WORST CASE untuk BST (pohon miring ke kiri)
        return list(range(size, 0, -1))

    return []   # Default: kembalikan list kosong


# ============================================================
# BAGIAN 6: FUNGSI BENCHMARKING
# ============================================================

def build_structure(structure_name, data):
    """
    Bangun (inisialisasi + isi) struktur data dari dataset.
    Waktu membangun struktur TIDAK dihitung dalam benchmark,
    yang diukur hanya operasi tunggal (search/insert/delete).

    Parameter:
        structure_name (str): Nama struktur data
        data (list)         : Dataset untuk mengisi struktur data

    Return:
        Objek struktur data yang sudah terisi
    """
    if structure_name == "Array/List":
        return data.copy()                  # Array adalah salinan list Python biasa

    elif structure_name == "BST":
        bst = BST()
        for val in data:
            bst.insert(val)                 # Masukkan semua data ke BST
        return bst

    elif structure_name == "Hash Table":
        # Kapasitas 3x ukuran data untuk mengurangi kemungkinan collision
        ht = HashTable(capacity=len(data) * 3)
        for val in data:
            ht.insert(val)                  # Masukkan semua data ke Hash Table
        return ht

    elif structure_name == "AVL Tree":
        avl = AVLTree()
        for val in data:
            avl.insert(val)                 # Masukkan semua data ke AVL Tree
        return avl


def measure_single_operation(structure_name, structure_obj, operation, value):
    """
    Ukur waktu eksekusi SATU operasi pada struktur data tertentu.
    Menggunakan time.perf_counter() untuk presisi sub-milidetik.

    Parameter:
        structure_name (str): Nama struktur data
        structure_obj       : Objek struktur data yang sudah terisi
        operation (str)     : "Search", "Insert", atau "Delete"
        value               : Nilai yang digunakan dalam operasi

    Return:
        float: Waktu eksekusi dalam milidetik (ms)
    """
    start = time.perf_counter()     # Catat waktu MULAI (presisi nanosecond)

    # Jalankan operasi sesuai struktur data dan tipe operasi yang dipilih
    if structure_name == "Array/List":
        if operation == "Search":
            array_linear_search(structure_obj, value)           # Cari di array
        elif operation == "Insert":
            array_insert(structure_obj.copy(), value)           # Copy agar data asli aman
        elif operation == "Delete":
            array_delete(structure_obj.copy(), value)           # Copy agar data asli aman

    elif structure_name == "BST":
        if operation == "Search":
            structure_obj.search(value)
        elif operation == "Insert":
            structure_obj.insert(value)
        elif operation == "Delete":
            structure_obj.delete(value)

    elif structure_name == "Hash Table":
        if operation == "Search":
            structure_obj.search(value)
        elif operation == "Insert":
            structure_obj.insert(value)
        elif operation == "Delete":
            structure_obj.delete(value)

    elif structure_name == "AVL Tree":
        if operation == "Search":
            structure_obj.search(value)
        elif operation == "Insert":
            structure_obj.insert(value)
        elif operation == "Delete":
            structure_obj.delete(value)

    end = time.perf_counter()       # Catat waktu SELESAI

    return (end - start) * 1000     # Konversi detik → milidetik


def run_benchmark(data, operation):
    """
    Jalankan benchmark untuk SEMUA struktur data pada satu dataset.

    Cara kerja:
    1. Tentukan nilai yang akan dioperasikan (nilai tengah untuk search/delete,
       nilai baru untuk insert)
    2. Untuk tiap struktur data: bangun struktur → ukur waktu operasi
    3. Simpan dan kembalikan semua hasil

    Parameter:
        data (list)     : Dataset yang digunakan
        operation (str) : Operasi yang diuji

    Return:
        dict: {nama_struktur: waktu_ms}
    """
    all_structures = ["Array/List", "BST", "Hash Table", "AVL Tree"]
    results = {}

    # Tentukan nilai uji berdasarkan operasi
    search_value = data[len(data) // 2]     # Nilai tengah dataset (pasti ada)
    insert_value = max(data) + 999          # Nilai baru yang belum ada di dataset

    for struct_name in all_structures:
        # Bangun struktur data (waktu ini TIDAK dihitung dalam benchmark)
        struct_obj = build_structure(struct_name, data)

        # Tentukan nilai yang digunakan untuk operasi ini
        if operation == "Insert":
            test_value = insert_value       # Nilai baru untuk insert
        else:
            test_value = search_value       # Nilai yang sudah ada untuk search/delete

        # Ukur dan simpan waktu eksekusi operasi
        elapsed = measure_single_operation(struct_name, struct_obj, operation, test_value)
        results[struct_name] = elapsed

    return results


# ============================================================
# BAGIAN 7: FUNGSI VISUALISASI / GRAFIK
# ============================================================

def create_bar_chart(results, title):
    """
    Buat bar chart perbandingan waktu eksekusi antar struktur data.

    Parameter:
        results (dict): {nama_struktur: waktu_ms}
        title (str)   : Judul grafik
    """
    fig, ax = plt.subplots(figsize=(9, 5))  # Buat figure dan axes

    names = list(results.keys())            # Nama-nama struktur data (sumbu X)
    values = list(results.values())         # Waktu eksekusi (sumbu Y)

    # Warna unik untuk setiap batang
    colors = ["#3498db", "#2ecc71", "#f39c12", "#e74c3c"]

    # Gambar batang
    bars = ax.bar(
        names, values,
        color=colors,
        edgecolor="black",
        linewidth=0.6,
        width=0.55
    )

    # Tambahkan label nilai di atas setiap batang
    max_val = max(values) if max(values) > 0 else 1
    for bar, val in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,   # Posisi X: tengah batang
            bar.get_height() + max_val * 0.02,    # Posisi Y: sedikit di atas batang
            f'{val:.5f} ms',                      # Teks: waktu dengan 5 desimal
            ha='center', va='bottom',
            fontsize=8, fontweight='bold'
        )

    # Konfigurasi tampilan grafik
    ax.set_xlabel("Struktur Data", fontsize=12)
    ax.set_ylabel("Waktu Eksekusi (ms)", fontsize=12)
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.grid(axis='y', linestyle='--', alpha=0.6)
    ax.set_ylim(0, max_val * 1.25)  # Berikan ruang kosong di atas label

    plt.tight_layout()  # Atur tata letak agar tidak terpotong
    return fig


def create_line_chart(all_results, sizes, operation, dataset_type):
    """
    Buat line chart yang menunjukkan tren performa seiring bertambahnya ukuran dataset.

    Parameter:
        all_results (dict): {nama_struktur: [waktu_100, waktu_1000, waktu_10000]}
        sizes (list)      : [100, 1000, 10000]
        operation (str)   : Nama operasi yang diuji
        dataset_type (str): Tipe dataset yang diuji
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    colors = ["#3498db", "#2ecc71", "#f39c12", "#e74c3c"]   # Warna setiap garis
    markers = ["o", "s", "^", "D"]                           # Bentuk marker setiap garis

    # Plot garis untuk setiap struktur data
    for idx, (struct_name, times) in enumerate(all_results.items()):
        ax.plot(
            sizes, times,
            label=struct_name,
            color=colors[idx],
            marker=markers[idx],
            linewidth=2.5,
            markersize=9,
            markeredgecolor="black",
            markeredgewidth=0.6
        )

        # Tambahkan anotasi nilai di setiap titik data
        for x, y in zip(sizes, times):
            ax.annotate(
                f'{y:.4f}',             # Format angka
                (x, y),                 # Posisi titik
                textcoords="offset points",
                xytext=(0, 10),         # Offset ke atas
                ha='center', fontsize=7
            )

    # Konfigurasi tampilan
    ax.set_xlabel("Ukuran Dataset (log scale)", fontsize=12)
    ax.set_ylabel("Waktu Eksekusi (ms)", fontsize=12)
    ax.set_title(
        f"Tren Performa Operasi {operation} — {dataset_type}",
        fontsize=13, fontweight='bold'
    )
    ax.legend(fontsize=10, loc='upper left')
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.set_xscale('log')        # Skala logaritmik agar jarak antar titik proporsional

    plt.tight_layout()
    return fig


def create_complexity_chart():
    """
    Buat grafik teoritis yang menggambarkan perbedaan pertumbuhan
    kompleksitas O(1), O(log n), dan O(n).
    Berguna untuk menjelaskan prediksi performa jika dataset diperbesar.
    """
    n = np.linspace(1, 10000, 500)  # Nilai n dari 1 sampai 10000 (500 titik)

    fig, ax = plt.subplots(figsize=(10, 5))

    # Plot ketiga kompleksitas dengan warna dan gaya berbeda
    ax.plot(n, n,                   label="O(n) — Array Linear Search",  color="#3498db", linewidth=2.5)
    ax.plot(n, np.log2(n),          label="O(log n) — BST / AVL Tree",   color="#2ecc71", linewidth=2.5)
    ax.plot(n, np.ones_like(n),     label="O(1) — Hash Table",           color="#f39c12", linewidth=2.5, linestyle='--')

    # Konfigurasi tampilan
    ax.set_xlabel("Ukuran Dataset (n)", fontsize=12)
    ax.set_ylabel("Jumlah Langkah Operasi (skala log)", fontsize=12)
    ax.set_title("Perbandingan Kompleksitas Algoritma Secara Teoritis", fontsize=13, fontweight='bold')
    ax.legend(fontsize=10)
    ax.set_yscale('log')        # Log scale agar perbedaan terlihat lebih jelas
    ax.grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()
    return fig


# ============================================================
# BAGIAN 8: STREAMLIT UI — KONFIGURASI HALAMAN
# ============================================================

# Konfigurasi halaman utama (harus dipanggil PERTAMA sebelum kode Streamlit lain)
st.set_page_config(
    page_title="Benchmarking Struktur Data",    # Judul di tab browser
    page_icon="📊",                              # Ikon di tab browser
    layout="wide",                               # Layout lebar penuh layar
    initial_sidebar_state="expanded"             # Sidebar terbuka saat pertama load
)

# Tambahkan CSS kustom untuk mempercantik tampilan
st.markdown("""
<style>
    /* Judul utama */
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        color: #2c3e50;
        text-align: center;
        padding: 0.5rem 0 0.2rem 0;
    }
    /* Subjudul */
    .sub-header {
        font-size: 1rem;
        color: #7f8c8d;
        text-align: center;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# BAGIAN 9: STREAMLIT UI — SIDEBAR (Panel Kiri)
# ============================================================

# Header sidebar
st.sidebar.title("⚙️ Konfigurasi Benchmark")
st.sidebar.markdown("---")

# Dropdown: pilih operasi yang akan diuji
operation = st.sidebar.selectbox(
    label="🔧 Pilih Operasi:",
    options=["Search", "Insert", "Delete"],
    help="Search: cari nilai | Insert: tambah nilai | Delete: hapus nilai"
)

# Dropdown: pilih tipe distribusi dataset
dataset_type = st.sidebar.selectbox(
    label="📋 Jenis Dataset:",
    options=["Acak (Random)", "Terurut Naik (Ascending)", "Terurut Turun (Descending)"],
    help="Acak = data random | Ascending = 1,2,3,... | Descending = n,n-1,..."
)

# Dropdown: pilih ukuran dataset (kecil / sedang / besar)
dataset_size = st.sidebar.selectbox(
    label="📏 Ukuran Dataset:",
    options=[100, 1000, 10000],
    help="Kecil=100 | Sedang=1.000 | Besar=10.000"
)

st.sidebar.markdown("---")

# Tombol untuk menjalankan benchmark satu ukuran saja
run_single = st.sidebar.button(
    "▶️ Jalankan Benchmark",
    type="primary",                 # Tampilkan sebagai tombol primer (biru)
    use_container_width=True,       # Lebar penuh sidebar
    help="Benchmark dengan ukuran dataset yang dipilih di atas"
)

# Tombol untuk menjalankan benchmark semua ukuran sekaligus (100, 1000, 10000)
run_full = st.sidebar.button(
    "🔄 Benchmark Semua Ukuran",
    use_container_width=True,
    help="Jalankan benchmark untuk 100, 1.000, dan 10.000 data sekaligus"
)

# Kotak informasi kompleksitas di sidebar
st.sidebar.markdown("---")
st.sidebar.info("""
**ℹ️ Kompleksitas Teoritis**
| Struktur | Search | Insert | Delete |
|----------|--------|--------|--------|
| Array    | O(n)   | O(1)   | O(n)   |
| BST      | O(log n)* | O(log n)* | O(log n)* |
| Hash Table | O(1) | O(1)   | O(1)   |
| AVL Tree | O(log n) | O(log n) | O(log n) |

\\* Rata-rata (worst case O(n) jika pohon miring)
""")


# ============================================================
# BAGIAN 10: STREAMLIT UI — KONTEN UTAMA
# ============================================================

# Judul dan deskripsi utama aplikasi
st.markdown('<div class="main-header">📊 Benchmarking Struktur Data</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Perbandingan Performa Array/List · BST · Hash Table · AVL Tree</div>', unsafe_allow_html=True)
st.markdown("---")

# Buat 4 tab navigasi untuk mengelompokkan konten
tab_home, tab_single, tab_full, tab_analysis = st.tabs([
    "🏠  Beranda",
    "📈  Benchmark Tunggal",
    "📊  Benchmark Lengkap",
    "📋  Analisis & Kesimpulan"
])


# ============================================================
# TAB 1: BERANDA
# Menampilkan pengenalan aplikasi dan panduan penggunaan
# ============================================================

with tab_home:
    # SILAKAN PASTE KODE BARU YANG RAMPIIING INI:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 12px 20px; border-radius: 8px; color: white; margin-bottom: 18px; box-shadow: 0 2px 10px rgba(0,0,0,0.08);">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.15); padding-bottom: 4px; margin-bottom: 8px;">
            <h3 style="margin: 0; font-weight: 800; font-size: 1.25rem; color: white;">🚀 KELOMPOK 1 — THE FIRST GROUP</h3>
            <span style="color: #f1c40f; font-size: 0.75rem; font-weight: bold; letter-spacing: 1px; border: 1px solid #f1c40f; padding: 2px 6px; border-radius: 4px;">PROJECT UAS</span>
        </div>
        <p style="margin: 0 0 8px 0; opacity: 0.85; font-size: 0.85rem; line-height: 1.2;">
            <strong>Mata Kuliah:</strong> Struktur Data &nbsp;|&nbsp; <strong>Tema:</strong> Benchmarking Struktur Data Pencarian
        </p>
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; background: rgba(255,255,255,0.06); padding: 6px 10px; border-radius: 6px; font-size: 0.8rem;">
            <div>👤 Yusuf Iskandar (2530801064)</div>
            <div>👤 Muhammad Hafizh Abdul Karim (2530801066)</div>
            <div>👤 Cindy Amelia (2530801071)</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


    # Deskripsi pengantar eksperimen
    st.markdown("""
    ### 🎯 Deskripsi Eksperimen
    Aplikasi ini membandingkan **kecepatan** empat struktur data populer secara empiris saat menjalankan 
    operasi **Search**, **Insert**, dan **Delete** pada berbagai skala ukuran dataset. Hasil pengukuran disajikan dalam 
    grafik interaktif untuk memvalidasi analisis kompleksitas teoritis (Big O).
    """)
    #  AKHIRAN BARU 
    
    # (Di bawah ini adalah kode lama kamu yang JANGAN dihapus, biarkan tetap ada)
    # Tampilkan info card untuk setiap struktur data dalam 4 kolom
    col1, col2, col3, col4 = st.columns(4)
    # ... dan seterusnya sampai bawah ...

    #  KOTAK INFORMASI STRUKTUR DATA
    st.markdown("### 📋 Struktur Data yang Diuji")
    
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.markdown("""
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px; height: 130px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
            <p style="margin:0; font-size:1.1rem;">📦 <b>Array / List</b></p>
            <p style="margin:5px 0 0 0; font-size:0.75rem; color:#4a5568; line-height:1.3;">
                Elemen berurutan. Akses indeks cepat <span style="color:#e53e3e; font-weight:bold;">O(1)</span>, pencarian lambat <span style="color:#e53e3e; font-weight:bold;">O(n)</span>.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px; height: 130px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
            <p style="margin:0; font-size:1.1rem;">🌳 <b>BST</b></p>
            <p style="margin:5px 0 0 0; font-size:0.75rem; color:#4a5568; line-height:1.3;">
                Pohon hierarkis. Rata-rata operasi <span style="color:#3182ce; font-weight:bold;">O(log n)</span>, memburuk jika data input terurut.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px; height: 130px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
            <p style="margin:0; font-size:1.1rem;">#️⃣ <b>Hash Table</b></p>
            <p style="margin:5px 0 0 0; font-size:0.75rem; color:#4a5568; line-height:1.3;">
                Key-value lewat fungsi hash. Pencarian super cepat dengan rata-rata <span style="color:#38a169; font-weight:bold;">O(1)</span>.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown("""
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px; height: 130px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
            <p style="margin:0; font-size:1.1rem;">⚖️ <b>AVL Tree</b></p>
            <p style="margin:5px 0 0 0; font-size:0.75rem; color:#4a5568; line-height:1.3;">
                Self-balancing BST. Tinggi pohon diatur otomatis via rotasi untuk stabilitas <span style="color:#3182ce; font-weight:bold;">O(log n)</span>.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    st.write("") # Jarak vertikal halus

    st.caption("\\* BST: O(log n) rata-rata. Bisa O(n) jika data sudah terurut (pohon menjadi miring/degenerate).")
    st.markdown("---")

    # Panduan langkah-langkah penggunaan
    st.subheader("📖 Cara Menggunakan Aplikasi")
    st.write("**1️⃣** Pilih **Operasi** di sidebar kiri (Search / Insert / Delete)")
    st.write("**2️⃣** Pilih **Jenis Dataset** (Acak / Terurut Naik / Terurut Turun)")
    st.write("**3️⃣** Pilih **Ukuran Dataset** (100 / 1.000 / 10.000 data)")
    st.write("**4️⃣** Klik **▶️ Jalankan Benchmark** untuk uji satu ukuran, atau")
    st.write("**5️⃣** Klik **🔄 Benchmark Semua Ukuran** untuk perbandingan lengkap")
    st.write("**6️⃣** Baca hasil di tab **Benchmark Tunggal** / **Benchmark Lengkap**")
    st.write("**7️⃣** Pelajari teori di tab **Analisis & Kesimpulan**")

    st.markdown("---")

    # Penjelasan tipe dataset
    st.subheader("📋 Penjelasan Tipe Dataset")
    dc1, dc2, dc3 = st.columns(3)

    with dc1:
        st.write("**🎲 Acak (Random)**")
        st.write("Data tidak berurutan, mewakili kondisi paling umum di dunia nyata.")
        st.code("[42, 7, 93, 15, 64, 28, ...]")

    with dc2:
        st.write("**⬆️ Terurut Naik (Ascending)**")
        st.write("Data 1, 2, 3, … → WORST CASE untuk BST (pohon miring kanan).")
        st.code("[1, 2, 3, 4, 5, 6, ...]")

    with dc3:
        st.write("**⬇️ Terurut Turun (Descending)**")
        st.write("Data n, n-1, … 1 → WORST CASE lain untuk BST (pohon miring kiri).")
        st.code("[100, 99, 98, 97, ...]")


# ============================================================
# TAB 2: BENCHMARK TUNGGAL
# Menjalankan benchmark untuk SATU ukuran dataset yang dipilih
# ============================================================

with tab_single:
    st.header("📈 Benchmark Tunggal")

    # Tampilkan konfigurasi yang sedang aktif
    st.write(f"Konfigurasi saat ini: **{operation}** | **{dataset_type}** | **{dataset_size:,} data**")

    if run_single:
        # Jalankan benchmark dalam spinner (tampil animasi loading)
        with st.spinner(f"⏳ Memproses benchmark {operation} — {dataset_size:,} data..."):
            data = generate_dataset(dataset_size, dataset_type)  # Buat dataset
            results = run_benchmark(data, operation)             # Jalankan benchmark

        # Tampilkan pesan sukses
        st.success(f"✅ Benchmark selesai! | Operasi: **{operation}** | Ukuran: **{dataset_size:,}** | Tipe: **{dataset_type}**")
        st.markdown("---")

        # Tentukan struktur data tercepat dan terlambat
        fastest = min(results, key=results.get)
        slowest = max(results, key=results.get)

        # Tampilkan metric cards untuk setiap struktur data
        st.subheader("⏱️ Hasil Waktu Eksekusi")
        metric_cols = st.columns(4)

        for idx, (struct_name, exec_time) in enumerate(results.items()):
            with metric_cols[idx]:
                # Beri tanda khusus untuk yang tercepat
                label = f"🏆 {struct_name}" if struct_name == fastest else struct_name
                delta_text = "Tercepat! 🎉" if struct_name == fastest else None
                st.metric(
                    label=label,
                    value=f"{exec_time:.6f} ms",
                    delta=delta_text
                )

        st.markdown("---")

        # Layout dua kolom: grafik (kiri lebih lebar) dan tabel (kanan)
        col_chart, col_table = st.columns([3, 2])

        with col_chart:
            st.subheader("📊 Grafik Bar Perbandingan")
            fig = create_bar_chart(
                results,
                f"Waktu Eksekusi {operation} — {dataset_size:,} Data ({dataset_type})"
            )
            st.pyplot(fig)
            plt.close(fig)      # Tutup figure untuk membebaskan memori

        with col_table:
            st.subheader("📋 Tabel Ranking")

            # Buat DataFrame dan urutkan dari tercepat
            df = pd.DataFrame({
                "Struktur Data": list(results.keys()),
                "Waktu (ms)": list(results.values()),
            })
            df = df.sort_values("Waktu (ms)").reset_index(drop=True)
            df.insert(0, "Rank", range(1, len(df) + 1))    # Tambahkan kolom ranking
            df["Waktu (ms)"] = df["Waktu (ms)"].apply(lambda x: f"{x:.6f}")  # Format angka

            st.dataframe(df, hide_index=True, use_container_width=True)

            st.markdown("---")
            st.markdown(f"🏆 **Tercepat:** `{fastest}`")
            st.markdown(f"🐢 **Terlambat:** `{slowest}`")

            # Hitung berapa kali lebih cepat yang tercepat vs terlambat
            fastest_t = results[fastest]
            slowest_t = results[slowest]
            if fastest_t > 0:
                ratio = slowest_t / fastest_t
                st.markdown(f"📊 `{fastest}` lebih cepat **{ratio:.1f}x** dari `{slowest}`")

    else:
        # Placeholder sebelum benchmark dijalankan
        st.info("👈 Atur konfigurasi di sidebar, lalu klik **▶️ Jalankan Benchmark**.")


# ============================================================
# TAB 3: BENCHMARK LENGKAP
# Menjalankan benchmark untuk SEMUA ukuran (100, 1000, 10000)
# ============================================================

with tab_full:
    st.header("📊 Benchmark Semua Ukuran Dataset")
    st.write(f"Konfigurasi: **{operation}** | **{dataset_type}** | Ukuran: 100, 1.000, 10.000 data")

    if run_full:
        sizes = [100, 1000, 10000]  # Tiga ukuran dataset yang diuji

        # Inisialisasi dictionary untuk menyimpan waktu dari semua ukuran
        all_results = {
            "Array/List": [],
            "BST": [],
            "Hash Table": [],
            "AVL Tree": []
        }

        # Tampilkan progress bar dan teks status
        progress_bar = st.progress(0)
        status_text = st.empty()    # Placeholder teks yang bisa diganti

        # Iterasi benchmark untuk setiap ukuran dataset
        for i, size in enumerate(sizes):
            status_text.text(f"⏳ Memproses dataset {size:,} data ({i+1}/3)...")

            data = generate_dataset(size, dataset_type)  # Buat dataset
            results = run_benchmark(data, operation)     # Benchmark semua struktur

            # Simpan hasil waktu ke all_results
            for struct_name, exec_time in results.items():
                all_results[struct_name].append(exec_time)

            progress_bar.progress((i + 1) / len(sizes)) # Update progress bar

        # Bersihkan progress bar dan teks setelah selesai
        progress_bar.empty()
        status_text.empty()

        st.success(f"✅ Benchmark lengkap selesai! | Operasi: **{operation}** | Tipe: **{dataset_type}**")
        st.markdown("---")

        # Tampilkan line chart tren performa
        st.subheader("📈 Grafik Tren Performa (Line Chart)")
        fig_line = create_line_chart(all_results, sizes, operation, dataset_type)
        st.pyplot(fig_line)
        plt.close(fig_line)

        st.markdown("---")

        # Tampilkan bar chart untuk setiap ukuran dataset berdampingan
        st.subheader("📊 Perbandingan Per Ukuran Dataset")
        cols_bar = st.columns(3)  # 3 kolom untuk 3 ukuran

        for i, (size, col) in enumerate(zip(sizes, cols_bar)):
            with col:
                # Ambil hasil untuk ukuran dataset ke-i
                size_results = {struct: times[i] for struct, times in all_results.items()}
                fig_bar = create_bar_chart(size_results, f"{size:,} Data")
                st.pyplot(fig_bar)
                plt.close(fig_bar)

        st.markdown("---")

        # Tampilkan tabel hasil lengkap
        st.subheader("📋 Tabel Hasil Lengkap")
        df_full = pd.DataFrame(
            all_results,
            index=[f"{s:,} data" for s in sizes]    # Format angka dengan koma ribuan
        )
        df_display = df_full.applymap(lambda x: f"{x:.6f} ms")   # Format tiap sel
        st.dataframe(df_display, use_container_width=True)

        st.markdown("---")

        # Ringkasan: siapa yang tercepat secara keseluruhan?
        st.subheader("🔍 Ringkasan Performa")
        averages = {struct: sum(times) / len(times) for struct, times in all_results.items()}
        best_avg = min(averages, key=averages.get)
        worst_avg = max(averages, key=averages.get)

        sa1, sa2 = st.columns(2)
        with sa1:
            st.metric("🏆 Rata-rata Tercepat", best_avg, f"{averages[best_avg]:.6f} ms")
        with sa2:
            st.metric("🐢 Rata-rata Terlambat", worst_avg, f"{averages[worst_avg]:.6f} ms")

    else:
        st.info("👈 Klik **🔄 Benchmark Semua Ukuran** di sidebar untuk menjalankan perbandingan lengkap.")


# ============================================================
# TAB 4: ANALISIS & KESIMPULAN
# Berisi teori, kelebihan/kekurangan, prediksi, dan kesimpulan
# ============================================================

with tab_analysis:
    st.header("📋 Analisis dan Kesimpulan")

    # --- BAGIAN A: Tabel Kompleksitas ---
    st.subheader("1️⃣ Tabel Kompleksitas Algoritma")

    df_complex = pd.DataFrame({
        "Struktur Data":     ["Array/List", "BST",         "Hash Table", "AVL Tree"],
        "Search":            ["O(n)",       "O(log n)*",   "O(1)**",     "O(log n)"],
        "Insert":            ["O(1)***",    "O(log n)*",   "O(1)**",     "O(log n)"],
        "Delete":            ["O(n)",       "O(log n)*",   "O(1)**",     "O(log n)"],
        "Space":             ["O(n)",       "O(n)",        "O(n)",       "O(n)"],
        "Keseimbangan":      ["—",          "Tidak dijamin","—",         "Selalu seimbang"]
    })

    st.dataframe(df_complex, hide_index=True, use_container_width=True)

    st.caption("""
    \\* BST: O(log n) untuk kasus rata-rata (data acak), namun bisa O(n) jika data terurut
    \\** Hash Table: O(1) rata-rata, bisa O(n) worst case jika banyak collision
    \\*** Array Insert ke akhir (append): O(1) amortized
    """)

    st.markdown("---")

    # --- BAGIAN B: Kelebihan dan Kekurangan ---
    st.subheader("2️⃣ Kelebihan dan Kekurangan Setiap Struktur Data")

    # Data kelebihan, kekurangan, dan rekomendasi penggunaan
    struct_details = [
        {
            "name": "📦 Array / List",
            "pros": [
                "Paling mudah diimplementasi dan dipahami",
                "Akses elemen via index: O(1) — sangat cepat jika tahu posisinya",
                "Cache-friendly karena memori berurutan (locality of reference)",
                "Overhead memori sangat kecil"
            ],
            "cons": [
                "Search lambat: O(n) — harus cek semua elemen satu per satu",
                "Insert/Delete di tengah array: O(n) — semua elemen setelahnya harus digeser",
                "Tidak efisien untuk dataset besar (> 1000 elemen)"
            ],
            "use": "Dataset kecil, atau saat akses via index sering dilakukan"
        },
        {
            "name": "🌳 BST (Binary Search Tree)",
            "pros": [
                "Search, Insert, Delete efisien: O(log n) rata-rata",
                "Data selalu dalam urutan terurut (in-order traversal = sorted)",
                "Struktur dinamis — mudah tambah/hapus elemen"
            ],
            "cons": [
                "Pohon bisa menjadi degenerate (miring) jika data sudah terurut → performa O(n)",
                "Tidak ada jaminan keseimbangan — performa sangat bergantung pada urutan input",
                "Rekursi dalam bisa menyebabkan stack overflow pada dataset sangat besar"
            ],
            "use": "Data acak yang memerlukan traversal terurut, tanpa kebutuhan performa terjamin"
        },
        {
            "name": "#️⃣ Hash Table",
            "pros": [
                "Paling cepat untuk search, insert, delete: O(1) rata-rata",
                "Performa konsisten meski dataset sangat besar",
                "Ideal untuk caching, database indexing, dan frequency counting"
            ],
            "cons": [
                "Tidak mendukung operasi terurut (tidak bisa iterasi sorted)",
                "Membutuhkan memori ekstra untuk bucket dan chaining",
                "Performa bisa turun saat banyak collision (bergantung pada hash function)",
                "Tidak mendukung range query (misal: cari semua nilai antara 10-50)"
            ],
            "use": "Pencarian cepat (lookup), caching, penghapusan duplikat, frekuensi kata"
        },
        {
            "name": "⚖️ AVL Tree",
            "pros": [
                "Performa O(log n) DIJAMIN untuk semua operasi (tidak ada worst case seperti BST)",
                "Selalu seimbang — tinggi pohon selalu O(log n)",
                "Data selalu terurut (in-order traversal = sorted)"
            ],
            "cons": [
                "Implementasi paling kompleks dari keempat struktur ini",
                "Insert dan Delete lebih lambat dari BST biasa karena ada operasi rotasi",
                "Overhead memori lebih tinggi (menyimpan height di setiap node)"
            ],
            "use": "Database yang butuh data terurut dengan performa pencarian konsisten"
        }
    ]

    # Tampilkan dalam expander agar tidak memakan terlalu banyak ruang
    for info in struct_details:
        with st.expander(f"{info['name']}", expanded=False):
            pro_col, con_col = st.columns(2)

            with pro_col:
                st.write("**✅ Kelebihan:**")
                for pro in info["pros"]:
                    st.write(f"• {pro}")

            with con_col:
                st.write("**❌ Kekurangan:**")
                for con in info["cons"]:
                    st.write(f"• {con}")

            st.info(f"💡 **Terbaik digunakan untuk:** {info['use']}")

    st.markdown("---")

    # --- BAGIAN C: Prediksi Performa Dataset Lebih Besar ---
    st.subheader("3️⃣ Prediksi Performa Jika Dataset Diperbesar")

    # Tampilkan grafik pertumbuhan kompleksitas teoritis
    fig_theory = create_complexity_chart()
    st.pyplot(fig_theory)
    plt.close(fig_theory)

    st.write("""
    Dari grafik di atas, dapat diprediksi jika dataset diperbesar berkali-kali lipat:

    - **Hash Table O(1):** Waktu eksekusi **tetap konstan** berapapun ukuran data.
      Inilah mengapa Hash Table sangat populer di sistem berskala besar.

    - **BST & AVL Tree O(log n):** Pertumbuhan **sangat lambat**.
      Meski data bertambah 1000x (dari 10 menjadi 10.000), waktu hanya bertambah ~10 langkah.

    - **Array O(n):** Waktu tumbuh **secara linear**.
      Data 10x lebih banyak = waktu search 10x lebih lama.
    """)

    # Tabel prediksi jumlah langkah teoritis
    st.subheader("Tabel Prediksi Jumlah Langkah Operasi")
    pred_df = pd.DataFrame({
        "Ukuran Dataset":            ["100", "1.000", "10.000", "100.000", "1.000.000"],
        "Array O(n) (langkah)":      ["100", "1.000", "10.000", "100.000", "1.000.000"],
        "BST/AVL O(log n) (langkah)": ["~7", "~10", "~14", "~17", "~20"],
        "Hash Table O(1) (langkah)": ["1", "1", "1", "1", "1"]
    })
    st.table(pred_df)     # Tampilkan sebagai tabel statis (tidak bisa di-scroll)

    st.markdown("---")

    # --- BAGIAN D: Kesimpulan ---
    st.subheader("4️⃣ Kesimpulan")

    # Jawaban atas pertanyaan analisis dari modul
    conclusions = [
        (
            "🥇 Hash Table: Terbaik untuk operasi lookup murni",
            "Kompleksitas O(1) menjadikan Hash Table sebagai pilihan tercepat untuk search, insert, dan delete — terutama pada dataset besar. Namun tidak cocok jika data perlu terurut."
        ),
        (
            "🥈 AVL Tree: Terbaik jika data harus terurut dengan performa konsisten",
            "AVL Tree menjamin O(log n) di semua kasus, berbeda dari BST yang bisa degenerasi. Pilih AVL Tree ketika data perlu bisa di-traversal secara terurut dan performa harus stabil."
        ),
        (
            "🥉 BST: Cukup baik untuk data acak, hindari data terurut",
            "BST efisien untuk data acak (O(log n)), tetapi kinerjanya bisa turun drastis ke O(n) jika data sudah terurut. Gunakan hanya jika data dapat dijamin acak."
        ),
        (
            "4️⃣ Array/List: Hanya untuk dataset kecil atau akses via index",
            "Array cocok untuk dataset kecil (< 100 elemen) atau saat akses random via indeks diutamakan. Tidak disarankan untuk dataset besar karena search O(n)."
        ),
    ]

    for title, desc in conclusions:
        st.write(f"**{title}**")
        st.write(f"↳ {desc}")
        st.write("")    # Baris kosong sebagai pemisah visual

    # Kotak kesimpulan utama
    st.success("""
    💡 **Poin Penting:** Tidak ada satu struktur data yang terbaik untuk semua situasi.
    Pemilihan harus disesuaikan dengan kebutuhan:
    - Butuh **kecepatan akses maksimum** → **Hash Table**
    - Butuh **data terurut + performa terjamin** → **AVL Tree**
    - Butuh **data terurut + implementasi sederhana** → **BST** (data acak saja)
    - Butuh **akses index langsung** atau **dataset sangat kecil** → **Array/List**
    """)

    st.markdown("---")

    # Jawaban pertanyaan modul: benchmarking dalam pengembangan software
    st.subheader("5️⃣ Peran Benchmarking dalam Pengembangan Software")
    st.write("""
    Benchmarking membantu pengembang software untuk:

    **a) Membuat keputusan berbasis data**, bukan hanya teori.
    Hasil eksperimen membuktikan apakah kompleksitas teoritis sesuai dengan performa nyata.

    **b) Mengidentifikasi bottleneck performa** dalam sistem.
    Jika sebuah fitur lambat, benchmarking membantu menemukan struktur data mana yang jadi penyebab.

    **c) Memilih struktur data yang tepat** sebelum sistem dibangun dalam skala besar.
    Kesalahan memilih struktur data yang diketahui sejak awal lebih murah diperbaiki daripada setelah produksi.

    **d) Mendukung skalabilitas sistem**.
    Dengan menguji berbagai ukuran dataset, developer bisa memprediksi apakah sistem akan tetap performa saat pengguna bertambah.
    """)


# ============================================================
# FOOTER — Bagian bawah halaman
# ============================================================
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#95a5a6; font-size:0.85rem;'>"
    "📚 <strong>UAS Struktur Data</strong> · "
    "Benchmarking Performa Struktur Data · "
    "Dibuat dengan Streamlit 🎈"
    "</div>",
    unsafe_allow_html=True
)

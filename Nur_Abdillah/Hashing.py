class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(size)]

    # Fungsi hash khusus angka
    def hash_function(self, key):
        return key % self.size

    # Insert data angka
    def insert(self, key):
        index = self.hash_function(key)
        self.table[index].append(key)

    # Search angka
    def search(self, key):
        index = self.hash_function(key)
        if key in self.table[index]:
            return True
        return False

    # Tampilkan isi hash table
    def display(self):
        for i in range(self.size):
            print(f"Index {i}: {self.table[i]}")


# ======================
# CONTOH PENGGUNAAN
# ======================
ht = HashTable(10)

data = [15, 23, 7, 32, 44, 12]

# Insert data
for angka in data:
    ht.insert(angka)

# Tampilkan tabel
print("Isi Hash Table:")
ht.display()

# Search
cari = 23
print(f"\nCari {cari}: ", "Ditemukan" if ht.search(cari) else "Tidak ditemukan")

cari = 99
print(f"Cari {cari}: ", "Ditemukan" if ht.search(cari) else "Tidak ditemukan")
class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [None] * size

    def hash_function(self, key):
        # Menggunakan rumus k mod size [cite: 163, 179]
        return key % self.size

    def insert(self, key):
        index = self.hash_function(key)
        
        # Jika terjadi tabrakan (Collision), gunakan Linear Probing 
        original_index = index
        while self.table[index] is not None:
            print(f"Tabrakan di indeks {index} untuk kunci {key}. Mencari sel berikutnya...")
            index = (index + 1) % self.size # Geser secara linear [cite: 181, 182]
            if index == original_index: # Tabel penuh
                return "Tabel Hash Penuh!"
        
        self.table[index] = key
        print(f"Kunci {key} berhasil disimpan di indeks {index}")

    def display(self):
        print("\nIsi Tabel Hash:")
        for i in range(self.size):
            print(f"Index {i}: {self.table[i]}")

# Contoh Penggunaan sesuai materi slide [cite: 182]
hash_table = HashTable(10)
data_untuk_input = [13, 157, 2001, 11456, 207]

for item in data_untuk_input:
    hash_table.insert(item)

hash_table.display()
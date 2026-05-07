class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [None] * size
        
    def hash_function(self, key):
        # Menggunakan modulus untuk menentukan indeks [cite: 318]
        return key % self.size
        
    def insert(self, key):
        index = self.hash_function(key)
        
        # Jika slot kosong, langsung masukkan data
        if self.table[index] is None:
            self.table[index] = key
            print(f"Data {key} berhasil dimasukkan ke indeks {index}")
        else:
            print(f"Terjadi Collision pada indeks {index} saat memasukkan {key}. Melakukan Linear Probing...")
            # Linear Probing: Mencari sel kosong berikutnya secara linier [cite: 315]
            original_index = index
            while self.table[index] is not None:
                index = (index + 1) % self.size
                if index == original_index:
                    print("Tabel Hash sudah penuh!")
                    return
            
            self.table[index] = key
            print(f"Data {key} ditempatkan pada sel kosong berikutnya di indeks {index}")

    def display(self):
        print("\n=== Tabel Hash ===")
        for i, val in enumerate(self.table):
            print(f"Index {i} : {val}")

# [cite: 318, 323, 329, 334, 336]
if __name__ == "__main__":
    # Membuat tabel hash dengan ukuran 10
    ht = HashTable(10)
    
    # Memasukkan data awal
    ht.insert(2001)
    ht.insert(13)
    ht.insert(11456)
    ht.insert(157)
    
    # Memasukkan elemen 207 yang akan memicu tabrakan di indeks 7 [cite: 318, 324]
    ht.insert(207)
    
    ht.display()
class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(size)]  # chaining

    def hash_function(self, key):
        return key % self.size

    def insert(self, key):
        index = self.hash_function(key)
        self.table[index].append(key)

    def search(self, key):
        index = self.hash_function(key)
        if key in self.table[index]:
            return True, index
        return False, index

    def display(self):
        for i, val in enumerate(self.table):
            print(f"Index {i}: {val}")


# TESTING
ht = HashTable(7)

data = [14, 5, 9, 1, 24]

for d in data:
    ht.insert(d)

ht.display()

# Cari data
print("\nCari 9:")
found, index = ht.search(9)
print("Ditemukan di index", index if found else "Tidak ditemukan")
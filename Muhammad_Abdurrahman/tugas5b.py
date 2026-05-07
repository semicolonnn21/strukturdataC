class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(size)]

    def hash_function(self, key):
        return key % self.size

    def insert(self, key):
        index = self.hash_function(key)
        self.table[index].append(key)

    def display(self):
        for i, val in enumerate(self.table):
            print(f"Index {i}: {val}")


# Contoh penggunaan
ht = HashTable(7)

data = [21, 77, 72, 75, 5, 19]

for d in data:
    ht.insert(d)

ht.display()
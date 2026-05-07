# ukuran hash table
size = 5
hash_table = [None] * size

# hash function
def hash_function(key):
    return key % size

# insert data
def insert(key):
    index = hash_function(key)

    while hash_table[index] is not None:
        index = (index + 1) % size  # linear probing

    hash_table[index] = key

# search data
def search(key):
    index = hash_function(key)
    start = index

    while hash_table[index] is not None:
        if hash_table[index] == key:
            return index
        index = (index + 1) % size
        if index == start:
            break

    return -1

# ====== contoh penggunaan ======
data = [70, 20, 31, 40, 15]

# insert
for d in data:
    insert(d)

print("Hash Table:", hash_table)

# search
cari = 40
hasil = search(cari)

if hasil != -1:
    print(f"Data {cari} ditemukan di index {hasil}")
else:
    print(f"Data {cari} tidak ditemukan")
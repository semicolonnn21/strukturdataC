import streamlit as st

#Berikut kode Implementasi BST
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, root, value):
        # Jika tree kosong
        if root is None:
            return Node(value)

        # Masuk ke kiri
        if value < root.value:
            root.left = self.insert(root.left, value)
        # Masuk ke kanan
        else:
            root.right = self.insert(root.right, value)

        return root

    def preorder(self, root, wadah):
        if root:
            wadah.append(str(root.value))
            self.preorder(root.left, wadah)
            self.preorder(root.right, wadah)

    def inorder(self, root, wadah):
        if root:
            self.inorder(root.left, wadah)
            wadah.append(str(root.value))
            self.inorder(root.right, wadah)

    def postorder(self, root, wadah):
        if root:
            self.postorder(root.left, wadah)
            self.postorder(root.right, wadah)
            wadah.append(str(root.value))


# TAMPILAN HALAMAN STREAMLIT

st.title("Tugas Implementasi Binary Search Tree (BST)")

# 1. Membuat BST awal
tree = BST()
data_awal = [50, 30, 70, 20, 40, 60, 80]
for item in data_awal:
    tree.root = tree.insert(tree.root, item)

st.header("1. Hasil Traversal Awal")

# Menyiapkan wadah kosong untuk menampung hasil angka
pre_awal, in_awal, post_awal = [], [], []

# Menjalankan fungsi traversal dan memasukkan angkanya ke wadah
tree.preorder(tree.root, pre_awal)
tree.inorder(tree.root, in_awal)
tree.postorder(tree.root, post_awal)

# Menampilkan wadah ke web Streamlit
st.text(f"Preorder  : {' '.join(pre_awal)}")
st.text(f"Inorder   : {' '.join(in_awal)}")
st.text(f"Postorder : {' '.join(post_awal)}")

# Menambahkan visualisasi tree sebelum ada node baru
st.subheader("Visualisasi Tree Awal")
st.code("""
               50
             /    \\
           30      70
          /  \\    /  \\
        20   40  60   80
""", language="text")


# 2. Menambahkan node baru
st.divider()
st.header("2. Hasil Traversal Setelah Penambahan Node (10, 90, 65)")

node_baru = [10, 90, 65]
for item in node_baru:
    tree.root = tree.insert(tree.root, item)

# Menyiapkan wadah baru untuk hasil akhir
pre_akhir, in_akhir, post_akhir = [], [], []

tree.preorder(tree.root, pre_akhir)
tree.inorder(tree.root, in_akhir)
tree.postorder(tree.root, post_akhir)

st.text(f"Preorder  : {' '.join(pre_akhir)}")
st.text(f"Inorder   : {' '.join(in_akhir)}")
st.text(f"Postorder : {' '.join(post_akhir)}")


# 3. Visualisasi Tree Akhir
st.divider()
st.header("3. Visualisasi Tree Akhir")
st.code("""
               50
             /    \\
           30      70
          /  \\    /  \\
        20   40  60   80
       /          \\     \\
     10           65    90
""", language="text")


# 4. Analisis Perubahan
st.divider()
st.header("4. Analisis Perubahan Hasil Traversal")
st.markdown("""
Penambahan tiga node baru mengubah urutan karena struktur rantingnya makin panjang di ujung. Ini alasannya:

1. **Inorder (Kiri, Akar, Kanan):** Karakteristik metode ini selalu memunculkan angka yang urut dari terkecil sampai terbesar. Node 10, 65, dan 90 langsung menyelip di urutan nilai yang pas tanpa merusak formasi.
2. **Preorder (Akar, Kiri, Kanan):** Alurnya langsung menelusuri dahan dari atas lurus ke ujung paling kiri. Node 10 terekam setelah 20. Node 65 terekam setelah 60 karena letaknya di kanan angka 60. Node 90 dibaca paling akhir karena posisinya di pucuk paling kanan pohon.
3. **Postorder (Kiri, Kanan, Akar):** Metode ini membaca dari daun terbawah dulu sebelum naik ke angka induknya. Karena node 10, 65, dan 90 berstatus sebagai daun di ujung pohon, mereka langsung dicetak duluan mendahului angka induknya (contohnya angka 10 tampil sebelum 20, dan 65 tampil sebelum 60).
""")
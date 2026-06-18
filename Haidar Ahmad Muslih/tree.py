import streamlit as st


# ======================
# CLASS NODE
# ======================

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


# ======================
# CLASS BST
# ======================

class BST:
    def __init__(self):
        self.root = None

    # INSERT NODE
    def insert(self, root, value):

        if root is None:
            return Node(value)

        if value < root.value:
            root.left = self.insert(root.left, value)

        else:
            root.right = self.insert(root.right, value)

        return root

    # PREORDER
    def preorder(self, root, result):

        if root:
            result.append(root.value)
            self.preorder(root.left, result)
            self.preorder(root.right, result)

    # INORDER
    def inorder(self, root, result):

        if root:
            self.inorder(root.left, result)
            result.append(root.value)
            self.inorder(root.right, result)

    # POSTORDER
    def postorder(self, root, result):

        if root:
            self.postorder(root.left, result)
            self.postorder(root.right, result)
            result.append(root.value)

    # MENAMPILKAN TREE
    def display_tree(self, root, level=0, side="Root"):

        if root is not None:

            st.write("   " * level + f"{side}: {root.value}")

            self.display_tree(root.left, level + 1, "L")
            self.display_tree(root.right, level + 1, "R")


# ======================
# STREAMLIT APP
# ======================

st.title("Visualisasi Binary Search Tree")

tree = BST()

# DATA AWAL
data_awal = [50, 30, 70, 20, 40, 60, 80]

for item in data_awal:
    tree.root = tree.insert(tree.root, item)

# TRAVERSAL AWAL
pre_awal = []
ino_awal = []
post_awal = []

tree.preorder(tree.root, pre_awal)
tree.inorder(tree.root, ino_awal)
tree.postorder(tree.root, post_awal)

st.subheader("Traversal Sebelum Penambahan Node")

st.write("Preorder :", pre_awal)
st.write("Inorder :", ino_awal)
st.write("Postorder :", post_awal)

# TAMBAH NODE BARU
new_nodes = [10, 90, 65]

for item in new_nodes:
    tree.root = tree.insert(tree.root, item)

# TRAVERSAL SETELAH PENAMBAHAN
pre = []
ino = []
post = []

tree.preorder(tree.root, pre)
tree.inorder(tree.root, ino)
tree.postorder(tree.root, post)

st.subheader("Traversal Setelah Penambahan Node")

st.write("Preorder :", pre)
st.write("Inorder :", ino)
st.write("Postorder :", post)

# TAMPILKAN TREE
st.subheader("Struktur Binary Search Tree")

tree.display_tree(tree.root)

# ANALISIS
st.subheader("Analisis")

st.write("""
- Node 10 masuk ke kiri node 20.
- Node 90 masuk ke kanan node 80.
- Node 65 masuk ke kanan node 60.

Traversal berubah karena jumlah node bertambah.
Traversal inorder tetap terurut dari kecil ke besar.
""")
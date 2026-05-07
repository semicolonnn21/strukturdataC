# simpan dengan nama app.py
# jalankan:
# streamlit run app.py

import streamlit as st

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    # insert node
    def insert(self, root, value):

        if root is None:
            return Node(value)

        if value < root.value:
            root.left = self.insert(root.left, value)

        else:
            root.right = self.insert(root.right, value)

        return root

    # preorder
    def preorder(self, root, hasil):
        if root:
            hasil.append(root.value)
            self.preorder(root.left, hasil)
            self.preorder(root.right, hasil)

    # inorder
    def inorder(self, root, hasil):
        if root:
            self.inorder(root.left, hasil)
            hasil.append(root.value)
            self.inorder(root.right, hasil)

    # postorder
    def postorder(self, root, hasil):
        if root:
            self.postorder(root.left, hasil)
            self.postorder(root.right, hasil)
            hasil.append(root.value)

def tampil_tree(node, space=0, level=0):

    if node is None:
        return ""

    hasil = ""

    # kanan
    hasil += tampil_tree(node.right, space + 8, level + 1)

    # node
    hasil += "\n"
    hasil += " " * space
    hasil += str(node.value)

    # kiri
    hasil += tampil_tree(node.left, space + 8, level + 1)

    return hasil

st.title("Visualisasi Binary Search Tree")

st.write("SALIM MUBAROK . STRUKTUR DATA . UINSSC")

input_data = st.text_input(
    "Masukkan node (pisahkan dengan koma)",
    "50,30,70,20,40,60,80,10,65,90"
)

# buat tree
tree = BST()

# ubah input menjadi list angka
data = [int(x) for x in input_data.split(",")]

# insert node
for angka in data:
    tree.root = tree.insert(tree.root, angka)

pre = []
ino = []
post = []

tree.preorder(tree.root, pre)
tree.inorder(tree.root, ino)
tree.postorder(tree.root, post)

st.subheader("Preorder")
st.write(pre)

st.subheader("Inorder")
st.write(ino)

st.subheader("Postorder")
st.write(post)

st.subheader("Analisis")

st.write("""
- Preorder : Root ➜ Left ➜ Right
- Inorder : Left ➜ Root ➜ Right
- Postorder : Left ➜ Right ➜ Root
- Inorder pada BST menghasilkan data yang terurut.
""")

st.subheader("Bentuk Tree")

tree_text = tampil_tree(tree.root)

st.code(tree_text)
import streamlit as st
from graphviz import Digraph
import io
from contextlib import redirect_stdout


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

    def insert(self, root, value):
        if root is None:
            return Node(value)
        if value < root.value:
            root.left = self.insert(root.left, value)
        else:
            root.right = self.insert(root.right, value)
        return root

    # Fungsi traversal (Sekarang berada di dalam Class BST)
    def preorder(self, root):
        if root:
            print(root.value, end=" ")
            self.preorder(root.left)
            self.preorder(root.right)

    def inorder(self, root):
        if root:
            self.inorder(root.left)
            print(root.value, end=" ")
            self.inorder(root.right)

    def postorder(self, root):
        if root:
            self.postorder(root.left)
            self.postorder(root.right)
            print(root.value, end=" ")


# --- Inisialisasi Data ---
tree = BST()
data = [50, 30, 70, 20, 40, 60, 80]
for item in data:
    tree.root = tree.insert(tree.root, item)

# Tambahkan node baru sesuai tugas
for item in [10, 90, 65]:
    tree.root = tree.insert(tree.root, item)

# --- Tampilan Streamlit ---
st.title("Visualisasi & Traversal BST")


# Fungsi untuk menangkap output print() agar tampil di Streamlit
def get_traversal_output(func, root):
    f = io.StringIO()
    with redirect_stdout(f):
        func(root)
    return f.getvalue()


st.subheader("1. Hasil Traversal")
st.text(f"Preorder  : {get_traversal_output(tree.preorder, tree.root)}")
st.text(f"Inorder   : {get_traversal_output(tree.inorder, tree.root)}")
st.text(f"Postorder : {get_traversal_output(tree.postorder, tree.root)}")

st.subheader("2. Visualisasi Tree")


def visualisasikan_tree(node, dot=None):
    if dot is None:
        dot = Digraph()
    if node:
        dot.node(str(node.value), str(node.value))
        if node.left:
            dot.edge(str(node.value), str(node.left.value))
            visualisasikan_tree(node.left, dot)
        if node.right:
            dot.edge(str(node.value), str(node.right.value))
            visualisasikan_tree(node.right, dot)
    return dot


st.graphviz_chart(visualisasikan_tree(tree.root))

st.subheader("3. Analisis")
st.write(
    "Setelah penambahan node 10, 90, dan 65, struktur pohon menjadi lebih dalam. Inorder tetap menampilkan urutan angka dari yang terkecil hingga terbesar."
)

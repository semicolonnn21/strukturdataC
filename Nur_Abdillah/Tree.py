import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt


# ======================
# NODE BST
# ======================

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


# ======================
# BST
# ======================

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


# ======================
# MEMBUAT GRAPH TREE
# ======================

def add_edges(graph, node):

    if node is None:
        return

    if node.left:
        graph.add_edge(node.value, node.left.value)
        add_edges(graph, node.left)

    if node.right:
        graph.add_edge(node.value, node.right.value)
        add_edges(graph, node.right)


# ======================
# POSISI TREE AGAR RAPI
# ======================

def hierarchy_pos(G, root, width=1.0, vert_gap=0.2,
                  vert_loc=0, xcenter=0.5, pos=None):

    if pos is None:
        pos = {}

    pos[root] = (xcenter, vert_loc)

    children = list(G.neighbors(root))

    if len(children) != 0:

        dx = width / len(children)

        nextx = xcenter - width / 2 - dx / 2

        for child in children:

            nextx += dx

            pos = hierarchy_pos(
                G,
                child,
                width=dx,
                vert_gap=vert_gap,
                vert_loc=vert_loc - vert_gap,
                xcenter=nextx,
                pos=pos
            )

    return pos


# ======================
# STREAMLIT
# ======================

st.title("Visualisasi Binary Search Tree")

tree = BST()

# ======================
# DATA AWAL
# ======================

data_awal = [50, 30, 70, 20, 40, 60, 80]

for item in data_awal:
    tree.root = tree.insert(tree.root, item)

# ======================
# TRAVERSAL AWAL
# ======================

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

# ======================
# TAMBAH NODE BARU
# ======================

new_nodes = [10, 90, 65]

for item in new_nodes:
    tree.root = tree.insert(tree.root, item)

# ======================
# TRAVERSAL SETELAH TAMBAH NODE
# ======================

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

# ======================
# ANALISIS
# ======================

st.subheader("Analisis")

st.write("""
Setelah node 10, 90, dan 65 ditambahkan,
struktur Binary Search Tree berubah sesuai aturan BST.

- Node 10 masuk ke subtree kiri.
- Node 90 masuk ke subtree kanan.
- Node 65 berada di kanan node 60.

Traversal preorder, inorder, dan postorder mengalami perubahan
karena jumlah node bertambah.

Traversal inorder tetap menghasilkan urutan data dari kecil ke besar
karena sifat Binary Search Tree.
""")

# ======================
# VISUALISASI TREE
# ======================

G = nx.DiGraph()

add_edges(G, tree.root)

fig, ax = plt.subplots(figsize=(10, 6))

# ROOT TREE
pos = hierarchy_pos(G, 50)

nx.draw(
    G,
    pos,
    with_labels=True,
    node_size=3000,
    node_color="skyblue",
    font_size=12,
    font_weight="bold",
    arrows=False,
    ax=ax
)

st.subheader("Visualisasi BST")

st.pyplot(fig)

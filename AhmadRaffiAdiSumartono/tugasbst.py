import os
os.environ["PATH"] += os.pathsep + r"C:\Program Files\Graphviz\bin"

from graphviz import Digraph

# =========================================
# TUGAS BST - TREE DATA STRUCTURE
# Nama : Ahmad Raffi Adi Sumartono
# =========================================

# =========================
# CLASS NODE
# =========================
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


# =========================
# CLASS BST
# =========================
class BST:
    def __init__(self):
        self.root = None

    # INSERT NODE
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
    def preorder(self, root):

        if root:
            print(root.value, end=" ")
            self.preorder(root.left)
            self.preorder(root.right)

    # INORDER
    def inorder(self, root):

        if root:
            self.inorder(root.left)
            print(root.value, end=" ")
            self.inorder(root.right)

    # POSTORDER
    def postorder(self, root):

        if root:
            self.postorder(root.left)
            self.postorder(root.right)
            print(root.value, end=" ")


# =========================
# VISUALISASI TREE
# =========================
def visualisasi(node, graph=None):

    if graph is None:
        graph = Digraph()
        graph.attr("node", shape="circle")

    if node:

        # Membuat node
        graph.node(str(node.value))

        # Ke kiri
        if node.left:
            graph.edge(str(node.value), str(node.left.value))
            visualisasi(node.left, graph)

        # Ke kanan
        if node.right:
            graph.edge(str(node.value), str(node.right.value))
            visualisasi(node.right, graph)

    return graph


# =========================
# MEMBUAT BST
# =========================
tree = BST()

# DATA AWAL
data = [50, 30, 70, 20, 40, 60, 80]

for item in data:
    tree.root = tree.insert(tree.root, item)

# =========================
# TRAVERSAL AWAL
# =========================
print("================================")
print("TRAVERSAL AWAL")
print("================================")

print("Preorder : ")
tree.preorder(tree.root)

print("\n\nInorder : ")
tree.inorder(tree.root)

print("\n\nPostorder : ")
tree.postorder(tree.root)

# =========================
# PENAMBAHAN NODE
# =========================
tambahan = [10, 90, 65]

for item in tambahan:
    tree.root = tree.insert(tree.root, item)

# =========================
# HASIL SETELAH PENAMBAHAN
# =========================
print("\n\n================================")
print("SETELAH PENAMBAHAN NODE")
print("================================")

print("Preorder : ")
tree.preorder(tree.root)

print("\n\nInorder : ")
tree.inorder(tree.root)

print("\n\nPostorder : ")
tree.postorder(tree.root)

# =========================
# ANALISIS
# =========================
print("\n\n================================")
print("ANALISIS")
print("================================")

print("- Node 10 masuk ke kiri dari 20")
print("- Node 90 masuk ke kanan dari 80")
print("- Node 65 masuk ke kanan dari 60")
print("- Traversal berubah karena ada penambahan node baru")
print("- Inorder traversal menghasilkan data terurut")

# =========================
# MEMBUAT VISUALISASI TREE
# =========================
graph = visualisasi(tree.root)

# Simpan jadi PNG
graph.render("visualisasi_bst", format="png", cleanup=True)

print("\n================================")
print("VISUALISASI BERHASIL")
print("================================")
print("File gambar : visualisasi_bst.png")

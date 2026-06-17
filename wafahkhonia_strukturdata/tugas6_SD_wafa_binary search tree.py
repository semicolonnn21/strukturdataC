import streamlit as st
import graphviz

# Node dan BST Class
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

    # Traversal Preorder
    def preorder(self, root, result):
        if root:
            result.append(root.value)
            self.preorder(root.left, result)
            self.preorder(root.right, result)

    # Traversal Inorder
    def inorder(self, root, result):
        if root:
            self.inorder(root.left, result)
            result.append(root.value)
            self.inorder(root.right, result)

    # Traversal Postorder
    def postorder(self, root, result):
        if root:
            self.postorder(root.left, result)
            self.postorder(root.right, result)
            result.append(root.value)

# Membuat BST
tree = BST()
data_awal = [50, 30, 70, 20, 40, 60, 80]
extra = [10, 90, 65]

# Data awal
for item in data_awal:
    tree.root = tree.insert(tree.root, item)

# Traversal sebelum penambahan
pre_before, in_before, post_before = [], [], []
tree.preorder(tree.root, pre_before)
tree.inorder(tree.root, in_before)
tree.postorder(tree.root, post_before)

# Tambahkan node baru
for item in extra:
    tree.root = tree.insert(tree.root, item)

# Traversal sesudah penambahan
pre_after, in_after, post_after = [], [], []
tree.preorder(tree.root, pre_after)
tree.inorder(tree.root, in_after)
tree.postorder(tree.root, post_after)

# Tampilan Streamlit
st.title("🌳 Visualisasi Binary Search Tree (BST)")

st.subheader("🔹 Traversal Sebelum Penambahan Node")
st.write("Preorder:", pre_before)
st.write("Inorder:", in_before)
st.write("Postorder:", post_before)

st.subheader("🔹 Traversal Sesudah Penambahan Node (10, 65, 90)")
st.write("Preorder:", pre_after)
st.write("Inorder:", in_after)
st.write("Postorder:", post_after)

# Analisis perubahan
st.subheader("📊 Analisis Perubahan Traversal")
st.markdown(f"""
- **Preorder** berubah dari {pre_before} menjadi {pre_after}.  
  ➝ Node baru muncul sesuai posisi: 10 di kiri bawah, 65 di kanan 60, 90 di kanan 80.  

- **Inorder** berubah dari {in_before} menjadi {in_after}.  
  ➝ Tetap terurut naik, membuktikan BST valid.  

- **Postorder** berubah dari {post_before} menjadi {post_after}.  
  ➝ Node baru muncul di urutan sesuai cabang masing-masing.
""")

# Visualisasi Tree dengan Graphviz
def draw_tree(root):
    dot = graphviz.Digraph()
    def add_nodes_edges(node):
        if node is None:
            return
        dot.node(str(node.value))
        if node.left:
            dot.edge(str(node.value), str(node.left.value))
            add_nodes_edges(node.left)
        if node.right:
            dot.edge(str(node.value), str(node.right.value))
            add_nodes_edges(node.right)
    add_nodes_edges(root)
    return dot

st.subheader("🌿 Visualisasi Tree")
st.graphviz_chart(draw_tree(tree.root))

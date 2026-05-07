import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

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
    
    def preorder(self, root, result=None):
        if result is None: result = []
        if root:
            result.append(root.value)
            self.preorder(root.left, result)
            self.preorder(root.right, result)
        return result

    def inorder(self, root, result=None):
        if result is None: result = []
        if root:
            self.inorder(root.left, result)
            result.append(root.value)
            self.inorder(root.right, result)
        return result

    def postorder(self, root, result=None):
        if result is None: result = []
        if root:
            self.postorder(root.left, result)
            self.postorder(root.right, result)
            result.append(root.value)
        return result


def get_edges_and_pos(node, x=0, y=0, layer_width=2, pos=None, edges=None):
    """Fungsi rekursif untuk menentukan posisi (x,y) dan garis tiap Node"""
    if pos is None: pos = {}
    if edges is None: edges = []
    
    pos[node.value] = (x, y)
    
    if node.left:
        edges.append((node.value, node.left.value))
        get_edges_and_pos(node.left, x - layer_width, y - 1, layer_width / 2, pos, edges)
    
    if node.right:
        edges.append((node.value, node.right.value))
        get_edges_and_pos(node.right, x + layer_width, y - 1, layer_width / 2, pos, edges)
        
    return edges, pos

def draw_bst(root):
    if not root:
        return None
    
    edges, pos = get_edges_and_pos(root, layer_width=4)
    
    G = nx.DiGraph()
    G.add_edges_from(edges)

    if not edges:
        G.add_node(root.value)
        
    fig, ax = plt.subplots(figsize=(10, 6))

    nx.draw(G, pos, with_labels=True, node_size=2000, node_color="#ADD8E6", 
            font_size=12, font_weight="bold", arrows=False, ax=ax, edge_color="gray")
    
    return fig


st.set_page_config(page_title="Visualisasi BST", layout="wide")
st.title("Visualisasi Binary Search Tree (BST)")

tree = BST()
data_awal = [50, 30, 70, 20, 40, 60, 80]
for item in data_awal:
    tree.root = tree.insert(tree.root, item)

st.header("1. Hasil Traversal Data Awal")
st.write(f"**Data dimasukkan:** `{data_awal}`")

col1, col2, col3 = st.columns(3)
with col1:
    st.info("**Preorder:**")
    st.write(tree.preorder(tree.root))
with col2:
    st.info("**Inorder:**")
    st.write(tree.inorder(tree.root))
with col3:
    st.info("**Postorder:**")
    st.write(tree.postorder(tree.root))

st.divider()

data_baru = [10, 90, 65]
for item in data_baru:
    tree.root = tree.insert(tree.root, item)

st.header("2. Hasil Setelah Penambahan Node Baru")
st.write(f"**Node baru yang ditambahkan:** `{data_baru}`")

col1, col2, col3 = st.columns(3)
with col1:
    st.success("**Preorder Baru:**")
    st.write(tree.preorder(tree.root))
with col2:
    st.success("**Inorder Baru:**")
    st.write(tree.inorder(tree.root))
with col3:
    st.success("**Postorder Baru:**")
    st.write(tree.postorder(tree.root))

st.divider()

st.header("3. Visualisasi Tree Setelah Seluruh Node Ditambahkan")
fig = draw_bst(tree.root)
st.pyplot(fig)

st.divider()

st.header("4. Analisis Perubahan Hasil Traversal")
st.markdown("""
Berdasarkan penambahan kode (nilai **10, 90, 65**), berikut adalah analisis perubahannya:

*   **Inorder (Kiri - Root - Kanan):** 
    Traversal inorder selalu menghasilkan data yang terurut dari kecil ke besar. pas angka 10, 65, dan 90 ditambahin, tiga angka itu otomatis disisipin ke posisi sesuai urutannya
    *   Awal: `[20, 30, 40, 50, 60, 70, 80]`
    *   Akhir: `[10, 20, 30, 40, 50, 60, 65, 70, 80, 90]`
*   **Preorder (Root - Kiri - Kanan):**
    Preorder mencerminkan bagaimana alur penelusuran (penciptaan) node dari atas ke bawah. 
    *   `10` menjadi anak kiri dari `20`, sehingga muncul setelah `20`.
    *   `65` menjadi anak kanan dari `60`, sehingga dieksekusi setelah `60`.
    *   `90` menjadi anak kanan dari `80`, sehingga dieksekusi di bagian paling akhir urutan.
*   **Postorder (Kiri - Kanan - Root):**
    Postorder mengeksekusi "daun" (leaf) terlebih dahulu sebelum kembali ke induknya (root). 
    *   Karena `10`, `65`, dan `90` dimasukkan terakhir dan menjadi ujung daun yang baru (leaf nodes), mereka akan tercetak lebih awal untuk sub-tree masing-masing sebelum induknya (misal: `10` dicetak sebelum induknya `20`).
""")
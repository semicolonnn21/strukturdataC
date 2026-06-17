import streamlit as st
import graphviz
import pandas as pd

# 1. Definisi Struktur Data
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

    def visualize(self):
        dot = graphviz.Digraph(node_attr={'color': 'darkgreen', 'style': 'filled', 'fillcolor': 'honeydew'})
        if not self.root:
            return dot
        
        def add_nodes_edges(node):
            dot.node(str(node.value), str(node.value))
            if node.left:
                dot.edge(str(node.value), str(node.left.value), color='blue', label=' L')
                add_nodes_edges(node.left)
            if node.right:
                dot.edge(str(node.value), str(node.right.value), color='red', label=' R')
                add_nodes_edges(node.right)
        
        add_nodes_edges(self.root)
        return dot

    def get_preorder(self, root, res):
        if root:
            res.append(root.value)
            self.get_preorder(root.left, res)
            self.get_preorder(root.right, res)
        return res

    def get_inorder(self, root, res):
        if root:
            self.get_inorder(root.left, res)
            res.append(root.value)
            self.get_inorder(root.right, res)
        return res

    def get_postorder(self, root, res):
        if root:
            self.get_postorder(root.left, res)
            self.get_postorder(root.right, res)
            res.append(root.value)
        return res

# 2. Antarmuka Streamlit
st.set_page_config(page_title="BST Analysis Tool", layout="wide")
st.title("🌳 Analisis Mendalam Binary Search Tree")
st.markdown("Alat ini memvisualisasikan perubahan struktur BST setelah penambahan data baru.")

# Dataset
data_awal = [50, 30, 70, 20, 40, 60, 80]
data_tambahan = [10, 90, 65]
total_data = data_awal + data_tambahan

# Build Tree
tree = BST()
for item in total_data:
    tree.root = tree.insert(tree.root, item)

# Layout Utama
col1, col2 = st.columns([1.2, 1])

with col1:
    st.subheader("Visualisasi Struktur Pohon")
    st.graphviz_chart(tree.visualize())
    st.caption("🔵 Garis Biru: Jalur Kiri (<) | 🔴 Garis Merah: Jalur Kanan (>)")

with col2:
    st.subheader("Hasil Traversal Terbaru")
    
    pre = tree.get_preorder(tree.root, [])
    ino = tree.get_inorder(root=tree.root, res=[])
    post = tree.get_postorder(tree.root, [])

    st.success(f"**Preorder:**  \n`{' → '.join(map(str, pre))}`")
    st.info(f"**Inorder:**  \n`{' → '.join(map(str, ino))}`")
    st.warning(f"**Postorder:**  \n`{' → '.join(map(str, post))}`")

    st.divider()
    st.subheader("📊 Tabel Perbandingan Traversal")
    
    # Membuat DataFrame dengan Indeks eksplisit (1, 2, 3)
    df_compare = pd.DataFrame({
        "Metode": ["Preorder", "Inorder", "Postorder"],
        "Sebelum (Awal)": [
            "50, 30, 20, 40, 70, 60, 80",
            "20, 30, 40, 50, 60, 70, 80",
            "20, 40, 30, 60, 80, 70, 50"
        ],
        "Sesudah (Update)": [
            ", ".join(map(str, pre)),
            ", ".join(map(str, ino)),
            ", ".join(map(str, post))
        ]
    })
    
    # Mengatur indeks agar dimulai dari 1
    df_compare.index = df_compare.index + 1
    st.table(df_compare)

st.divider()

# 3. Bagian Analisis
# 3. Bagian Analisis Lengkap
st.subheader("📝 Analisis Perubahan Struktur & Traversal")

# Menggunakan Container atau Expander agar lebih rapi
with st.container():
    st.markdown("""
    Penambahan node **10, 65, dan 90** bikin struktur BST berubah, jadi hasil traversalnya juga otomatis ikut berubah.
    
    
    #### Posisi Node Baru:
    *   **10** → Masuk ke **kiri** dari node 20.
    *   **65** → Masuk ke **kanan** dari node 60.
    *   **90** → Masuk ke **kanan** dari node 80.


    #### Analisis Perubahan Traversal:
    
    **1. Preorder (Root → Left → Right)**
    *   **Hasil:** `50, 30, 20, 10, 40, 70, 60, 65, 80, 90`
    *   **Apa yang berubah?** 
        *   Node 10 muncul tepat setelah 20 karena dia anak kiri 20.
        *   Node 65 muncul setelah 60 karena dia anak kanan 60.
        *   Node 90 muncul di paling akhir setelah 80.

    **2. Inorder (Left → Root → Right)**
    *   **Hasil:** `10, 20, 30, 40, 50, 60, 65, 70, 80, 90`
    *   **Apa yang berubah?**
        *   Angka 10 geser ke posisi paling awal (paling kecil).
        *   Angka 65 nyelip di antara 60 dan 70.
        *   Angka 90 sekarang jadi yang paling akhir.
        *   *Catatan:* Traversal Inorder **tetap berurutan** dari kecil ke besar (ciri khas BST).

    **3. Postorder (Left → Right → Root)**
    *   **Hasil:** `10, 20, 40, 30, 65, 60, 90, 80, 70, 50`
    *   **Apa yang berubah?**
        *   10 sekarang diproses sebelum 20.
        *   65 diproses sebelum 60.
        *   90 diproses sebelum 80.
    """)
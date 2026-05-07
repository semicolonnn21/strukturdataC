import streamlit as st
import graphviz

# --- 1. LOGIKA DATA STRUCTURE (BST) ---
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

    def get_preorder(self, root, res):
        if root:
            res.append(str(root.value))
            self.get_preorder(root.left, res)
            self.get_preorder(root.right, res)
        return res

    def get_inorder(self, root, res):
        if root:
            self.get_inorder(root.left, res)
            res.append(str(root.value))
            self.get_inorder(root.right, res)
        return res

    def get_postorder(self, root, res):
        if root:
            self.get_postorder(root.left, res)
            self.get_postorder(root.right, res)
            res.append(str(root.value))
        return res

# --- 2. FUNGSI GAMBAR POHON ---
def draw_tree(root, dot=None):
    if dot is None:
        dot = graphviz.Digraph()
        # Mengatur tampilan node jadi bulat pink
        dot.attr('node', shape='circle', style='filled', color='#FF69B4', fontcolor='white', fontname='Arial-Bold')
    
    if root:
        if root.left:
            dot.edge(str(root.value), str(root.left.value))
            draw_tree(root.left, dot)
        if root.right:
            dot.edge(str(root.value), str(root.right.value))
            draw_tree(root.right, dot)
    return dot

# --- 3. TAMPILAN STREAMLIT (UI) ---
st.set_page_config(page_title="Tugas BST Nona Cantik", layout="wide")

# Judul Pink Bold
st.markdown("<h1 style='text-align: center; color: #FF69B4;'><b>🌳 Implementasi Tree Data Structure</b></h1>", unsafe_allow_html=True)
st.write("---")

# Kolom untuk perbandingan
col1, col2 = st.columns(2)

# --- BAGIAN 1: KONDISI AWAL ---
tree = BST()
data_awal = [50, 30, 70, 20, 40, 60, 80]
for x in data_awal:
    tree.root = tree.insert(tree.root, x)

with col1:
    st.markdown("<h3 style='color: #FF69B4;'><b>1. Hasil Traversal Awal</b></h3>", unsafe_allow_html=True)
    st.graphviz_chart(draw_tree(tree.root))
    
    st.write("**Hasil Traversal:**")
    st.success(f"**Preorder:** {', '.join(tree.get_preorder(tree.root, []))}")
    st.info(f"**Inorder:** {', '.join(tree.get_inorder(tree.root, []))}")
    st.warning(f"**Postorder:** {', '.join(tree.get_postorder(tree.root, []))}")

# --- BAGIAN 2: SETELAH TAMBAH NODE ---
nodes_baru = [10, 90, 65]
for x in nodes_baru:
    tree.root = tree.insert(tree.root, x)

with col2:
    st.markdown("<h3 style='color: #FF69B4;'><b>2. Hasil Setelah Tambah Node (10, 90, 65)</b></h3>", unsafe_allow_html=True)
    st.graphviz_chart(draw_tree(tree.root))
    
    st.write("**Hasil Traversal Baru:**")
    st.success(f"**Preorder:** {', '.join(tree.get_preorder(tree.root, []))}")
    st.info(f"**Inorder:** {', '.join(tree.get_inorder(tree.root, []))}")
    st.warning(f"**Postorder:** {', '.join(tree.get_postorder(tree.root, []))}")

# --- BAGIAN 3: ANALISIS ---
st.markdown("<br><h2 style='color: #FF69B4;'><b>📝 Analisis Perubahan</b></h2>", unsafe_allow_html=True)
st.info("""
1. **Node 10**: Menjadi anak kiri dari 20 karena nilainya paling kecil.
2. **Node 90**: Menjadi anak kanan dari 80 karena nilainya paling besar.
3. **Node 65**: Menjadi anak kanan dari 60 karena 65 > 60.
4. **Traversal Inorder**: Selalu menghasilkan urutan angka yang rapi dari terkecil ke terbesar.
""")
import streamlit as st
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

    def preorder(self, root, res=[]):
        if root:
            res.append(root.value)
            self.preorder(root.left, res)
            self.preorder(root.right, res)
        return res

    def inorder(self, root, res=[]):
        if root:
            self.inorder(root.left, res)
            res.append(root.value)
            self.inorder(root.right, res)
        return res

    def postorder(self, root, res=[]):
        if root:
            self.postorder(root.left, res)
            self.postorder(root.right, res)
            res.append(root.value)
        return res

def get_positions(node, depth=0, left=0.0, right=1.0, pos={}):
    if node is None:
        return pos
    mid = (left + right) / 2
    pos[node.value] = (mid, -depth)
    get_positions(node.left,  depth+1, left, mid, pos)
    get_positions(node.right, depth+1, mid, right, pos)
    return pos

def get_edges(node, edges=[]):
    if node is None:
        return edges
    if node.left:
        edges.append((node.value, node.left.value))
        get_edges(node.left, edges)
    if node.right:
        edges.append((node.value, node.right.value))
        get_edges(node.right, edges)
    return edges

def draw_tree(root, new_nodes=set()):
    pos   = get_positions(root, pos={})
    edges = get_edges(root, edges=[])

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.axis("off")

    for p, c in edges:
        px, py = pos[p]
        cx, cy = pos[c]
        ax.plot([px, cx], [py, cy], 'k-', lw=1.5)

    for val, (x, y) in pos.items():
        color = "#a78bfa" if val in new_nodes else "#60a5fa"
        circle = plt.Circle((x, y), 0.04, color=color, zorder=2)
        ax.add_patch(circle)
        ax.text(x, y, str(val), ha='center', va='center',
                fontsize=10, fontweight='bold', color='white', zorder=3)

    xs = [v[0] for v in pos.values()]
    ys = [v[1] for v in pos.values()]
    ax.set_xlim(min(xs)-0.08, max(xs)+0.08)
    ax.set_ylim(min(ys)-0.1,  max(ys)+0.1)
    plt.tight_layout()
    return fig

# ── App ──────────────────────────────────────
st.title("🌳 BST Visualizer")

# Build tree
tree = BST()
for v in [50, 30, 70, 20, 40, 60, 80]:
    tree.root = tree.insert(tree.root, v)

# Tambah node baru
add_new = st.checkbox("Tambahkan node baru: 10, 90, 65")
new_nodes = set()
if add_new:
    for v in [10, 90, 65]:
        tree.root = tree.insert(tree.root, v)
        new_nodes.add(v)

# Gambar tree
st.subheader("Struktur Tree")
st.caption("🔵 Node awal   🟣 Node baru")
st.pyplot(draw_tree(tree.root, new_nodes))

# Traversal
st.subheader("Hasil Traversal")
col1, col2, col3 = st.columns(3)
col1.markdown("**Preorder**")
col1.write(tree.preorder(tree.root, []))
col2.markdown("**Inorder**")
col2.write(tree.inorder(tree.root, []))
col3.markdown("**Postorder**")
col3.write(tree.postorder(tree.root, []))

# Analisis Kesimpulan
st.subheader("Analisis Perubahan Traversal")

st.markdown("**1. Preorder** (Root → Kiri → Kanan)")
st.table({
    "": ["Sebelum", "Sesudah"],
    "Hasil": [
        "50 → 30 → 20 → 40 → 70 → 60 → 80",
        "50 → 30 → 20 → 10 → 40 → 70 → 60 → 65 → 80 → 90"
    ]
})
st.markdown("""
- Node **10** muncul setelah 20 → anak kiri dari 20
- Node **65** muncul setelah 60 → anak kanan dari 60
- Node **90** muncul setelah 80 → anak kanan dari 80
""")

st.markdown("**2. Inorder** (Kiri → Root → Kanan)")
st.table({
    "": ["Sebelum", "Sesudah"],
    "Hasil": [
        "20 → 30 → 40 → 50 → 60 → 70 → 80",
        "10 → 20 → 30 → 40 → 50 → 60 → 65 → 70 → 80 → 90"
    ]
})
st.markdown("""
- Selalu terurut **naik** — sifat utama BST
- Node baru otomatis masuk di posisi yang benar
""")

st.markdown("**3. Postorder** (Kiri → Kanan → Root)")
st.table({
    "": ["Sebelum", "Sesudah"],
    "Hasil": [
        "20 → 40 → 30 → 60 → 80 → 70 → 50",
        "10 → 20 → 40 → 30 → 65 → 60 → 90 → 80 → 70 → 50"
    ]
})
st.markdown("""
- Root **(50)** selalu muncul **paling akhir**
- Setiap subtree diproses tuntas sebelum parent-nya
""")

st.success("""
**Kesimpulan:**
- Inorder selalu menghasilkan urutan terurut pada BST, dia tidak berubah, hanya bertambah 3 elemen baru di posisi yang benar
- Preorder dan Postorder berubah karena path traversal melewati cabang baru (10 di bawah 20, 65 di bawah 60, 90 di bawah 80)
- Penambahan node tidak mengubah posisi node yang lama, tapi hanya menambahkan cabang di leaf saja
""")
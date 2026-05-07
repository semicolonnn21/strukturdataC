import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ─── BST Implementation ───────────────────────────────────────────────────────

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
        if result is None:
            result = []
        if root:
            result.append(root.value)
            self.preorder(root.left, result)
            self.preorder(root.right, result)
        return result

    def inorder(self, root, result=None):
        if result is None:
            result = []
        if root:
            self.inorder(root.left, result)
            result.append(root.value)
            self.inorder(root.right, result)
        return result

    def postorder(self, root, result=None):
        if result is None:
            result = []
        if root:
            self.postorder(root.left, result)
            self.postorder(root.right, result)
            result.append(root.value)
        return result


# ─── Tree Position Calculator ─────────────────────────────────────────────────

def compute_positions(node, depth=0, counter=[0], pos={}):
    if node is None:
        return
    compute_positions(node.left, depth + 1, counter, pos)
    pos[node.value] = (counter[0], -depth)
    counter[0] += 1
    compute_positions(node.right, depth + 1, counter, pos)
    return pos


def get_edges(node, edges=None):
    if edges is None:
        edges = []
    if node:
        if node.left:
            edges.append((node.value, node.left.value))
            get_edges(node.left, edges)
        if node.right:
            edges.append((node.value, node.right.value))
            get_edges(node.right, edges)
    return edges


def draw_tree(root, highlight_nodes=None, title="Binary Search Tree"):
    if root is None:
        return None

    pos = compute_positions(root, counter=[0], pos={})
    edges = get_edges(root)

    fig, ax = plt.subplots(figsize=(14, 7))
    fig.patch.set_facecolor("#0f172a")
    ax.set_facecolor("#0f172a")

    # Draw edges
    for parent, child in edges:
        x1, y1 = pos[parent]
        x2, y2 = pos[child]
        ax.plot([x1, x2], [y1, y2], color="#475569", linewidth=2, zorder=1)

    # Draw nodes
    new_nodes = {10, 90, 65}
    initial_nodes = {50, 30, 70, 20, 40, 60, 80}

    for value, (x, y) in pos.items():
        if highlight_nodes and value in highlight_nodes:
            color = "#f59e0b"     # amber – highlighted traversal
            text_color = "#0f172a"
        elif value in new_nodes:
            color = "#22d3ee"     # cyan – newly added
            text_color = "#0f172a"
        else:
            color = "#6366f1"     # indigo – original
            text_color = "white"

        circle = plt.Circle((x, y), 0.35, color=color, zorder=3)
        ax.add_patch(circle)
        ax.text(x, y, str(value), ha="center", va="center",
                fontsize=11, fontweight="bold", color=text_color, zorder=4)

    # Legend
    legend_items = [
        mpatches.Patch(color="#6366f1", label="Node Awal"),
        mpatches.Patch(color="#22d3ee", label="Node Baru (10, 90, 65)"),
        mpatches.Patch(color="#f59e0b", label="Node Traversal Aktif"),
    ]
    ax.legend(handles=legend_items, loc="upper left",
              facecolor="#1e293b", edgecolor="#475569",
              labelcolor="white", fontsize=9)

    ax.set_title(title, color="white", fontsize=14, fontweight="bold", pad=12)
    ax.axis("off")

    all_x = [v[0] for v in pos.values()]
    all_y = [v[1] for v in pos.values()]
    ax.set_xlim(min(all_x) - 1, max(all_x) + 1)
    ax.set_ylim(min(all_y) - 1, max(all_y) + 1)

    plt.tight_layout()
    return fig


# ─── Streamlit App ────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="BST Visualizer",
    page_icon="🌳",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    body, .stApp { background-color: #0f172a; color: #e2e8f0; }
    .block-container { padding: 2rem 2rem 2rem 2rem; }
    h1, h2, h3 { color: #e2e8f0 !important; }
    .stMetric { background: #1e293b; border-radius: 10px; padding: 10px; }
    .traversal-box {
        background: #1e293b;
        border-left: 4px solid #6366f1;
        border-radius: 8px;
        padding: 12px 16px;
        margin: 8px 0;
        font-family: monospace;
        font-size: 14px;
        color: #e2e8f0;
    }
    .new-node-box {
        background: #1e293b;
        border-left: 4px solid #22d3ee;
        border-radius: 8px;
        padding: 12px 16px;
        margin: 8px 0;
        font-family: monospace;
        font-size: 14px;
        color: #e2e8f0;
    }
    .analysis-box {
        background: #1e293b;
        border-left: 4px solid #f59e0b;
        border-radius: 8px;
        padding: 12px 16px;
        margin: 8px 0;
        color: #e2e8f0;
        font-size: 14px;
    }
    div[data-testid="stHorizontalBlock"] > div {
        background: #1e293b;
        border-radius: 10px;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ─── Build Trees ──────────────────────────────────────────────────────────────

# Initial BST
tree_awal = BST()
data_awal = [50, 30, 70, 20, 40, 60, 80]
for item in data_awal:
    tree_awal.root = tree_awal.insert(tree_awal.root, item)

pre_awal  = tree_awal.preorder(tree_awal.root)
in_awal   = tree_awal.inorder(tree_awal.root)
post_awal = tree_awal.postorder(tree_awal.root)

# Final BST (with new nodes)
tree_final = BST()
data_final = [50, 30, 70, 20, 40, 60, 80, 10, 90, 65]
for item in data_final:
    tree_final.root = tree_final.insert(tree_final.root, item)

pre_final  = tree_final.preorder(tree_final.root)
in_final   = tree_final.inorder(tree_final.root)
post_final = tree_final.postorder(tree_final.root)

# ─── Header ──────────────────────────────────────────────────────────────────

st.title("🌳 Binary Search Tree – Visualizer")
st.markdown("**Modul Tree | Struktur Data** — Implementasi & Analisis BST dengan Traversal")
st.markdown("---")

# ─── Section 1 : BST Awal ────────────────────────────────────────────────────

st.subheader("📌 Tugas 1 – BST Awal: `[50, 30, 70, 20, 40, 60, 80]`")

col1, col2 = st.columns([1.2, 1])

with col1:
    fig_awal = draw_tree(tree_awal.root, title="BST Awal")
    st.pyplot(fig_awal)
    plt.close()

with col2:
    st.markdown("**Hasil Traversal BST Awal:**")
    st.markdown(f'<div class="traversal-box">🔵 <b>Preorder</b>  (Root→L→R):<br>{" → ".join(map(str, pre_awal))}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="traversal-box">🟢 <b>Inorder</b>   (L→Root→R):<br>{" → ".join(map(str, in_awal))}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="traversal-box">🔴 <b>Postorder</b> (L→R→Root):<br>{" → ".join(map(str, post_awal))}</div>', unsafe_allow_html=True)
    st.info("💡 Inorder menghasilkan urutan **ascending** karena properti BST: semua node kiri < root < semua node kanan.")

st.markdown("---")

# ─── Section 2 : Penambahan Node ─────────────────────────────────────────────

st.subheader("📌 Tugas 2 & 3 – Setelah Penambahan Node: `10, 90, 65`")

col3, col4 = st.columns([1.2, 1])

with col3:
    fig_final = draw_tree(tree_final.root, title="BST Setelah Penambahan Node 10, 90, 65")
    st.pyplot(fig_final)
    plt.close()

with col4:
    st.markdown("**Node yang Ditambahkan:**")
    node_info = {
        10: "Anak kiri node 20  →  (10 < 50 → 30 → 20)",
        90: "Anak kanan node 80 →  (90 > 50 → 70 → 80)",
        65: "Anak kanan node 60 →  (65 > 50 → 70 < 60 → 65)",
    }
    for n, path in node_info.items():
        st.markdown(f'<div class="new-node-box">🩵 <b>Node {n}</b>: {path}</div>', unsafe_allow_html=True)

    st.markdown("**Hasil Traversal Setelah Penambahan:**")
    st.markdown(f'<div class="traversal-box">🔵 <b>Preorder</b> :<br>{" → ".join(map(str, pre_final))}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="traversal-box">🟢 <b>Inorder</b>  :<br>{" → ".join(map(str, in_final))}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="traversal-box">🔴 <b>Postorder</b>:<br>{" → ".join(map(str, post_final))}</div>', unsafe_allow_html=True)

st.markdown("---")

# ─── Section 3 : Analisis ────────────────────────────────────────────────────

st.subheader("📌 Tugas 4 – Analisis Perubahan Traversal")

analysis = [
    ("Preorder", pre_awal, pre_final,
     "Root 50 tetap pertama. Node 10, 90, dan 65 muncul di posisi sesuai letak mereka dalam subtree masing-masing. Urutan kunjungan berubah karena ada cabang baru yang harus dikunjungi."),
    ("Inorder", in_awal, in_final,
     "Tetap terurut ascending. Node 10 masuk di awal (nilai terkecil), 65 di antara 60-70, dan 90 di akhir (nilai terbesar). Ini membuktikan properti BST terjaga dengan benar."),
    ("Postorder", post_awal, post_final,
     "Root 50 tetap di posisi terakhir. Node daun baru (10, 90, 65) dikunjungi sebelum induknya masing-masing, sesuai prinsip Postorder: anak-anak selesai sebelum orang tua."),
]

for name, before, after, note in analysis:
    with st.expander(f"📊 {name} — Perubahan Detail", expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"**Sebelum ({len(before)} node):**")
            st.markdown(f'<div class="traversal-box">{" → ".join(map(str, before))}</div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f"**Sesudah ({len(after)} node):**")
            st.markdown(f'<div class="traversal-box">{" → ".join(map(str, after))}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="analysis-box">📝 {note}</div>', unsafe_allow_html=True)

st.markdown("---")

# ─── Section 4 : Perbandingan Statistik ──────────────────────────────────────

st.subheader("📌 Statistik BST")

col5, col6, col7, col8 = st.columns(4)
col5.metric("Node Awal", len(data_awal))
col6.metric("Node Ditambahkan", 3)
col7.metric("Total Node", len(data_final))
col8.metric("Tinggi Tree", 4)

st.markdown("---")
st.caption("🌳 Dibuat untuk tugas Modul Tree – Struktur Data | BST Visualization with Streamlit")

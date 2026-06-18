import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# page Config
st.set_page_config(page_title="BST Visualizer", page_icon="🌳", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Space+Grotesk:wght@300;500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
}
code, pre, .mono { font-family: 'JetBrains Mono', monospace; }

h1, h2, h3 { font-family: 'Space Grotesk', sans-serif; font-weight: 700; }

.stApp { background: #0f1117; color: #e8eaf0; }

.card {
    background: #1a1d2e;
    border: 1px solid #2a2d3e;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1rem;
}

.traversal-box {
    background: #0d1117;
    border-left: 3px solid #58a6ff;
    border-radius: 0 8px 8px 0;
    padding: 0.6rem 1rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.95rem;
    color: #79c0ff;
    margin: 0.3rem 0;
    letter-spacing: 0.05em;
}
.traversal-box.inorder  { border-color: #3fb950; color: #7ee787; }
.traversal-box.postorder{ border-color: #d29922; color: #e3b341; }

.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
    margin-right: 6px;
    font-family: 'JetBrains Mono', monospace;
}
.badge-pre  { background:#1f3a5f; color:#58a6ff; }
.badge-in   { background:#1a3a2a; color:#3fb950; }
.badge-post { background:#3a2e10; color:#d29922; }

.analysis-item {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 8px;
    padding: 0.7rem 1rem;
    margin: 0.4rem 0;
    font-size: 0.9rem;
    line-height: 1.6;
}
.highlight { color: #58a6ff; font-weight: 600; }
.green { color: #3fb950; }

.section-title {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #8b949e;
    margin-bottom: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# BST Implementation
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

# Tree Visualization
def get_positions(root, x=0, y=0, gap=1.5, positions=None, edges=None):
    if positions is None: positions = {}
    if edges is None: edges = []
    if root:
        positions[root.value] = (x, y)
        if root.left:
            edges.append((root.value, root.left.value))
            get_positions(root.left,  x - gap, y - 1.2, gap / 1.7, positions, edges)
        if root.right:
            edges.append((root.value, root.right.value))
            get_positions(root.right, x + gap, y - 1.2, gap / 1.7, positions, edges)
    return positions, edges

def draw_tree(root, highlight_nodes=None, title=""):
    positions, edges = get_positions(root)
    if not positions:
        return None

    fig, ax = plt.subplots(figsize=(11, 6))
    fig.patch.set_facecolor('#0f1117')
    ax.set_facecolor('#0f1117')

    # Draw edges
    for (u, v) in edges:
        x1, y1 = positions[u]
        x2, y2 = positions[v]
        ax.plot([x1, x2], [y1, y2], color='#30363d', linewidth=1.8, zorder=1)

    # Draw nodes
    for val, (x, y) in positions.items():
        is_new = highlight_nodes and val in highlight_nodes
        face  = '#238636' if is_new else '#1f6feb'
        edge_c = '#3fb950' if is_new else '#58a6ff'
        circle = plt.Circle((x, y), 0.38, color=face, zorder=2)
        ax.add_patch(circle)
        circle2 = plt.Circle((x, y), 0.38, fill=False, edgecolor=edge_c, linewidth=2, zorder=3)
        ax.add_patch(circle2)
        ax.text(x, y, str(val), ha='center', va='center',
                fontsize=11, fontweight='bold', color='white',
                fontfamily='monospace', zorder=4)

    # Legend
    if highlight_nodes:
        p1 = mpatches.Patch(color='#1f6feb', label='Node Awal')
        p2 = mpatches.Patch(color='#238636', label='Node Baru')
        ax.legend(handles=[p1, p2], loc='upper right',
                  facecolor='#161b22', edgecolor='#30363d',
                  labelcolor='white', fontsize=9)

    all_x = [p[0] for p in positions.values()]
    all_y = [p[1] for p in positions.values()]
    ax.set_xlim(min(all_x) - 1, max(all_x) + 1)
    ax.set_ylim(min(all_y) - 0.8, max(all_y) + 0.8)
    ax.axis('off')
    if title:
        ax.set_title(title, color='#8b949e', fontsize=10, pad=10, fontfamily='monospace')
    plt.tight_layout()
    return fig

# Build Trees
data_awal   = [50, 30, 70, 20, 40, 60, 80]
data_tambah = [10, 90, 65]

tree_awal = BST()
for v in data_awal:
    tree_awal.root = tree_awal.insert(tree_awal.root, v)

tree_baru = BST()
for v in data_awal + data_tambah:
    tree_baru.root = tree_baru.insert(tree_baru.root, v)

# Head
st.markdown("# 🌳 BST Visualizer")
st.markdown("<p style='color:#8b949e; margin-top:-0.5rem;'>Binary Search Tree__Traversal</p>", unsafe_allow_html=True)
st.markdown("---")

# Layout
tab1, tab2, tab3 = st.tabs(["BST Awal", "+ Setelah Tambah Node", "Analisis"])

# TAB 1: BST Awal
with tab1:
    col1, col2 = st.columns([3, 2], gap="large")

    with col1:
        st.markdown("<div class='section-title'>Visualisasi Tree</div>", unsafe_allow_html=True)
        fig1 = draw_tree(tree_awal.root, title="Data: [50, 30, 70, 20, 40, 60, 80]")
        st.pyplot(fig1)

    with col2:
        st.markdown("<div class='section-title'>Traversal</div>", unsafe_allow_html=True)

        pre  = tree_awal.preorder(tree_awal.root)
        ino  = tree_awal.inorder(tree_awal.root)
        post = tree_awal.postorder(tree_awal.root)

        st.markdown("<span class='badge badge-pre'>PREORDER</span>", unsafe_allow_html=True)
        st.markdown(f"<div class='traversal-box'>{' → '.join(map(str, pre))}</div>", unsafe_allow_html=True)

        st.markdown("<span class='badge badge-in'>INORDER</span>", unsafe_allow_html=True)
        st.markdown(f"<div class='traversal-box inorder'>{' → '.join(map(str, ino))}</div>", unsafe_allow_html=True)

        st.markdown("<span class='badge badge-post'>POSTORDER</span>", unsafe_allow_html=True)
        st.markdown(f"<div class='traversal-box postorder'>{' → '.join(map(str, post))}</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class='card'>
            <div class='section-title'>Info</div>
            <div style='font-size:0.9rem; color:#8b949e; line-height:1.8'>
                • Jumlah Node: <span class='highlight'>{len(data_awal)}</span><br>
                • Root: <span class='highlight'>50</span><br>
                • Height: <span class='highlight'>3</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# TAB 2: Setelah Tambah Node
with tab2:
    col1, col2 = st.columns([3, 2], gap="large")

    with col1:
        st.markdown("<div class='section-title'>Visualisasi Tree (Node Baru = Hijau)</div>", unsafe_allow_html=True)
        fig2 = draw_tree(tree_baru.root, highlight_nodes=set(data_tambah),
                         title="Tambahan: 10, 90, 65")
        st.pyplot(fig2)

    with col2:
        st.markdown("<div class='section-title'>Traversal Baru</div>", unsafe_allow_html=True)

        pre2  = tree_baru.preorder(tree_baru.root)
        ino2  = tree_baru.inorder(tree_baru.root)
        post2 = tree_baru.postorder(tree_baru.root)

        st.markdown("<span class='badge badge-pre'>PREORDER</span>", unsafe_allow_html=True)
        st.markdown(f"<div class='traversal-box'>{' → '.join(map(str, pre2))}</div>", unsafe_allow_html=True)

        st.markdown("<span class='badge badge-in'>INORDER</span>", unsafe_allow_html=True)
        st.markdown(f"<div class='traversal-box inorder'>{' → '.join(map(str, ino2))}</div>", unsafe_allow_html=True)

        st.markdown("<span class='badge badge-post'>POSTORDER</span>", unsafe_allow_html=True)
        st.markdown(f"<div class='traversal-box postorder'>{' → '.join(map(str, post2))}</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class='card'>
            <div class='section-title'>Info</div>
            <div style='font-size:0.9rem; color:#8b949e; line-height:1.8'>
                • Jumlah Node: <span class='highlight'>{len(data_awal) + len(data_tambah)}</span><br>
                • Root: <span class='highlight'>50</span><br>
                • Height: <span class='highlight'>4</span><br>
                • BST Property: <span class='green'>Terjaga</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# TAB 3: Analisis
with tab3:
    st.markdown("<div class='section-title'>Analisis Penempatan Node Baru</div>", unsafe_allow_html=True)

    analysis = [
        ("Node 10", "58a6ff", "50 → 30 → 20", "Left child dari <b>20</b>", "10 &lt; 50, 10 &lt; 30, 10 &lt; 20 → masuk kiri terus"),
        ("Node 90", "3fb950", "50 → 70 → 80", "Right child dari <b>80</b>", "90 &gt; 50, 90 &gt; 70, 90 &gt; 80 → masuk kanan terus"),
        ("Node 65", "d29922", "50 → 70 → 60", "Right child dari <b>60</b>", "65 &gt; 50, 65 &lt; 70, 65 &gt; 60 → kanan, kiri, kanan"),
    ]

    for node, color, path, pos, logic in analysis:
        st.markdown(f"""
        <div class='analysis-item'>
            <span style='color:#{color}; font-weight:700; font-family:monospace;'>{node}</span>
            &nbsp;·&nbsp; Path: <span style='color:#8b949e; font-family:monospace;'>{path}</span>
            &nbsp;→&nbsp; <span style='color:#{color};'>{pos}</span><br>
            <span style='color:#6e7681; font-size:0.85rem;'>{logic}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><div class='section-title'>Dampak Pada Traversal</div>", unsafe_allow_html=True)

    impacts = [
        ("badge-pre",  "PREORDER",  "10 muncul setelah 20 | 65 muncul setelah 60 | 90 muncul setelah 80"),
        ("badge-in",   "INORDER",   "Urutan tetap ascending: 10 20 30 40 50 60 65 70 80 90 → BST property terjaga ✓"),
        ("badge-post", "POSTORDER", "10 muncul sebelum 20 | 65 muncul sebelum 60 | 90 muncul sebelum 80"),
    ]

    for badge, label, desc in impacts:
        st.markdown(f"""
        <div class='analysis-item'>
            <span class='badge {badge}'>{label}</span><br>
            <span style='color:#8b949e; font-size:0.88rem; font-family:monospace;'>{desc}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class='card' style='margin-top:1rem; border-color:#1f6feb;'>
        <div class='section-title'> Kesimpulan</div>
        <div style='font-size:0.9rem; color:#8b949e; line-height:1.8'>
            BST selalu menempatkan node lebih kecil ke <span class='highlight'>kiri</span> dan lebih besar ke <span class='highlight'>kanan</span>.<br>
            Jadi, <span class='green'>Inorder traversal</span> selalu menghasilkan urutan <b>ascending</b> ini adalah sifat paling berguna dari BST.
        </div>
    </div>
    """, unsafe_allow_html=True)
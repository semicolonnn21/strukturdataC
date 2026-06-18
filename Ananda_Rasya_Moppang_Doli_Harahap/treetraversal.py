import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import time

st.set_page_config(page_title="BST Visualizer", page_icon="🌳", layout="wide")

# ─────────────────────────── BST Logic ───────────────────────────
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


def build_tree(values):
    tree = BST()
    for v in values:
        tree.root = tree.insert(tree.root, v)
    return tree


# ─────────────────────────── Tree Layout ───────────────────────────
def get_positions(node, pos=None, x=0, y=0, layer=1):
    if pos is None:
        pos = {}
    if node:
        pos[node.value] = (x, y)
        gap = 2.5 / layer
        get_positions(node.left,  pos, x - gap, y - 1.5, layer + 1)
        get_positions(node.right, pos, x + gap, y - 1.5, layer + 1)
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


# ─────────────────────────── Draw Tree ───────────────────────────
def draw_tree(tree, highlight=None, visited=None, new_nodes=None, title="BST"):
    if highlight is None:
        highlight = set()
    if visited is None:
        visited = set()
    if new_nodes is None:
        new_nodes = set()

    pos = get_positions(tree.root)
    edges = get_edges(tree.root)

    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor('#0E1117')
    ax.set_facecolor('#0E1117')

    # Draw edges
    for parent, child in edges:
        x_vals = [pos[parent][0], pos[child][0]]
        y_vals = [pos[parent][1], pos[child][1]]
        ax.plot(x_vals, y_vals, color='#4A5568', linewidth=1.5, zorder=1)

    # Draw nodes
    for value, (x, y) in pos.items():
        if value in highlight:
            color = '#3182CE'      # blue – current
            text_color = 'white'
            ec = '#63B3ED'
            lw = 2.5
        elif value in visited:
            color = '#276749'      # green – visited
            text_color = 'white'
            ec = '#68D391'
            lw = 1.5
        elif value in new_nodes:
            color = '#744210'      # amber – new node
            text_color = '#FEFCBF'
            ec = '#F6AD55'
            lw = 1.5
        else:
            color = '#2D3748'      # dark gray – default
            text_color = '#E2E8F0'
            ec = '#718096'
            lw = 1.0

        circle = plt.Circle((x, y), 0.35, color=color, zorder=2, ec=ec, linewidth=lw)
        ax.add_patch(circle)
        ax.text(x, y, str(value), ha='center', va='center',
                fontsize=12, fontweight='bold', color=text_color, zorder=3)

    ax.set_xlim(-6, 6)
    ax.set_ylim(-6, 1.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(title, color='#E2E8F0', fontsize=14, fontweight='bold', pad=10)

    # Legend
    legend_items = [
        mpatches.Patch(color='#2D3748', ec='#718096', label='Node awal'),
        mpatches.Patch(color='#744210', ec='#F6AD55', label='Node baru (10, 90, 65)'),
        mpatches.Patch(color='#3182CE', ec='#63B3ED', label='Sedang dikunjungi'),
        mpatches.Patch(color='#276749', ec='#68D391', label='Sudah dikunjungi'),
    ]
    ax.legend(handles=legend_items, loc='lower left',
              facecolor='#1A202C', edgecolor='#4A5568',
              labelcolor='#E2E8F0', fontsize=9, framealpha=0.9)

    plt.tight_layout()
    return fig


# ─────────────────────────── Session State ───────────────────────────
ORIGINAL = [50, 30, 70, 20, 40, 60, 80]
NEW_NODES = [10, 90, 65]
FULL = ORIGINAL + NEW_NODES

if 'step' not in st.session_state:
    st.session_state.step = -1
if 'mode' not in st.session_state:
    st.session_state.mode = 'preorder'
if 'dataset' not in st.session_state:
    st.session_state.dataset = 'full'
if 'playing' not in st.session_state:
    st.session_state.playing = False


# ─────────────────────────── UI ───────────────────────────
st.markdown("""
<h1 style='text-align:center; color:#63B3ED; margin-bottom:4px'>🌳 BST Traversal Visualizer</h1>
<p style='text-align:center; color:#718096; font-size:14px; margin-bottom:20px'>
    Implementasi Binary Search Tree — Tugas Struktur Data
</p>
""", unsafe_allow_html=True)

# ── Controls ──
col_a, col_b, col_c = st.columns([1, 1, 1])

with col_a:
    st.markdown("**Dataset**")
    dataset = st.radio("", ["Original (7 node)", "Setelah tambah node (10 node)"],
                       index=0 if st.session_state.dataset == 'original' else 1,
                       key="ds_radio")
    st.session_state.dataset = 'original' if dataset.startswith("Original") else 'full'

with col_b:
    st.markdown("**Mode Traversal**")
    mode = st.radio("", ["Preorder (Root→L→R)", "Inorder (L→Root→R)", "Postorder (L→R→Root)"],
                    key="mode_radio")
    if mode.startswith("Pre"):
        st.session_state.mode = 'preorder'
    elif mode.startswith("In"):
        st.session_state.mode = 'inorder'
    else:
        st.session_state.mode = 'postorder'

with col_c:
    st.markdown("**Kontrol Animasi**")
    speed = st.slider("Kecepatan (detik/step)", 0.3, 2.0, 0.8, 0.1)
    b1, b2 = st.columns(2)
    with b1:
        if st.button("▶ Animasi", use_container_width=True, type="primary"):
            st.session_state.step = -1
            st.session_state.playing = True
    with b2:
        if st.button("↺ Reset", use_container_width=True):
            st.session_state.step = -1
            st.session_state.playing = False

st.divider()

# ── Build tree & traversal order ──
data = FULL if st.session_state.dataset == 'full' else ORIGINAL
tree = build_tree(data)
new_nodes_set = set(NEW_NODES) if st.session_state.dataset == 'full' else set()

m = st.session_state.mode
if m == 'preorder':
    order = tree.preorder(tree.root)
elif m == 'inorder':
    order = tree.inorder(tree.root)
else:
    order = tree.postorder(tree.root)

# ── Main layout: tree + traversal ──
col_tree, col_info = st.columns([2.2, 1])

with col_tree:
    tree_placeholder = st.empty()

with col_info:
    st.markdown("**Urutan Traversal**")
    token_placeholder = st.empty()
    step_placeholder = st.empty()

    st.markdown("---")
    st.markdown("**Hasil Lengkap**")

    tree2 = build_tree(data)
    pre = tree2.preorder(tree2.root)
    ino = tree2.inorder(tree2.root)
    post = tree2.postorder(tree2.root)

    st.markdown(f"**Preorder:**")
    st.code(" → ".join(map(str, pre)), language=None)
    st.markdown(f"**Inorder:**")
    st.code(" → ".join(map(str, ino)), language=None)
    st.markdown(f"**Postorder:**")
    st.code(" → ".join(map(str, post)), language=None)

    if st.session_state.dataset == 'full':
        st.markdown("---")
        st.markdown("**Analisis Node Baru**")
        st.markdown("""
- **10** → kiri dari 20 (10 < 20)
- **90** → kanan dari 80 (90 > 80)
- **65** → kanan dari 60, kiri dari 70
- Inorder tetap **ascending** ✓
""")


# ── Render current step ──
def render_step(step):
    if step < 0:
        visited = set()
        highlight = set()
        title_suffix = "— tekan ▶ untuk animasi"
    elif step < len(order):
        visited = set(order[:step])
        highlight = {order[step]}
        title_suffix = f"step {step+1}/{len(order)}: node {order[step]}"
    else:
        visited = set(order)
        highlight = set()
        title_suffix = "selesai ✓"

    mode_label = {'preorder': 'Preorder', 'inorder': 'Inorder', 'postorder': 'Postorder'}[st.session_state.mode]
    fig = draw_tree(tree, highlight=highlight, visited=visited,
                    new_nodes=new_nodes_set,
                    title=f"{mode_label} Traversal {title_suffix}")
    tree_placeholder.pyplot(fig)
    plt.close(fig)

    # Token row
    tokens_html = ""
    for i, v in enumerate(order):
        if i < (step if step >= 0 else -1):
            bg, color = "#276749", "#68D391"
        elif i == step:
            bg, color = "#2B6CB0", "#90CDF4"
        else:
            bg, color = "#2D3748", "#A0AEC0"
        tokens_html += f'<span style="display:inline-block;background:{bg};color:{color};padding:4px 10px;border-radius:6px;margin:3px;font-weight:bold;font-size:14px">{v}</span>'

    token_placeholder.markdown(tokens_html, unsafe_allow_html=True)

    if step < 0:
        step_placeholder.info("Pilih mode dan tekan ▶ Animasi")
    elif step < len(order):
        step_placeholder.success(f"🔵 Mengunjungi node **{order[step]}**")
    else:
        step_placeholder.success(f"✅ Traversal selesai! {len(order)} node dikunjungi")


# ── Animation loop ──
if st.session_state.playing:
    current = st.session_state.step
    if current < len(order):
        next_step = current + 1
        st.session_state.step = next_step
        render_step(next_step)
        time.sleep(speed)
        if next_step < len(order):
            st.rerun()
        else:
            st.session_state.playing = False
    else:
        st.session_state.playing = False
        render_step(st.session_state.step)
else:
    render_step(st.session_state.step)

# ── Step-by-step manual buttons ──
st.divider()
mc1, mc2, mc3, mc4 = st.columns([1, 1, 1, 3])
with mc1:
    if st.button("⏮ Awal"):
        st.session_state.step = -1
        st.session_state.playing = False
        st.rerun()
with mc2:
    if st.button("◀ Prev") and st.session_state.step > -1:
        st.session_state.step -= 1
        st.session_state.playing = False
        st.rerun()
with mc3:
    if st.button("Next ▶") and st.session_state.step < len(order):
        st.session_state.step += 1
        st.session_state.playing = False
        st.rerun()
with mc4:
    st.caption(f"Step {max(0,st.session_state.step+1)} / {len(order)} — mode: `{st.session_state.mode}` | dataset: `{st.session_state.dataset}`")
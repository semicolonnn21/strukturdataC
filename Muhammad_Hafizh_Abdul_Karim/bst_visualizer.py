import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BST Visualizer",
    page_icon="🌳",
    layout="wide"
)

# ─── BST Logic ────────────────────────────────────────────────────────────────
class BSTNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def insert(root, value):
    if root is None:
        return BSTNode(value)
    if value < root.value:
        root.left = insert(root.left, value)
    elif value > root.value:
        root.right = insert(root.right, value)
    return root

def preorder(root, result=None):
    if result is None: result = []
    if root:
        result.append(root.value)
        preorder(root.left, result)
        preorder(root.right, result)
    return result

def inorder(root, result=None):
    if result is None: result = []
    if root:
        inorder(root.left, result)
        result.append(root.value)
        inorder(root.right, result)
    return result

def postorder(root, result=None):
    if result is None: result = []
    if root:
        postorder(root.left, result)
        postorder(root.right, result)
        result.append(root.value)
    return result

def build_bst(data):
    root = None
    for v in data:
        root = insert(root, v)
    return root

# ─── Position Assignment (for drawing) ────────────────────────────────────────
def get_positions(node, depth=0, counter=None, pos=None):
    if counter is None: counter = [0]
    if pos is None: pos = {}
    if not node: return pos
    get_positions(node.left, depth + 1, counter, pos)
    pos[node.value] = (counter[0], -depth)
    counter[0] += 1
    get_positions(node.right, depth + 1, counter, pos)
    return pos

def get_edges(node, edges=None):
    if edges is None: edges = []
    if not node: return edges
    if node.left:
        edges.append((node.value, node.left.value))
        get_edges(node.left, edges)
    if node.right:
        edges.append((node.value, node.right.value))
        get_edges(node.right, edges)
    return edges

def get_all_nodes(node, nodes=None):
    if nodes is None: nodes = []
    if not node: return nodes
    nodes.append(node.value)
    get_all_nodes(node.left, nodes)
    get_all_nodes(node.right, nodes)
    return nodes

# ─── Draw Tree ────────────────────────────────────────────────────────────────
def draw_tree(root, visited=None, current=None, color="#3b82f6"):
    if visited is None: visited = []
    visited_set = set(visited)

    fig, ax = plt.subplots(figsize=(9, 3.5))
    fig.patch.set_facecolor("#0f172a")
    ax.set_facecolor("#0f172a")

    if root is None:
        ax.text(0.5, 0.5, "Tambahkan node untuk memulai",
                ha="center", va="center", color="#64748b", fontsize=12,
                transform=ax.transAxes)
        ax.axis("off")
        return fig

    pos = get_positions(root)
    edges = get_edges(root)
    nodes = get_all_nodes(root)

    # Draw edges
    for a, b in edges:
        x1, y1 = pos[a]
        x2, y2 = pos[b]
        edge_color = "#475569"
        if a in visited_set and b in visited_set:
            edge_color = color
        ax.plot([x1, x2], [y1, y2], color=edge_color, lw=2, zorder=1)

    # Draw nodes
    for v in nodes:
        x, y = pos[v]
        if v == current:
            fc, ec, tc = "#f59e0b", "#fbbf24", "#1e293b"
            lw = 3
        elif v in visited_set:
            fc, ec, tc = color, "#fff", "#ffffff"
            lw = 2
        else:
            fc, ec, tc = "#1e293b", "#475569", "#94a3b8"
            lw = 1.5

        circle = plt.Circle((x, y), 0.4, color=fc, ec=ec, lw=lw, zorder=2)
        ax.add_patch(circle)
        ax.text(x, y, str(v), ha="center", va="center",
                color=tc, fontsize=10, fontweight="bold",
                fontfamily="monospace", zorder=3)

    all_x = [pos[v][0] for v in nodes]
    all_y = [pos[v][1] for v in nodes]
    ax.set_xlim(min(all_x) - 0.8, max(all_x) + 0.8)
    ax.set_ylim(min(all_y) - 0.8, max(all_y) + 0.8)
    ax.set_aspect("equal")
    ax.axis("off")
    plt.tight_layout(pad=0.2)
    return fig

# ─── Session State ─────────────────────────────────────────────────────────────
DEFAULT = [50, 30, 70, 20, 40, 60, 80]

if "data" not in st.session_state:
    st.session_state.data = DEFAULT.copy()
if "step" not in st.session_state:
    st.session_state.step = -1
if "mode" not in st.session_state:
    st.session_state.mode = "preorder"

root = build_bst(st.session_state.data)

pre = preorder(root)
ino = inorder(root)
post = postorder(root)

MODES = {
    "preorder":  {"label": "Pre-order  (Root → Left → Right)", "color": "#3b82f6", "result": pre},
    "inorder":   {"label": "In-order   (Left → Root → Right)", "color": "#10b981", "result": ino},
    "postorder": {"label": "Post-order (Left → Right → Root)", "color": "#ef4444", "result": post},
}

# ─── Title ────────────────────────────────────────────────────────────────────
st.title("🌳 Binary Search Tree Visualizer")
st.caption("Struktur Data — Pre-order · In-order · Post-order")
st.divider()

# ─── Layout ───────────────────────────────────────────────────────────────────
col1, col2 = st.columns([1, 2], gap="large")

# ══════════════════════
# KIRI: Input & Ringkasan
# ══════════════════════
with col1:
    st.subheader("📊 Data & Input")

    # Tampilkan data saat ini
    st.write("**Node dalam BST:**")
    st.code("  →  ".join(str(v) for v in sorted(st.session_state.data)), language=None)

    # Form tambah node
    with st.form("form_tambah", clear_on_submit=True):
        new_val = st.number_input("Masukkan nilai node baru:", min_value=1, max_value=999, value=None, step=1, placeholder="Ketik angka...")
        c1, c2 = st.columns(2)
        add = c1.form_submit_button("➕ Tambah", use_container_width=True)
        reset = c2.form_submit_button("↺ Reset", use_container_width=True)

    if add:
        if new_val is None:
            st.warning("Masukkan nilai node terlebih dahulu!")
        elif int(new_val) not in st.session_state.data:
            st.session_state.data.append(int(new_val))
            st.session_state.step = -1
            st.rerun()
        else:
            st.warning(f"Node {int(new_val)} sudah ada!")

    if reset:
        st.session_state.data = DEFAULT.copy()
        st.session_state.step = -1
        st.rerun()

    st.divider()

    # Ringkasan traversal
    st.subheader("📋 Hasil Traversal")
    for key, info in MODES.items():
        st.write(f"**{info['label']}**")
        result_str = " → ".join(str(v) for v in info["result"])
        st.code(result_str, language=None)

    st.info("💡 In-order pada BST selalu menghasilkan nilai **terurut ascending**.")

# ══════════════════════
# KANAN: Visualisasi
# ══════════════════════
with col2:
    st.subheader("🌲 Visualisasi Tree")

    # Pilih mode traversal
    mode = st.radio(
        "Pilih Traversal:",
        options=list(MODES.keys()),
        format_func=lambda x: MODES[x]["label"],
        horizontal=True,
        key="mode"
    )

    # Reset step jika ganti mode
    current_result = MODES[mode]["result"]
    current_color  = MODES[mode]["color"]
    step = st.session_state.step

    # Clamp step
    if step >= len(current_result):
        st.session_state.step = len(current_result) - 1
        step = st.session_state.step

    # Hitung visited & current node
    visited = current_result[:step + 1] if step >= 0 else []
    current_node = current_result[step] if step >= 0 else None

    # Gambar tree
    fig = draw_tree(root, visited=visited, current=current_node, color=current_color)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    # Legend
    lc1, lc2, lc3 = st.columns(3)
    lc1.caption("⬜ Belum dikunjungi")
    lc2.caption("🔵 Sudah dikunjungi")
    lc3.caption("🟡 Sedang dikunjungi")

    st.divider()

    # Kontrol animasi
    st.write("**⏯ Kontrol Animasi:**")
    bc1, bc2, bc3, bc4 = st.columns(4)

    if bc1.button("⏮ Awal", use_container_width=True):
        st.session_state.step = -1
        st.rerun()

    if bc2.button("◀ Mundur", use_container_width=True):
        if st.session_state.step > -1:
            st.session_state.step -= 1
            st.rerun()

    if bc3.button("Maju ▶", use_container_width=True):
        if st.session_state.step < len(current_result) - 1:
            st.session_state.step += 1
            st.rerun()

    if bc4.button("Akhir ⏭", use_container_width=True):
        st.session_state.step = len(current_result) - 1
        st.rerun()

    # Progress bar
    if len(current_result) > 0:
        progress = (step + 1) / len(current_result) if step >= 0 else 0
        st.progress(progress, text=f"Langkah {step + 1 if step >= 0 else 0} / {len(current_result)}")

    st.divider()

    # Step-by-step log
    st.write("**📝 Log Kunjungan:**")
    if step == -1:
        st.caption("Tekan **Maju ▶** untuk memulai traversal.")
    else:
        for i, v in enumerate(current_result[:step + 1]):
            is_current = (i == step)
            icon = "👉" if is_current else "✅"
            label = f"Langkah {i+1:02d}: Kunjungi node **{v}**"

            if mode == "preorder" and i == 0:
                label += "  ← *Root (pertama)*"
            elif mode == "inorder":
                label += f"  ← *urutan ke-{i+1}*"
            elif mode == "postorder" and i == len(current_result) - 1 and is_current:
                label += "  ← *Root (terakhir!)*"

            if is_current:
                st.success(f"{icon} {label}")
            else:
                st.write(f"{icon} {label}")
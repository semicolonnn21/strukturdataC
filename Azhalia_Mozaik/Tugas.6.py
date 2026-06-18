import streamlit as st
import plotly.graph_objects as go

# STRUKTUR DATA BST
class Node:
    def __init__(self, value, x=0, y=0, level=1):
        self.value = value
        self.left = None
        self.right = None
        self.x = x
        self.y = y
        self.level = level

class BST:
    def __init__(self):
        self.root = None

    def insert(self, root, value, x=0, y=0, level=1, gap=2.0):
        if root is None:
            return Node(value, x, y, level)
        
        # Logika pembagian gap eksponensial agar visualisasi tidak bertumpuk
        if value < root.value:
            root.left = self.insert(root.left, value, x - gap/(2**level), y - 1, level + 1, gap)
        else:
            root.right = self.insert(root.right, value, x + gap/(2**level), y - 1, level + 1, gap)
        return root

    def get_traversal(self, root, type="inorder"):
        res = []
        def traverse(node):
            if node:
                if type == "preorder": res.append(str(node.value))
                traverse(node.left)
                if type == "inorder": res.append(str(node.value))
                traverse(node.right)
                if type == "postorder": res.append(str(node.value))
        traverse(root)
        return " → ".join(res)

# FUNGSI VISUALISASI
def draw_tree(root):
    if not root: return go.Figure()
    edge_x, edge_y, node_x, node_y, node_text = [], [], [], [], []

    def get_coords(node):
        if node:
            node_x.append(node.x)
            node_y.append(node.y)
            node_text.append(str(node.value))
            if node.left:
                edge_x.extend([node.x, node.left.x, None])
                edge_y.extend([node.y, node.left.y, None])
                get_coords(node.left)
            if node.right:
                edge_x.extend([node.x, node.right.x, None])
                edge_y.extend([node.y, node.right.y, None])
                get_coords(node.right)

    get_coords(root)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=edge_x, y=edge_y, mode='lines', line=dict(color='#888', width=2), hoverinfo='none'))
    fig.add_trace(go.Scatter(x=node_x, y=node_y, mode='markers+text', 
                             text=node_text, textposition="middle center",
                             textfont=dict(color="white", size=11),
                             marker=dict(size=35, color='#1f77b4', line=dict(width=2, color='white'))))
    
    fig.update_layout(showlegend=False, 
                      xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                      yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                      height=400, margin=dict(l=20, r=20, t=20, b=20),
                      paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return fig

# INTERFACE STREAMLIT
st.set_page_config(page_title="Tugas BST - Azhalia Mozaik", layout="wide")
st.title("🌳Visualisasi Binary Search Tree (BST)🌳")

# DATA 
data_awal = [50, 30, 70, 20, 40, 60, 80]
node_baru = [10, 90, 65]

tree = BST()

# TAHAP 1 DATA AWAL
for val in data_awal:
    tree.root = tree.insert(tree.root, val)

st.header("1. Struktur Pohon Awal")
col_info, col_graph = st.columns([1, 2])
with col_info:
    st.write("**Dataset Awal:**", data_awal)
    st.info(f"**Inorder:** {tree.get_traversal(tree.root, 'inorder')}")
with col_graph:
    st.plotly_chart(draw_tree(tree.root), width='stretch')

# TAHAP 2 PENAMBAHAN DATA
st.divider()
st.header("2. Penambahan Node Baru (10, 90, 65)")
for val in node_baru:
    tree.root = tree.insert(tree.root, val)

st.plotly_chart(draw_tree(tree.root), width='stretch')

# TAHAP 3 TRAVERSAL AKHIR
st.divider()
st.subheader("📊 Hasil Traversal Akhir")

st.markdown("**Preorder**")
st.code(tree.get_traversal(tree.root, 'preorder'))

st.markdown("**Inorder**")
st.code(tree.get_traversal(tree.root, 'inorder'))

st.markdown("**Postorder**")
st.code(tree.get_traversal(tree.root, 'postorder'))

# TAHAP 4 ANALISIS (Sesuai Gambar)
st.divider()
st.header("Analisis Tugas")

st.write(r"""
- **Node Baru:** 10 (kiri dari 20), 65 (kanan dari 60), 90 (kanan dari 80).
- **Height of Tree:** Jalur terpanjang adalah 3 edge.
- **Internal Nodes:** 50, 30, 70, 20, 60, 80.
""")
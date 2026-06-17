import streamlit as st

st.set_page_config(page_title="BST Visualizer", layout="wide")

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

    def display_tree(self, root, level=0, prefix="Root:"):
        if root is not None:
            st.text("  " * (level * 4) + f"{prefix} {root.value}")
            if root.left or root.right:
                if root.left:
                    self.display_tree(root.left, level + 1, "L──")
                else:
                    st.text("  " * ((level + 1) * 4) + "L── None")
                if root.right:
                    self.display_tree(root.right, level + 1, "R──")
                else:
                    st.text("  " * ((level + 1) * 4) + "R── None")

st.title("🌳 Binary Search Tree Visualizer")
st.write("Hafidzar Ashyawal Sinatryas - 2530801075")

if 'tree' not in st.session_state:
    st.session_state.tree = BST()
    data_awal = [50, 30, 70, 20, 40, 60, 80]
    for item in data_awal:
        st.session_state.tree.root = st.session_state.tree.insert(st.session_state.tree.root, item)

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Kontrol Tree")
    new_val = st.number_input("Tambah Node Baru:", step=1, value=65)
    if st.button("Tambah ke Tree"):
        st.session_state.tree.root = st.session_state.tree.insert(st.session_state.tree.root, new_val)
        st.success(f"Node {new_val} berhasil ditambahkan!")

    st.subheader("Hasil Traversal")
    t_root = st.session_state.tree.root
    
    st.info(f"**Preorder:** {' ➔ '.join(st.session_state.tree.get_preorder(t_root, []))}")
    st.success(f"**Inorder:** {' ➔ '.join(st.session_state.tree.get_inorder(t_root, []))}")
    st.warning(f"**Postorder:** {' ➔ '.join(st.session_state.tree.get_postorder(t_root, []))}")

with col2:
    st.subheader("Visualisasi Struktur")
    with st.expander("Lihat Hierarki Tree", expanded=True):
        st.session_state.tree.display_tree(st.session_state.tree.root)

st.divider()
st.caption("Struktur Data - Informatika")
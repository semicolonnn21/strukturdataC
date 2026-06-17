import streamlit as st

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

    #fungsi untuk mengambil urutan angka dalam bentuk list
    def traversal_list(self, root, mode, res):
        if root:
            if mode == 'pre': res.append(root.value)
            self.traversal_list(root.left, mode, res)
            if mode == 'in': res.append(root.value)
            self.traversal_list(root.right, mode, res)
            if mode == 'post': res.append(root.value)
        return res

# UI
st.set_page_config(page_title="Project Binary Search Tree 🌲", layout="wide")
st.title("Binary Search Tree 🌲")
st.caption("***Untuk memenuhi Tugas Mata kuliah: Struktur Data😁***")

st.divider()

col_nama, col_nim, col_mk, col_class = st.columns(4)
with col_nama:
    st.write("**Nama:** Abil Ghinaya Azka")
with col_nim:
    st.write("**NIM:** 2530801056")
with col_mk:
    st.write("**Mata kuliah:** Struktur Data")
with col_class:
    st.write("**Kelas:** II C")

st.divider()

#inisialisasi Pohon
tree = BST()
data_awal = [50, 30, 70, 20, 40, 60, 80]
for item in data_awal:
    tree.root = tree.insert(tree.root, item)

st.header("Traversal Awal")
col1, col2, col3 = st.columns(3)
with col1:
    st.write("**Preorder**")
    st.code(tree.traversal_list(tree.root, 'pre', []))
with col2:
    st.write("**Inorder**")
    st.code(tree.traversal_list(tree.root, 'in', []))
with col3:
    st.write("**Postorder**")
    st.code(tree.traversal_list(tree.root, 'post', []))

#tambah Node Baru
node_baru = [10, 90, 65]
for n in node_baru:
    tree.root = tree.insert(tree.root, n)

st.divider() 

# menampilkan hasil
st.header("Traversal Akhir")
tab1, tab2, tab3 = st.tabs(["Preorder", "Inorder", "Postorder"])
tab1.success(f"Hasil: {tree.traversal_list(tree.root, 'pre', [])}")
tab2.info(f"Hasil: {tree.traversal_list(tree.root, 'in', [])}")
tab3.warning(f"Hasil: {tree.traversal_list(tree.root, 'post', [])}")

st.divider()

st.header("Analisis Perubahan")
st.write("""
Setelah penambahan node:
* **Angka 10**: Menjadi anak kiri dari 20 (karena 10 < 20).
* **Angka 90**: Menjadi anak kanan dari 80 (karena 90 > 80).
* **Angka 65**: Menjadi anak kanan dari 60 (karena 65 > 60).
* **Kesimpulan:** Struktur Inorder tetap terurut secara numerik, yang membuktikan logika BST berjalan benar.
""")

st.header("Visualisasi Struktur Tree")
st.code("""
              50
           /      \\
         30        70
        /  \\      /  \\
      20    40   60   80
     /            \\     \\
   10              65    90
""", language="text")
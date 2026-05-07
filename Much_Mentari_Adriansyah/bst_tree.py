import streamlit as st

st.set_page_config(
    page_title="Belajar BST",
    layout="wide"
)

# Class Node
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

# Class BST
class BST:
    def __init__(self):
        self.root = None
    def insert(self, root, value):
        # Jika tree kosong
        if root is None:
            return Node(value)
        # Masuk ke kiri
        if value < root.value:
            root.left = self.insert(root.left, value)
        # Masuk ke kanan
        else:
            root.right = self.insert(root.right, value)
        return root

    # Fungsi tambahan
    def tambah(self, nilai):
        self.root = self.insert(self.root, nilai)

    # Traversal preorder
    def preorder(self, root, hasil=None):
        if hasil is None:
            hasil = []
        if root:
            hasil.append(root.value)
            self.preorder(root.left, hasil)
            self.preorder(root.right, hasil)
        return hasil

    # Traversal inorder
    def inorder(self, root, hasil=None):
        if hasil is None:
            hasil = []
        if root:
            self.inorder(root.left, hasil)
            hasil.append(root.value)
            self.inorder(root.right, hasil)
        return hasil

    # Traversal postorder
    def postorder(self, root, hasil=None):
        if hasil is None:
            hasil = []
        if root:
            self.postorder(root.left, hasil)
            self.postorder(root.right, hasil)
            hasil.append(root.value)
        return hasil


# Visualisasi BST
def tampilkan_node(nilai, jenis="lama"):
    if jenis == "akar":
        st.success(f"⭐ ROOT : {nilai}")
    elif jenis == "baru":
        st.warning(f"🟠 NODE BARU : {nilai}")
    else:
        st.info(f"🔵 NODE : {nilai}")
def tampilkan_tree_awal():
    st.subheader("Visualisasi BST Awal")

    # Level 1
    kolom1, kolom2, kolom3 = st.columns([1,1,1])
    with kolom2:
        tampilkan_node(50, "akar")

    # Level 2
    kolom1, kolom2, kolom3, kolom4, kolom5 = st.columns(5)
    with kolom2:
        tampilkan_node(30)
    with kolom4:
        tampilkan_node(70)

    # Level 3
    kolom1, kolom2, kolom3, kolom4, kolom5, kolom6, kolom7 = st.columns(7)
    with kolom1:
        tampilkan_node(20)
    with kolom3:
        tampilkan_node(40)
    with kolom5:
        tampilkan_node(60)
    with kolom7:
        tampilkan_node(80)

def tampilkan_tree_final():
    st.subheader("Visualisasi BST Setelah Penambahan Node")
    # Level 1
    kolom1, kolom2, kolom3 = st.columns([1,1,1])
    with kolom2:
        tampilkan_node(50, "akar")
    # Level 2
    kolom1, kolom2, kolom3, kolom4, kolom5 = st.columns(5)
    with kolom2:
        tampilkan_node(30)
    with kolom4:
        tampilkan_node(70)
    # Level 3
    kolom1, kolom2, kolom3, kolom4, kolom5, kolom6, kolom7 = st.columns(7)
    with kolom1:
        tampilkan_node(20)
    with kolom3:
        tampilkan_node(40)
    with kolom5:
        tampilkan_node(60)
    with kolom7:
        tampilkan_node(80)
    # Level 4
    kolom1, kolom2, kolom3, kolom4, kolom5, kolom6, kolom7, kolom8, kolom9 = st.columns(9)
    with kolom1:
        tampilkan_node(10, "baru")
    with kolom6:
        tampilkan_node(65, "baru")
    with kolom9:
        tampilkan_node(90, "baru")

# Judul

st.title("🌳 Binary Search Tree (BST)")
st.write("Belajar BST dari awal hingga akhir menggunakan Streamlit")

st.divider()

# Data Awal

data_awal = [50, 30, 70, 20, 40, 60, 80]
st.header("1️⃣ Data Awal BST")
st.write("Data yang dimasukkan ke dalam BST:")
st.code(data_awal)

# Membuat BST
tree = BST()

# Memasukkan data
for item in data_awal:
    tree.tambah(item)
st.divider()

# Visualisasi Awal

st.header("2️⃣ Bentuk BST Awal")

st.write("""
Aturan BST:
- Angka lebih kecil → masuk ke kiri
- Angka lebih besar → masuk ke kanan
""")

tampilkan_tree_awal()

st.divider()

# Traversal Awal

st.header("3️⃣ Hasil Traversal BST Awal")

hasil_preorder = tree.preorder(tree.root)
hasil_inorder = tree.inorder(tree.root)
hasil_postorder = tree.postorder(tree.root)

tab1, tab2, tab3 = st.tabs([
    "Preorder",
    "Inorder",
    "Postorder"
])

with tab1:
    st.subheader("Preorder")
    st.write("Urutan: Root → Kiri → Kanan")
    st.code(hasil_preorder)
with tab2:
    st.subheader("Inorder")
    st.write("Urutan: Kiri → Root → Kanan")
    st.code(hasil_inorder)
    st.success("Traversal inorder pada BST selalu menghasilkan data terurut.")
with tab3:
    st.subheader("Postorder")
    st.write("Urutan: Kiri → Kanan → Root")
    st.code(hasil_postorder)
st.divider()

# Tambah Node Baru
st.header("4️⃣ Menambahkan Node Baru")
data_baru = [10, 90, 65]
st.write("Node baru yang akan ditambahkan:")

kolom1, kolom2, kolom3 = st.columns(3)
with kolom1:
    st.metric("Node Baru", "10")
with kolom2:
    st.metric("Node Baru", "90")
with kolom3:
    st.metric("Node Baru", "65")
# Menambahkan node baru
for item in data_baru:
    tree.tambah(item)
st.divider()

# Tree Final
st.header("5️⃣ BST Setelah Penambahan Node")
tampilkan_tree_final()

st.info("""
Keterangan:
- ⭐ = Root
- 🔵 = Node Lama
- 🟠 = Node Baru
""")

st.divider()

# Traversal Baru
st.header("6️⃣ Traversal Setelah Penambahan")
preorder_baru = tree.preorder(tree.root)
inorder_baru = tree.inorder(tree.root)
postorder_baru = tree.postorder(tree.root)

tab1, tab2, tab3 = st.tabs([
    "Preorder Baru",
    "Inorder Baru",
    "Postorder Baru"
])

with tab1:
    st.code(preorder_baru)
    st.write("""
    Analisis:
    - Node 10 berada di kiri node 20
    - Node 65 berada di kanan node 60
    - Node 90 berada di kanan node 80
    """)

with tab2:
    st.code(inorder_baru)
    st.success("""
    Data tetap terurut dari kecil ke besar.
    Ini adalah ciri khas traversal inorder pada BST.
    """)
with tab3:
    st.code(postorder_baru)
    st.write("""
    Pada postorder, anak dikunjungi terlebih dahulu,
    kemudian induknya.
    """)
st.divider()

# Ringkasan
st.header("7️⃣ Ringkasan Posisi Node")
st.table({
    "Node": [10,20,30,40,50,60,65,70,80,90],
    "Posisi": [
        "Kiri dari 20",
        "Kiri dari 30",
        "Kanan dari 30",
        "ROOT",
        "Kiri dari 70",
        "Kanan dari 60",
        "Kanan dari 50",
        "Kanan dari 70",
        "Kanan dari 80"
    ]
})

st.success("🎉 BST berhasil dibuat dan divisualisasikan!")
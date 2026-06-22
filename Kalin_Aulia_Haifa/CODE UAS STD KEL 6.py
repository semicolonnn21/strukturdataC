import streamlit as st
import time
import random

st.set_page_config(
    page_title="Benchmarking Struktur Data",
    page_icon="📊",
    layout="wide"
)


# ──────────────────────────────────────────────
#  HEADER UTAMA
# ──────────────────────────────────────────────
st.markdown("""
<h1 style='color: #4A90D9; margin-bottom: 0px;'>📊 Benchmarking Struktur Data</h1>
<p style='color: #8b9bb4; font-size: 15px;'>Perbandingan performa Array, BST, Hash Table, dan AVL Tree</p>
""", unsafe_allow_html=True)
st.divider()

# ──────────────────────────────────────────────
#  FUNGSI STRUKTUR DATA
# ──────────────────────────────────────────────
def generate_dataset(ukuran, jenis):
    if jenis == "Acak":
        return random.sample(range(ukuran * 10), ukuran)
    elif jenis == "Terurut (Ascending)":
        return list(range(ukuran))
    else:
        return list(range(ukuran - 1, -1, -1))

def array_insert(data):
    arr = []
    s = time.perf_counter()
    for v in data: arr.append(v)
    return arr, (time.perf_counter() - s) * 1000

def array_search(arr, data):
    targets = random.choices(data, k=min(100, len(data)))
    s = time.perf_counter()
    for v in targets: _ = v in arr
    return (time.perf_counter() - s) * 1000

def array_delete(arr, data):
    targets = random.choices(data, k=min(50, len(data)))
    s = time.perf_counter()
    for v in targets:
        if v in arr: arr.remove(v)
    return (time.perf_counter() - s) * 1000

def hash_insert(data):
    tabel = {}
    s = time.perf_counter()
    for v in data: tabel[v] = True
    return tabel, (time.perf_counter() - s) * 1000

def hash_search(tabel, data):
    targets = random.choices(data, k=min(100, len(data)))
    s = time.perf_counter()
    for v in targets: _ = v in tabel
    return (time.perf_counter() - s) * 1000

def hash_delete(tabel, data):
    targets = random.choices(data, k=min(50, len(data)))
    s = time.perf_counter()
    for v in targets: tabel.pop(v, None)
    return (time.perf_counter() - s) * 1000

def bst_insert_node(pohon, nilai):
    node_baru = [nilai, None, None]
    if not pohon:
        pohon.append(node_baru)
        return pohon
    idx = 0
    while True:
        if nilai < pohon[idx][0]:
            if pohon[idx][1] is None:
                pohon[idx][1] = len(pohon)
                pohon.append(node_baru)
                break
            else: idx = pohon[idx][1]
        elif nilai > pohon[idx][0]:
            if pohon[idx][2] is None:
                pohon[idx][2] = len(pohon)
                pohon.append(node_baru)
                break
            else: idx = pohon[idx][2]
        else: break
    return pohon

def bst_insert(data):
    pohon = []
    s = time.perf_counter()
    for v in data: pohon = bst_insert_node(pohon, v)
    return pohon, (time.perf_counter() - s) * 1000

def bst_search(pohon, data):
    if not pohon:
        return 0.0
    targets = random.choices(data, k=min(100, len(data)))
    s = time.perf_counter()
    for v in targets:
        idx = 0
        while idx is not None:
            if v == pohon[idx][0]: break
            idx = pohon[idx][1] if v < pohon[idx][0] else pohon[idx][2]
    return (time.perf_counter() - s) * 1000

def bst_delete_node(pohon, root_idx, nilai):
    """
    Hapus 'nilai' dari BST (representasi list: node = [value, left_idx, right_idx]).
    Mengembalikan index root baru (bisa berubah jika root yang dihapus).
    Menangani 3 kasus: tanpa anak, satu anak, dua anak (pakai inorder successor).
    """
    parent_idx, idx = None, root_idx
    # 1) Cari node yang mau dihapus + simpan parent-nya
    while idx is not None and pohon[idx][0] != nilai:
        parent_idx = idx
        idx = pohon[idx][1] if nilai < pohon[idx][0] else pohon[idx][2]

    if idx is None:
        return root_idx  # nilai tidak ditemukan

    left, right = pohon[idx][1], pohon[idx][2]

    def set_child(p_idx, old_idx, new_idx):
        """Sambungkan parent ke child baru (atau ke root jika p_idx None)."""
        if p_idx is None:
            return new_idx
        if pohon[p_idx][1] == old_idx:
            pohon[p_idx][1] = new_idx
        else:
            pohon[p_idx][2] = new_idx
        return root_idx

    # Kasus 1: tidak punya anak
    if left is None and right is None:
        return set_child(parent_idx, idx, None)

    # Kasus 2: hanya satu anak -> anak tersebut naik menggantikan posisi idx
    if left is None or right is None:
        child = right if left is None else left
        return set_child(parent_idx, idx, child)

    # Kasus 3: dua anak -> cari successor (nilai terkecil di subtree kanan)
    succ_parent, succ_idx = idx, right
    while pohon[succ_idx][1] is not None:
        succ_parent = succ_idx
        succ_idx = pohon[succ_idx][1]

    # Salin nilai successor ke node yang dihapus
    pohon[idx][0] = pohon[succ_idx][0]

    # Lepaskan node successor asli dari posisinya (successor punya child kiri None)
    if succ_parent == idx:
        pohon[idx][2] = pohon[succ_idx][2]
    else:
        pohon[succ_parent][1] = pohon[succ_idx][2]

    return root_idx


def bst_delete(pohon, data, root_idx=0):
    if not pohon:
        return 0
    targets = random.choices(data, k=min(50, len(data)))
    s = time.perf_counter()
    for v in targets:
        if root_idx is None:
            break
        root_idx = bst_delete_node(pohon, root_idx, v)
    return (time.perf_counter() - s) * 1000

# ── AVL Tree asli: pohon biner seimbang dengan rotasi otomatis ──
# Representasi node sebagai object kecil (bukan list/index) agar rotasi mudah ditulis.
class AVLNode:
    __slots__ = ("value", "left", "right", "height")
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1  # tinggi node daun = 1

def _height(node):
    return node.height if node else 0

def _balance_factor(node):
    return _height(node.left) - _height(node.right) if node else 0

def _update_height(node):
    node.height = 1 + max(_height(node.left), _height(node.right))

def _rotate_right(y):
    x = y.left
    y.left = x.right
    x.right = y
    _update_height(y)
    _update_height(x)
    return x  # x jadi root baru subtree ini

def _rotate_left(x):
    y = x.right
    x.right = y.left
    y.left = x
    _update_height(x)
    _update_height(y)
    return y  # y jadi root baru subtree ini

def avl_insert_node(node, value):
    if node is None:
        return AVLNode(value)
    if value < node.value:
        node.left = avl_insert_node(node.left, value)
    elif value > node.value:
        node.right = avl_insert_node(node.right, value)
    else:
        return node  # duplikat, tidak disisipkan

    _update_height(node)
    balance = _balance_factor(node)

    # Left Left
    if balance > 1 and value < node.left.value:
        return _rotate_right(node)
    # Right Right
    if balance < -1 and value > node.right.value:
        return _rotate_left(node)
    # Left Right
    if balance > 1 and value > node.left.value:
        node.left = _rotate_left(node.left)
        return _rotate_right(node)
    # Right Left
    if balance < -1 and value < node.right.value:
        node.right = _rotate_right(node.right)
        return _rotate_left(node)

    return node

def avl_search_node(node, value):
    while node is not None:
        if value == node.value: return True
        node = node.left if value < node.value else node.right
    return False

def _avl_min_value_node(node):
    while node.left is not None:
        node = node.left
    return node

def avl_delete_node(node, value):
    if node is None:
        return node
    if value < node.value:
        node.left = avl_delete_node(node.left, value)
    elif value > node.value:
        node.right = avl_delete_node(node.right, value)
    else:
        # node ditemukan -> hapus dengan 3 kasus standar
        if node.left is None:
            return node.right
        elif node.right is None:
            return node.left
        else:
            successor = _avl_min_value_node(node.right)
            node.value = successor.value
            node.right = avl_delete_node(node.right, successor.value)

    _update_height(node)
    balance = _balance_factor(node)

    # Rebalance setelah delete (4 kasus rotasi seperti insert)
    if balance > 1 and _balance_factor(node.left) >= 0:
        return _rotate_right(node)
    if balance > 1 and _balance_factor(node.left) < 0:
        node.left = _rotate_left(node.left)
        return _rotate_right(node)
    if balance < -1 and _balance_factor(node.right) <= 0:
        return _rotate_left(node)
    if balance < -1 and _balance_factor(node.right) > 0:
        node.right = _rotate_right(node.right)
        return _rotate_left(node)

    return node

def avl_insert(data):
    root = None
    s = time.perf_counter()
    for v in data:
        root = avl_insert_node(root, v)
    return root, (time.perf_counter() - s) * 1000

def avl_search(root, data):
    targets = random.choices(data, k=min(100, len(data)))
    s = time.perf_counter()
    for v in targets:
        _ = avl_search_node(root, v)
    return (time.perf_counter() - s) * 1000

def avl_delete(root, data):
    targets = random.choices(data, k=min(50, len(data)))
    s = time.perf_counter()
    for v in targets:
        root = avl_delete_node(root, v)
    return (time.perf_counter() - s) * 1000


# ──────────────────────────────────────────────
#  PROSES BENCHMARK
# ──────────────────────────────────────────────
def jalankan_benchmark(data, pilihan_ds, pilihan_ops):
    hasil = []
    for ds in pilihan_ds:
        row = {"Struktur Data": ds}
        if ds == "Array/List":
            struktur, t_ins = array_insert(data)
            t_srch = array_search(struktur, data) if "Search" in pilihan_ops else 0
            t_del = array_delete(struktur, data) if "Delete" in pilihan_ops else 0
        elif ds == "Hash Table":
            struktur, t_ins = hash_insert(data)
            t_srch = hash_search(struktur, data) if "Search" in pilihan_ops else 0
            t_del = hash_delete(struktur, data) if "Delete" in pilihan_ops else 0
        elif ds == "BST":
            struktur, t_ins = bst_insert(data)
            t_srch = bst_search(struktur, data) if "Search" in pilihan_ops else 0
            t_del = bst_delete(struktur, data) if "Delete" in pilihan_ops else 0
        elif ds == "AVL Tree":
            struktur, t_ins = avl_insert(data)
            t_srch = avl_search(struktur, data) if "Search" in pilihan_ops else 0
            t_del = avl_delete(struktur, data) if "Delete" in pilihan_ops else 0

        if "Insert" in pilihan_ops: row["Insert (ms)"] = round(t_ins, 4)
        if "Search" in pilihan_ops: row["Search (ms)"] = round(t_srch, 4)
        if "Delete" in pilihan_ops: row["Delete (ms)"] = round(t_del, 4)
        row["Total (ms)"] = round(t_ins + t_srch + t_del, 4)
        hasil.append(row)
    return hasil


# ──────────────────────────────────────────────
#  SIDEBAR CONFIGURATION
# ──────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Konfigurasi")
    pilihan_ds = st.multiselect(
        "Struktur Data",
        ["Array/List", "BST", "Hash Table", "AVL Tree"],
        default=["Array/List", "BST", "Hash Table", "AVL Tree"]
    )

    ukuran_map = {"Kecil – 100 data": 100, "Sedang – 1.000 data": 1000, "Besar – 10.000 data": 10000}
    ukuran_label = st.selectbox("Ukuran Dataset", list(ukuran_map.keys()))
    jenis_data = st.selectbox("Jenis Dataset", ["Acak", "Terurut (Ascending)", "Descending"])

    pilihan_ops = st.multiselect(
        "Operasi yang Diuji",
        ["Insert", "Search", "Delete"],
        default=["Insert", "Search", "Delete"]
    )
    st.markdown("<br>", unsafe_allow_html=True)
    tombol = st.button("▶ Jalankan Benchmark", use_container_width=True)


# ──────────────────────────────────────────────
#  MAIN WINDOW RENDER
# ──────────────────────────────────────────────
st.subheader("📋 Kompleksitas Algoritma (Teoritis)")
kompleks = [
    {"Struktur Data": "Array/List", "Insert": "O(1)*", "Search": "O(n)", "Delete": "O(n)", "Space": "O(n)"},
    {"Struktur Data": "BST",        "Insert": "O(log n)", "Search": "O(log n)", "Delete": "O(log n)", "Space": "O(n)"},
    {"Struktur Data": "Hash Table", "Insert": "O(1)*",    "Search": "O(1)*",    "Delete": "O(1)*",    "Space": "O(n)"},
    {"Struktur Data": "AVL Tree",   "Insert": "O(log n)", "Search": "O(log n)", "Delete": "O(log n)", "Space": "O(n)"},
]
st.table(kompleks)
st.caption("*) rata-rata (average case)")
st.divider()

if not tombol:
    st.info("👈 Atur konfigurasi di sidebar, lalu klik **▶ Jalankan Benchmark**.")
    st.stop()

# ── Jalankan Pengujian ──
data = generate_dataset(ukuran_map[ukuran_label], jenis_data)
hasil = jalankan_benchmark(data, pilihan_ds, pilihan_ops)

st.subheader("📄 Hasil Waktu Eksekusi (Real-time)")
st.table(hasil)

# ── Visualisasi dengan st.bar_chart (tanpa Plotly) ──
st.subheader("📈 Visualisasi Total Waktu (ms)")
chart_data = {r["Struktur Data"]: r["Total (ms)"] for r in hasil}
st.bar_chart(chart_data)

# ── Analisis ──
st.subheader("🔍 Analisis Hasil")
analisis = {
    "Array/List":  "Array menyimpan data secara berurutan. Insert cepat (O(1)), tapi search harus sekuensial (O(n)).",
    "BST":         "Search rata-rata O(log n), namun jika dataset terurut (worst case), pohon miring dan performa anjlok ke O(n).",
    "Hash Table":  "Menggunakan fungsi hash untuk pemetaan langsung. Performa rata-rata luar biasa stabil di O(1).",
    "AVL Tree":    "Varian BST seimbang yang menjamin search selalu O(log n) dengan melakukan rotasi balancing otomatis."
}

for nama in pilihan_ds:
    with st.expander(f"📌 Karakteristik {nama}"):
        st.write(analisis[nama])
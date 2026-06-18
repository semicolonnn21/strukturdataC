import streamlit as st
import random
import time
import pandas as pd
import altair as alt
import sys
from typing import Optional, Dict, List

# Naikkan recursion limit agar aman untuk dataset besar
sys.setrecursionlimit(15000)

# Binary Search Tree (BST)
class BSTNode:
    def __init__(self, key):
        self.key = key
        self.left: Optional['BSTNode'] = None
        self.right: Optional['BSTNode'] = None

class BST:
    def __init__(self):
        self.root: Optional[BSTNode] = None

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, node: Optional[BSTNode], key) -> BSTNode:
        # Jika node kosong, buat node baru
        if node is None:
            return BSTNode(key)
        # Masuk ke kiri jika lebih kecil
        if key < node.key:
            node.left = self._insert(node.left, key)
        # Masuk ke kanan jika lebih besar
        elif key > node.key:
            node.right = self._insert(node.right, key)
        else:
            # Tangani duplikat: jangan masukkan lagi
            return node
        return node

    def search(self, key) -> bool:
        return self._search(self.root, key)

    def _search(self, node: Optional[BSTNode], key) -> bool:
        if node is None:
            return False
        if key == node.key:
            return True
        if key < node.key:
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, node: Optional[BSTNode], key) -> Optional[BSTNode]:
        if node is None:
            return None
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            # Node ditemukan
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            # Dua anak: cari inorder successor
            succ = node.right
            while succ.left:
                succ = succ.left
            node.key = succ.key
            node.right = self._delete(node.right, succ.key)
        return node

# AVL Tree (self-balancing)
class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left: Optional['AVLNode'] = None
        self.right: Optional['AVLNode'] = None
        self.height = 1

class AVL:
    def __init__(self):
        self.root: Optional[AVLNode] = None

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _height(self, node: Optional[AVLNode]) -> int:
        return node.height if node else 0

    def _update_height(self, node: AVLNode):
        node.height = 1 + max(self._height(node.left), self._height(node.right))

    def _balance_factor(self, node: AVLNode) -> int:
        return self._height(node.left) - self._height(node.right)

    def _rotate_right(self, y: AVLNode) -> AVLNode:
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        self._update_height(y)
        self._update_height(x)
        return x

    def _rotate_left(self, x: AVLNode) -> AVLNode:
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        self._update_height(x)
        self._update_height(y)
        return y

    def _insert(self, node: Optional[AVLNode], key) -> AVLNode:
        if not node:
            return AVLNode(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        else:
            # Tangani duplikat
            return node

        self._update_height(node)
        balance = self._balance_factor(node)

        # Left Left
        if balance > 1 and key < node.left.key:
            return self._rotate_right(node)
        # Right Right
        if balance < -1 and key > node.right.key:
            return self._rotate_left(node)
        # Left Right
        if balance > 1 and key > node.left.key:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        # Right Left
        if balance < -1 and key < node.right.key:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def search(self, key) -> bool:
        node = self.root
        while node:
            if key == node.key:
                return True
            node = node.left if key < node.key else node.right
        return False

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _min_value_node(self, node: AVLNode) -> AVLNode:
        current = node
        while current.left:
            current = current.left
        return current

    def _delete(self, node: Optional[AVLNode], key) -> Optional[AVLNode]:
        if not node:
            return node
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            temp = self._min_value_node(node.right)
            node.key = temp.key
            node.right = self._delete(node.right, temp.key)

        self._update_height(node)
        balance = self._balance_factor(node)

        if balance > 1 and self._balance_factor(node.left) >= 0:
            return self._rotate_right(node)
        if balance > 1 and self._balance_factor(node.left) < 0:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        if balance < -1 and self._balance_factor(node.right) <= 0:
            return self._rotate_left(node)
        if balance < -1 and self._balance_factor(node.right) > 0:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        return node

# Hash Table (wrapper dict)
class HashTable:
    def __init__(self):
        self.table: Dict[int, bool] = {}

    def insert(self, key):
        self.table[key] = True

    def search(self, key) -> bool:
        return key in self.table

    def delete(self, key):
        if key in self.table:
            del self.table[key]

# Dataset generator (unik)
def generate_dataset(size: int, kind: str) -> List[int]:
    if size <= 0:
        return []
    if kind == 'random':
        # range lebih besar untuk mengurangi kemungkinan duplikat saat sampling
        return random.sample(range(size * 10 + 100), size)
    elif kind == 'sorted':
        return list(range(size))
    elif kind == 'descending':
        return list(range(size, 0, -1))
    else:
        return random.sample(range(size * 10 + 100), size)

# Waktu operasi per struktur
def time_operation(struct_name: str, operation: str, keys: List[int], test_keys: List[int]) -> float:
    start = time.perf_counter()

    if operation == 'insert':
        # Mulai dari struktur kosong
        if struct_name == 'list':
            ds = []
            for k in test_keys:
                ds.append(k)
        elif struct_name == 'hashtable':
            ds = HashTable()
            for k in test_keys:
                ds.insert(k)
        elif struct_name == 'bst':
            ds = BST()
            for k in test_keys:
                ds.insert(k)
        elif struct_name == 'avl':
            ds = AVL()
            for k in test_keys:
                ds.insert(k)
    else:
        # Build dari keys terlebih dahulu
        if struct_name == 'list':
            ds = list(keys)
            if operation == 'search':
                for k in test_keys:
                    _ = (k in ds)
            elif operation == 'delete':
                for k in test_keys:
                    try:
                        ds.remove(k)
                    except ValueError:
                        pass
        elif struct_name == 'hashtable':
            ds = HashTable()
            for k in keys:
                ds.insert(k)
            if operation == 'search':
                for k in test_keys:
                    _ = ds.search(k)
            elif operation == 'delete':
                for k in test_keys:
                    ds.delete(k)
        elif struct_name == 'bst':
            ds = BST()
            for k in keys:
                ds.insert(k)
            if operation == 'search':
                for k in test_keys:
                    _ = ds.search(k)
            elif operation == 'delete':
                for k in test_keys:
                    ds.delete(k)
        elif struct_name == 'avl':
            ds = AVL()
            for k in keys:
                ds.insert(k)
            if operation == 'search':
                for k in test_keys:
                    _ = ds.search(k)
            elif operation == 'delete':
                for k in test_keys:
                    ds.delete(k)

    end = time.perf_counter()
    return end - start

# Benchmark sekali untuk kombinasi size/kind/operation
def benchmark_once(size: int, kind: str, operation: str, struct_names: List[str], repeat: int = 3) -> pd.DataFrame:
    """
    Mengembalikan DataFrame dengan kolom:
    structure, size, kind, operation, time
    """
    results = []
    # base dataset (unik)
    base = generate_dataset(size, kind)

    for struct in struct_names:
        times = []
        for r in range(repeat):
            if operation == 'insert':
                # test_keys untuk insert: dataset baru unik
                test_keys = generate_dataset(size, 'random')
                t = time_operation(struct, 'insert', [], test_keys)
            else:
                # test_keys untuk search/delete: gabungan present dan absent
                # pilih subset present (maks 10% atau minimal 1)
                present_count = max(1, size // 10)
                present_count = min(present_count, len(base))
                present = random.sample(base, present_count) if present_count > 0 else []
                # buat absent yang tidak ada di base
                absent_size = max(1, present_count // 2)
                # buat pool besar dan ambil yang tidak ada di base
                pool = set(range(size * 20 + 200)) - set(base)
                absent = random.sample(list(pool), absent_size) if absent_size > 0 else []
                test_keys = present + absent
                t = time_operation(struct, operation, base, test_keys)
            times.append(t)
        avg_time = sum(times) / len(times)
        results.append({
            'structure': struct,
            'size': size,
            'kind': kind,
            'operation': operation,
            'time': avg_time
        })
    return pd.DataFrame(results)

# Streamlit UI
st.set_page_config(page_title="Benchmark Struktur Data", layout="wide")
st.title("Benchmarking Struktur Data: Search / Insert / Delete")
st.markdown("Bandingkan performa struktur data: **list**, **BST**, **HashTable**, **AVL**.")

st.sidebar.header("Pengaturan Benchmark")
sizes = st.sidebar.multiselect("Pilih ukuran dataset", options=[100, 1000, 10000], default=[100, 1000, 10000])
kinds = st.sidebar.multiselect("Jenis dataset", options=['random', 'sorted', 'descending'], default=['random', 'sorted', 'descending'])
operations = st.sidebar.multiselect("Operasi yang diuji", options=['search', 'insert', 'delete'], default=['search', 'insert', 'delete'])
structures = st.sidebar.multiselect("Struktur data", options=['list', 'bst', 'hashtable', 'avl'], default=['list', 'bst', 'hashtable', 'avl'])
repeat = st.sidebar.slider("Repeat per pengukuran", min_value=1, max_value=10, value=5)

st.sidebar.markdown("---")
st.sidebar.markdown("Tips: Untuk BST akan memakan waktu cukup lama jadi saya sarankan lakukan terakhir.")

if st.sidebar.button("Jalankan Benchmark"):
    if not sizes or not kinds or not operations or not structures:
        st.warning("Pilih minimal satu ukuran, satu jenis dataset, satu operasi, dan satu struktur.")
    else:
        all_results = []
        total_tasks = len(sizes) * len(kinds) * len(operations)
        progress = st.progress(0)
        task_count = 0

        for size in sizes:
            for kind in kinds:
                for op in operations:
                    df = benchmark_once(size=size, kind=kind, operation=op, struct_names=structures, repeat=repeat)
                    all_results.append(df)
                    task_count += 1
                    progress.progress(task_count / total_tasks)

        if all_results:
            results_df = pd.concat(all_results, ignore_index=True)
            st.success("Benchmark selesai")
            st.dataframe(results_df)

            # Visualisasi per operasi
            st.header("Visualisasi Hasil")
            for op in operations:
                st.subheader(f"Operasi: {op}")
                chart_df = results_df[results_df['operation'] == op]
                if chart_df.empty:
                    st.info(f"Tidak ada data untuk operasi {op}.")
                    continue
                chart = alt.Chart(chart_df).mark_bar().encode(
                    x=alt.X('size:O', title='Ukuran dataset'),
                    y=alt.Y('time:Q', title='Waktu (detik)'),
                    color='structure:N',
                    column='kind:N',
                    tooltip=['structure', 'size', 'kind', 'time']
                ).properties(width=220)
                st.altair_chart(chart, use_container_width=True)

            # Analisis ringkas: struktur tercepat per kombinasi
            st.header("Analisis Ringkas")
            try:
                summary = (
                    results_df.sort_values('time')
                    .groupby(['operation', 'size', 'kind'], as_index=False)
                    .first()
                )
                cols = [c for c in ['operation', 'size', 'kind', 'structure', 'time'] if c in summary.columns]
                st.dataframe(summary[cols])
            except Exception as e:
                st.warning(f"Analisis ringkas tidak dapat ditampilkan: {e}")
                st.dataframe(results_df)

            # Opsi ekspor sederhana (CSV)
            csv = results_df.to_csv(index=False)
            st.download_button("Unduh hasil (CSV)", data=csv, file_name="benchmark_results.csv", mime="text/csv")
        else:
            st.info("Tidak ada hasil. Periksa pengaturan dan coba lagi.")
else:
    st.info("Atur parameter di sidebar lalu klik 'Jalankan Benchmark' untuk memulai.")

st.markdown("---")
st.markdown("**Catatan**:")
st.markdown("- Hasil bersifat tidak menentu. jalankan beberapa kali agar bisa mendapatkan hasil yang sesuai")
st.markdown("- Jujur pas ngerun semuanya progresnya akan lama jadi saya sarankan untuk 1 per 1 saja. jika dipaksa sekaligus maka siapkan waktu 30 menit anda untuk memproses program ini")
st.markdown("- Jika ingin mengubah alurnya tekan silang saja apa yang inin dihapus pada side bar")
st.markdown("- #BTRGOESTOPARIS!")
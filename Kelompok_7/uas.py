import streamlit as st
import time
import random
import pandas as pd
import plotly.express as px
import sys

sys.setrecursionlimit(20000)

# ==========================================
# 1. IMPLEMENTASI STRUKTUR DATA
# ==========================================

class ListDS:
    def __init__(self):
        self.data = []

    def insert(self, value):
        self.data.append(value)

    def search_linear(self, value):
        for item in self.data:
            if item == value:
                return True
        return False

    def search_binary(self, value):
        self.data.sort()
        low, high = 0, len(self.data) - 1
        while low <= high:
            mid = (low + high) // 2
            if self.data[mid] == value:
                return True
            elif self.data[mid] < value:
                low = mid + 1
            else:
                high = mid - 1
        return False

    def delete(self, value):
        try:
            self.data.remove(value)
            return True
        except ValueError:
            return False

class HashTableDS:
    def __init__(self):
        self.table = {}

    def insert(self, value):
        self.table[value] = True

    def search(self, value):
        return value in self.table

    def delete(self, value):
        if value in self.table:
            del self.table[value]
            return True
        return False

class BSTNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, value):
        if self.root is None:
            self.root = BSTNode(value)
        else:
            self._insert_rec(self.root, value)

    def _insert_rec(self, node, value):
        if value < node.value:
            if node.left is None:
                node.left = BSTNode(value)
            else:
                self._insert_rec(node.left, value)
        else:
            if node.right is None:
                node.right = BSTNode(value)
            else:
                self._insert_rec(node.right, value)

    def search(self, value):
        return self._search_rec(self.root, value)

    def _search_rec(self, node, value):
        if node is None:
            return False
        if node.value == value:
            return True
        elif value < node.value:
            return self._search_rec(node.left, value)
        else:
            return self._search_rec(node.right, value)

    def delete(self, value):
        self.root = self._delete_rec(self.root, value)

    def _delete_rec(self, node, value):
        if node is None:
            return None
        if value < node.value:
            node.left = self._delete_rec(node.left, value)
        elif value > node.value:
            node.right = self._delete_rec(node.right, value)
        else:
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            temp = node.right
            while temp.left:
                temp = temp.left
            node.value = temp.value
            node.right = self._delete_rec(node.right, temp.value)
        return node

class AVLNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None

    def _get_h(self, node):
        return node.height if node else 0

    def _upd_h(self, node):
        node.height = 1 + max(self._get_h(node.left), self._get_h(node.right))

    def _rot_right(self, y):
        x = y.left
        y.left = x.right
        x.right = y
        self._upd_h(y)
        self._upd_h(x)
        return x

    def _rot_left(self, x):
        y = x.right
        x.right = y.left
        y.left = x
        self._upd_h(x)
        self._upd_h(y)
        return y

    
    def insert(self, value):
        self.root = self._ins_rec(self.root, value)

    def _ins_rec(self, node, value):
        if not node:
            return AVLNode(value)
        if value < node.value:
            node.left = self._ins_rec(node.left, value)
        else:
            node.right = self._ins_rec(node.right, value)
        
        self._upd_h(node)
        bal = self._get_h(node.left) - self._get_h(node.right)
        
        if bal > 1 and value < node.left.value:
            return self._rot_right(node)
        if bal < -1 and value > node.right.value:
            return self._rot_left(node)
        if bal > 1 and value > node.left.value:
            node.left = self._rot_left(node.left)
            return self._rot_right(node)
        if bal < -1 and value < node.right.value:
            node.right = self._rot_right(node.right)
            return self._rot_left(node)
        return node

    def search(self, value):
        return self._search_rec(self.root, value)

    def _search_rec(self, node, value):
        if node is None:
            return False
        if node.value == value:
            return True
        elif value < node.value:
            return self._search_rec(node.left, value)
        else:
            return self._search_rec(node.right, value)

    def _get_balance(self, node):
          if not node:
            return 0
          return self._get_h(node.left) - self._get_h(node.right)

    def delete(self, value):
        self.root = self._del_rec(self.root, value)

    def _del_rec(self, node, value):
        if not node:
            return None
        if value < node.value:
            node.left = self._del_rec(node.left, value)
        elif value > node.value:
            node.right = self._del_rec(node.right, value)
        else:
            if not node.left:
                return node.right
            if not node.right:
                return node.left
            temp = node.right
            while temp.left:
                temp = temp.left
            node.value = temp.value
            node.right = self._del_rec(node.right, temp.value)
        
        self._upd_h(node)
        bal = self._get_balance(node)

        # Left Left
        if bal > 1 and self._get_balance(node.left) >= 0:
            return self._rot_right(node)

        # Left Right
        if bal > 1 and self._get_balance(node.left) < 0:
            node.left = self._rot_left(node.left)
            return self._rot_right(node)

        # Right Right
        if bal < -1 and self._get_balance(node.right) <= 0:
            return self._rot_left(node)

        # Right Left
        if bal < -1 and self._get_balance(node.right) > 0:
            node.right = self._rot_right(node.right)
            return self._rot_left(node)
# ==========================================
# 2. LOGIC BENCHMARKING
# ==========================================

def run_single_benchmark(size, dtype, ds_type_str, op_type):
    # Generate Data
    if dtype == "Random":
        data = random.sample(range(size * 5), size)
    elif dtype == "Ascending":
        data = list(range(size))
    else:
        data = list(range(size, 0, -1))
    
    target = data[random.randint(0, size-1)] if size > 0 else 0
    
    # Pilih Struktur Data
    ds = None
    if ds_type_str == "Array (Linear)": 
        ds = ListDS()
    elif ds_type_str == "Array (Binary)": 
        ds = ListDS()
    elif ds_type_str == "Hash Table": 
        ds = HashTableDS()
    elif ds_type_str == "BST": 
        ds = BST()
    elif ds_type_str == "AVL Tree": 
        ds = AVLTree()
    
    elapsed = 0
    
    # ===== PERUBAHAN UTAMA DI SINI =====
    if op_type == "Insert":
        # Untuk Insert: Ukur waktu membangun SELURUH dataset
        start = time.perf_counter()
        for x in data:
            ds.insert(x)
        elapsed = (time.perf_counter() - start) * 1000  # dalam ms
        
    else:
        # Untuk Search & Delete: Build data dulu, lalu ukur 1x operasi
        # Build data
        for x in data:
            ds.insert(x)
            
        # Ukur waktu operasi
        start = time.perf_counter()
        
        if op_type == "Search":
            if ds_type_str == "Array (Linear)":
                ds.search_linear(target)
            elif ds_type_str == "Array (Binary)":
                ds.search_binary(target)
            else:
                ds.search(target)
        elif op_type == "Delete":
            if ds_type_str in ["Array (Linear)", "Array (Binary)"]:
                ds.delete(ds.data[0])
            else:
                ds.delete(target)
        
        elapsed = (time.perf_counter() - start) * 1000  # dalam ms
    
    return elapsed

def update_history(key, new_time):
    found = False
    for item in st.session_state[key]:
        if (item['ds'] == new_time['ds'] and 
            item['op'] == new_time['op'] and 
            item['size'] == new_time['size'] and 
            item['dtype'] == new_time['dtype']):
            item['count'] += 1
            item['time'] = ((item['time'] * (item['count']-1)) + new_time['time']) / item['count']
            found = True
            break
    if not found:
        st.session_state[key].append(new_time)

# ==========================================
# 3. STREAMLIT UI
# ==========================================

st.set_page_config(page_title="Benchmark Struktur Data", layout="wide")

if 'history' not in st.session_state:
    st.session_state['history'] = []

if 'last_result' not in st.session_state:
    st.session_state['last_result'] = None

st.title("📊 Benchmark Performa Struktur Data")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Pengaturan")
    ds_choice = st.selectbox("Pilih Struktur Data", 
        ["Array (Linear)", "Array (Binary)", "Hash Table", "BST", "AVL Tree"])
    size_choice = st.selectbox("Ukuran Dataset (N)", [100, 1000, 10000])
    type_choice = st.selectbox("Jenis Dataset", ["Random", "Ascending", "Descending"])
    op_choice = st.selectbox("Operasi", ["Search", "Insert", "Delete"])
    
    st.markdown("---")
    run_btn = st.button("🚀 Jalankan Benchmark", type="primary")
    clear_btn = st.button("🗑️ Reset Grafik")

# Logic Tombol
if clear_btn:
    st.session_state['history'] = []
    st.session_state['last_result'] = None
    st.rerun()

if run_btn:
    #Untuk Search/Delete: lakukan beberapa kali untuk rata-rata
    #Untuk Insert: cukup 1x karena sudah mengukur seluruh data
    if op_choice == "Insert":
        # Insert: 1x saja karena sudah mengukur semua 10.000 data
        avg_time = run_single_benchmark(size_choice, type_choice, ds_choice, op_choice)
    else:
        # Search/Delete: rata-rata 10x untuk akurasi
        total_time = 0
        for _ in range(10):
            t = run_single_benchmark(size_choice, type_choice, ds_choice, op_choice)
            total_time += t
        avg_time = total_time / 10
    
    res_data = {
        'ds': ds_choice,
        'op': op_choice,
        'size': size_choice,
        'dtype': type_choice,
        'time': round(avg_time, 4),
        'count': 1
    }
    
    update_history('history', res_data)
    st.session_state['last_result'] = res_data
    
    st.rerun()

# Tampilkan Hasil
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.markdown("### 📋 Hasil Terakhir")
    if st.session_state['last_result']:
        res = st.session_state['last_result']
        st.success(f"**Operasi:** {res['op']}")
        st.success(f"**Struktur Data:** {res['ds']}")
        st.success(f"**Ukuran:** {res['size']}")
        
        label_waktu = "Waktu Membangun Data (ms)" if res['op'] == "Insert" else "Waktu Rata-rata (ms)"
        st.success(f"**{label_waktu}:** {res['time']:.4f} ms")

with col2:
    st.markdown("### ⏱️ Kompleksitas Teori")
    comp = {
        "Array (Linear)": {"Search": "O(n)", "Insert": "O(1)*", "Delete": "O(n)"},
        "Array (Binary)": {"Search": "O(log n)", "Insert": "O(n)", "Delete": "O(n)"},
        "Hash Table": {"Search": "O(1)", "Insert": "O(1)", "Delete": "O(1)"},
        "BST": {"Search": "O(n)", "Insert": "O(n)", "Delete": "O(n)"},
        "AVL Tree": {"Search": "O(log n)", "Insert": "O(log n)", "Delete": "O(log n)"}
    }
    if st.session_state['last_result']:
        ds = st.session_state['last_result']['ds']
        op = st.session_state['last_result']['op']
        st.info(f"**Big O ({ds}):** {comp[ds][op]}")

with col3:
    st.markdown("### 📊 Rangkuman")
    st.write(f"Jumlah struktur data di grafik: **{len(st.session_state['history'])}**")

st.markdown("---")

# Visualisasi Grafik
st.subheader("📈 Grafik Perbandingan")

if len(st.session_state['history']) > 0:
    df = pd.DataFrame(st.session_state['history'])
    
    current_op = op_choice
    current_size = size_choice
    
    filtered_df = df[(df['op'] == current_op) & (df['size'] == current_size)]
    
    if not filtered_df.empty:
        y_label = "Waktu Membangun Data (ms)" if current_op == "Insert" else "Waktu (ms)"
        
        fig = px.bar(
            filtered_df, 
            x='ds', 
            y='time', 
            color='ds',
            title=f"Perbandingan Waktu Operasi {current_op} (N={current_size})",
            labels={'ds': 'Struktur Data', 'time': y_label},
            text='time'
        )
        fig.update_traces(texttemplate='%{text:.4f} ms', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("📋 Tabel Detail")
        st.dataframe(filtered_df[['ds', 'op', 'size', 'dtype', 'time', 'count']])
    else:
        st.warning("Belum ada data untuk kombinasi ini.")
else:
    st.info("Silakan pilih pengaturan dan Tekan tombol 'Jalankan Benchmark' untuk memulai.")

# Analisis Teks
if len(st.session_state['history']) > 0:
    st.markdown("---")
    st.subheader("📝 Analisis Hasil")
    
    if not filtered_df.empty:
        best_row = filtered_df.loc[filtered_df['time'].idxmin()]
        
        st.success(f"✅ **{best_row['ds']}** memiliki performa terbaik dengan waktu **{best_row['time']:.4f} ms**")
        
        if current_op == "Insert":
            explanation = f"""
            **Analisis untuk Operasi Insert (Membangun {current_size} Data):**
            
            1. **{best_row['ds']}** menjadi tercepat untuk membangun struktur data.
            
            2. Untuk dataset yang lebih besar (≥100.000):
               - **Hash Table** kemungkinan besar akan tetap cepat karena proses hashing O(1).
               - **AVL Tree** mungkin sedikit lebih lambat karena proses *rebalancing*.
               - **Array/BST** bisa sangat lambat terutama jika data terurut (worst case).
            
            3. Rekomendasi:
               - Gunakan **Hash Table** jika membutuhkan pembangunan data cepat.
               - Gunakan **AVL Tree** jika Urutan data penting setelah pembangunan.
            """
        else:
            explanation = f"""
            **Analisis untuk Operasi {current_op} (N={current_size}):**
            
            1. **{best_row['ds']}** menjadi tercepat.
            
            2. Kompleksitas teori **{comp[best_row['ds']][current_op]}** terlihat sesuai dengan hasil eksperimen.
            
            3. Rekomendasi untuk penggunaan nyata:
               - **Search**: Gunakan Hash Table untuk Pencarian data besar.
               - **Delete**: Gunakan AVL Tree untuk data yang sering berubah.
            """
        
        st.markdown(explanation)
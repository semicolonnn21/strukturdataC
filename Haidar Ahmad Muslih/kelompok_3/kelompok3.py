import streamlit as st
import random
import time
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="DS Benchmarking",
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Space+Grotesk:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
}

.main { background-color: #0d0f14; }

h1, h2, h3 { font-family: 'JetBrains Mono', monospace; }

.hero-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 2.4rem;
    font-weight: 700;
    color: #e2e8f0;
    letter-spacing: -1px;
    line-height: 1.2;
}
.hero-sub {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1rem;
    color: #64748b;
    margin-top: 0.3rem;
}
.accent { color: #38bdf8; }

.card {
    background: #161b27;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1rem;
}
.metric-val {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.6rem;
    font-weight: 700;
    color: #38bdf8;
}
.metric-label {
    font-size: 0.78rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 1px;
}
.badge {
    display: inline-block;
    background: #0f172a;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 2px 10px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: #94a3b8;
    margin: 2px;
}
.winner-badge {
    background: #0c2a1a;
    border: 1px solid #16a34a;
    color: #4ade80;
}
.section-header {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    color: #38bdf8;
    text-transform: uppercase;
    letter-spacing: 2px;
    border-bottom: 1px solid #1e293b;
    padding-bottom: 6px;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATA STRUCTURES
# ─────────────────────────────────────────────

# --- Array/List ---
class ArrayDS:
    def __init__(self): self.data = []
    def insert(self, val): self.data.append(val)
    def search(self, val): return val in self.data
    def delete(self, val):
        try: self.data.remove(val)
        except ValueError: pass

# --- Hash Table ---
class HashTable:
    def __init__(self, size=2048):
        self.size = size
        self.table = [[] for _ in range(size)]
    def _h(self, v): return hash(v) % self.size
    def insert(self, v): self.table[self._h(v)].append(v)
    def search(self, v): return v in self.table[self._h(v)]
    def delete(self, v):
        b = self.table[self._h(v)]
        if v in b: b.remove(v)

# --- BST (ITERATIF) ---
# CATATAN PERBAIKAN:
# Versi sebelumnya memakai rekursi (fungsi panggil dirinya sendiri) untuk
# insert/search/delete. Masalahnya: kalau dataset sudah terurut (Ascending
# atau Descending), BST akan "merosot" jadi rantai lurus sedalam jumlah
# elemennya. Untuk dataset "Besar" (10.000), itu berarti rekursi sedalam
# 10.000 — padahal limit rekursi default Python cuma 1000, jadi Python
# melempar RecursionError dan benchmark berhenti sebelum grafik sempat
# dibuat. Makanya hasil visualisasi "error".
# Solusinya: ditulis ulang jadi versi iteratif (pakai while-loop), jadi
# sedalam apa pun BST-nya, tidak akan pernah RecursionError lagi.
class BSTNode:
    def __init__(self, val): self.val = val; self.left = self.right = None

class BST:
    def __init__(self): self.root = None

    def insert(self, val):
        if self.root is None:
            self.root = BSTNode(val)
            return
        node = self.root
        while True:
            if val < node.val:
                if node.left is None:
                    node.left = BSTNode(val)
                    return
                node = node.left
            elif val > node.val:
                if node.right is None:
                    node.right = BSTNode(val)
                    return
                node = node.right
            else:
                return  # duplikat, abaikan

    def search(self, val):
        node = self.root
        while node:
            if val == node.val: return True
            node = node.left if val < node.val else node.right
        return False

    def delete(self, val):
        parent, node = None, self.root
        while node and node.val != val:
            parent = node
            node = node.left if val < node.val else node.right
        if node is None:
            return  # tidak ditemukan

        # Kasus punya 2 anak: cari successor (nilai terkecil di subtree kanan)
        if node.left is not None and node.right is not None:
            succ_parent, succ = node, node.right
            while succ.left is not None:
                succ_parent, succ = succ, succ.left
            node.val = succ.val
            parent, node = succ_parent, succ

        # Sekarang node punya maksimal 1 anak
        child = node.left if node.left is not None else node.right
        if parent is None:
            self.root = child
        elif parent.left is node:
            parent.left = child
        else:
            parent.right = child

# --- AVL Tree ---
class AVLNode:
    def __init__(self, val):
        self.val = val; self.left = self.right = None; self.height = 1

class AVL:
    def __init__(self): self.root = None
    def _h(self, n): return n.height if n else 0
    def _bf(self, n): return self._h(n.left) - self._h(n.right) if n else 0
    def _upd(self, n): n.height = 1 + max(self._h(n.left), self._h(n.right))
    def _rl(self, z):
        y = z.right; T2 = y.left; y.left = z; z.right = T2
        self._upd(z); self._upd(y); return y
    def _rr(self, z):
        y = z.left; T3 = y.right; y.right = z; z.left = T3
        self._upd(z); self._upd(y); return y
    def _bal(self, n, val):
        self._upd(n); bf = self._bf(n)
        if bf > 1:
            if val < n.left.val: return self._rr(n)
            n.left = self._rl(n.left); return self._rr(n)
        if bf < -1:
            if val > n.right.val: return self._rl(n)
            n.right = self._rr(n.right); return self._rl(n)
        return n
    def insert(self, val): self.root = self._ins(self.root, val)
    def _ins(self, node, val):
        if not node: return AVLNode(val)
        if val < node.val: node.left = self._ins(node.left, val)
        elif val > node.val: node.right = self._ins(node.right, val)
        else: return node
        return self._bal(node, val)
    def search(self, val):
        n = self.root
        while n:
            if val == n.val: return True
            n = n.left if val < n.val else n.right
        return False
    def delete(self, val): self.root = self._del(self.root, val)
    def _del(self, node, val):
        if not node: return node
        if val < node.val: node.left = self._del(node.left, val)
        elif val > node.val: node.right = self._del(node.right, val)
        else:
            if not node.left: return node.right
            if not node.right: return node.left
            mn = node.right
            while mn.left: mn = mn.left
            node.val = mn.val
            node.right = self._del(node.right, mn.val)
        if not node: return node
        self._upd(node)
        bf = self._bf(node)
        if bf > 1:
            if self._bf(node.left) >= 0: return self._rr(node)
            node.left = self._rl(node.left); return self._rr(node)
        if bf < -1:
            if self._bf(node.right) <= 0: return self._rl(node)
            node.right = self._rr(node.right); return self._rl(node)
        return node

# ─────────────────────────────────────────────
# BENCHMARK FUNCTION
# ─────────────────────────────────────────────
def generate_dataset(size, kind):
    if kind == "Random": return random.sample(range(size * 10), size)
    elif kind == "Ascending": return list(range(size))
    else: return list(range(size, 0, -1))

def benchmark(ds_name, ds_cls, dataset, n_search=50):
    ds = ds_cls()
    results = {}

    # INSERT
    t0 = time.perf_counter()
    for v in dataset:
        ds.insert(v)
    results["insert"] = (time.perf_counter() - t0) * 1000

    # SEARCH
    targets = random.sample(dataset, min(n_search, len(dataset)))
    t0 = time.perf_counter()
    for v in targets:
        ds.search(v)
    results["search"] = (time.perf_counter() - t0) * 1000

    # DELETE
    to_del = random.sample(dataset, min(n_search, len(dataset)))
    t0 = time.perf_counter()
    for v in to_del:
        ds.delete(v)
    results["delete"] = (time.perf_counter() - t0) * 1000

    return results

# ─────────────────────────────────────────────
# COLORS
# ─────────────────────────────────────────────
DS_COLORS = {
    "Array/List":   "#38bdf8",
    "Hash Table":   "#4ade80",
    "BST":          "#f97316",
    "AVL Tree":     "#c084fc",
}

DS_MAP = {
    "Array/List": ArrayDS,
    "Hash Table": HashTable,
    "BST": BST,
    "AVL Tree": AVL,
}

COMPLEXITY = {
    "Array/List":   {"search": "O(n)", "insert": "O(1)", "delete": "O(n)"},
    "Hash Table":   {"search": "O(1)", "insert": "O(1)", "delete": "O(1)"},
    "BST":          {"search": "O(log n)*", "insert": "O(log n)*", "delete": "O(log n)*"},
    "AVL Tree":     {"search": "O(log n)", "insert": "O(log n)", "delete": "O(log n)"},
}

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="section-header">⚙ Konfigurasi</div>', unsafe_allow_html=True)

    dataset_size = st.selectbox(
        "Ukuran Dataset",
        options=[100, 1000, 10000],
        format_func=lambda x: f"{'Kecil' if x==100 else 'Sedang' if x==1000 else 'Besar'} — {x:,} data"
    )

    dataset_type = st.selectbox(
        "Jenis Dataset",
        ["Random", "Ascending", "Descending"]
    )

    selected_ds = st.multiselect(
        "Struktur Data",
        list(DS_MAP.keys()),
        default=list(DS_MAP.keys())
    )

    st.markdown('<div class="section-header" style="margin-top:1.5rem;">ℹ Kompleksitas</div>', unsafe_allow_html=True)
    for ds in list(DS_MAP.keys()):
        c = COMPLEXITY[ds]
        st.markdown(f"""
        <div style="margin-bottom:0.6rem;">
        <span style="color:#94a3b8;font-family:'JetBrains Mono',monospace;font-size:0.8rem;">{ds}</span><br>
        <span class="badge">S: {c['search']}</span>
        <span class="badge">I: {c['insert']}</span>
        <span class="badge">D: {c['delete']}</span>
        </div>
        """, unsafe_allow_html=True)

    run_btn = st.button("▶ Jalankan Benchmark", use_container_width=True, type="primary")

    st.markdown('<hr style="border-color:#1e293b;margin:1.2rem 0;">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">🔬 Mode Lanjutan</div>', unsafe_allow_html=True)
    st.caption("Otomatis menjalankan 100 / 1.000 / 10.000 data × Random / Ascending / Descending untuk setiap struktur data terpilih di atas.")
    comp_btn = st.button("📊 Analisis Lengkap (Semua Skenario)", use_container_width=True)

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-title">⚡ DS <span class="accent">Benchmark</span></div>
<div class="hero-sub">Benchmarking Performa Struktur Data — Searching · Insertion · Deletion</div>
<br>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
if run_btn:
    if not selected_ds:
        st.warning("Pilih minimal satu struktur data.")
        st.stop()

    try:
        with st.spinner("Menjalankan benchmark..."):
            dataset = generate_dataset(dataset_size, dataset_type)
            all_results = {}
            for ds_name in selected_ds:
                all_results[ds_name] = benchmark(ds_name, DS_MAP[ds_name], dataset)
    except Exception as e:
        st.error(f"Benchmark gagal dijalankan: {e}")
        st.stop()

    # ── Summary metrics ──
    st.markdown('<div class="section-header">📊 Ringkasan Hasil</div>', unsafe_allow_html=True)
    cols = st.columns(len(selected_ds))
    for i, ds_name in enumerate(selected_ds):
        r = all_results[ds_name]
        total = sum(r.values())
        with cols[i]:
            st.markdown(f"""
            <div class="card">
                <div style="color:{DS_COLORS[ds_name]};font-family:'JetBrains Mono',monospace;font-size:0.85rem;font-weight:700;margin-bottom:0.5rem;">{ds_name}</div>
                <div class="metric-val">{total:.3f}<span style="font-size:0.9rem;color:#64748b;"> ms</span></div>
                <div class="metric-label">Total Waktu</div>
                <hr style="border-color:#1e293b;margin:0.7rem 0;">
                <div style="font-size:0.8rem;color:#94a3b8;">
                Insert: <b style="color:#e2e8f0;">{r['insert']:.3f} ms</b><br>
                Search: <b style="color:#e2e8f0;">{r['search']:.3f} ms</b><br>
                Delete: <b style="color:#e2e8f0;">{r['delete']:.3f} ms</b>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Charts ──
    st.markdown('<div class="section-header" style="margin-top:1rem;">📈 Visualisasi</div>', unsafe_allow_html=True)

    operations = ["insert", "search", "delete"]
    # sharey=True -> ketiga subplot pakai skala sumbu-Y yang SAMA, supaya
    # tinggi bar antar-chart (insert vs search vs delete) bisa dibandingkan
    # secara visual. Tanpa ini, tiap subplot auto-scale sendiri-sendiri
    # sehingga nilai kecil dan besar bisa kelihatan "sama tinggi".
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5), sharey=True)
    fig.patch.set_facecolor("#0d0f14")

    for i, (ax, op) in enumerate(zip(axes, operations)):
        ax.set_facecolor("#161b27")
        vals = [all_results[ds][op] for ds in selected_ds]
        colors = [DS_COLORS[ds] for ds in selected_ds]
        bars = ax.bar(selected_ds, vals, color=colors, width=0.55, zorder=3)
        ax.set_title(op.upper(), color="#e2e8f0", fontsize=11,
                     fontfamily="monospace", pad=10)
        if i == 0:
            ax.set_ylabel("Waktu (ms)", color="#64748b", fontsize=9)
        ax.tick_params(colors="#94a3b8", labelsize=8)
        ax.spines[:].set_color("#1e293b")
        ax.yaxis.label.set_color("#64748b")
        ax.grid(axis="y", color="#1e293b", linewidth=0.8, zorder=0)
        max_val = max(vals) if max(vals) > 0 else 1
        for bar, val in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max_val*0.02,
                    f"{val:.3f}", ha="center", va="bottom", fontsize=7.5,
                    color="#e2e8f0", fontfamily="monospace")
        for label in ax.get_xticklabels():
            label.set_rotation(15)
            label.set_ha("right")

    plt.tight_layout(pad=2)
    st.pyplot(fig)

    # ── Grouped bar (comparison) ──
    fig2, ax2 = plt.subplots(figsize=(12, 4.5))
    fig2.patch.set_facecolor("#0d0f14")
    ax2.set_facecolor("#161b27")
    x = np.arange(len(operations))
    w = 0.8 / len(selected_ds)
    for i, ds in enumerate(selected_ds):
        vals = [all_results[ds][op] for op in operations]
        offset = (i - len(selected_ds)/2 + 0.5) * w
        ax2.bar(x + offset, vals, w*0.85, label=ds,
                color=DS_COLORS[ds], zorder=3, alpha=0.9)

    ax2.set_xticks(x)
    ax2.set_xticklabels([o.upper() for o in operations], color="#e2e8f0",
                         fontfamily="monospace", fontsize=10)
    ax2.set_ylabel("Waktu (ms)", color="#64748b")
    ax2.set_title("Perbandingan Semua Operasi", color="#e2e8f0",
                  fontfamily="monospace", fontsize=12, pad=12)
    ax2.tick_params(colors="#94a3b8")
    ax2.spines[:].set_color("#1e293b")
    ax2.grid(axis="y", color="#1e293b", linewidth=0.8, zorder=0)
    ax2.legend(facecolor="#161b27", edgecolor="#334155",
               labelcolor="#e2e8f0", fontsize=9)
    plt.tight_layout()
    st.pyplot(fig2)

    # ── Data Table ──
    st.markdown('<div class="section-header" style="margin-top:1rem;">📋 Tabel Data</div>', unsafe_allow_html=True)
    rows = []
    for ds in selected_ds:
        r = all_results[ds]
        rows.append({
            "Struktur Data": ds,
            "Insert (ms)": round(r["insert"], 4),
            "Search (ms)": round(r["search"], 4),
            "Delete (ms)": round(r["delete"], 4),
            "Total (ms)": round(sum(r.values()), 4),
            "Search Complexity": COMPLEXITY[ds]["search"],
        })
    df = pd.DataFrame(rows).sort_values("Total (ms)")
    df.insert(0, "Rank", range(1, len(df)+1))

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
    )

    # ── Analysis ──
    st.markdown('<div class="section-header" style="margin-top:1rem;">🧠 Analisis Otomatis</div>', unsafe_allow_html=True)

    best_search = min(selected_ds, key=lambda d: all_results[d]["search"])
    best_insert = min(selected_ds, key=lambda d: all_results[d]["insert"])
    best_overall = min(selected_ds, key=lambda d: sum(all_results[d].values()))

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="card">
            <div class="section-header">🏆 Pemenang</div>
            <p>🔍 <b>Search tercepat:</b> <span style="color:#4ade80;">{best_search}</span>
            — {all_results[best_search]['search']:.4f} ms</p>
            <p>➕ <b>Insert tercepat:</b> <span style="color:#4ade80;">{best_insert}</span>
            — {all_results[best_insert]['insert']:.4f} ms</p>
            <p>⭐ <b>Overall terbaik:</b> <span style="color:#38bdf8;">{best_overall}</span>
            — {sum(all_results[best_overall].values()):.4f} ms total</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="card">
            <div class="section-header">📌 Kesimpulan</div>
            <p style="color:#94a3b8;font-size:0.9rem;line-height:1.7;">
            Dataset <b style="color:#e2e8f0;">{dataset_type}</b> ukuran 
            <b style="color:#e2e8f0;">{dataset_size:,}</b> data.<br>
            Hash Table unggul di search/insert O(1), namun buruk di dataset terurut karena collision.
            AVL Tree menjamin O(log n) balanced di semua kasus.
            BST cepat di dataset random, lambat di dataset terurut (degenerasi ke O(n)).
            Array/List paling lambat untuk search & delete karena O(n).
            </p>
        </div>
        """, unsafe_allow_html=True)

    # ── Per-DS Analysis ──
    st.markdown('<div class="section-header" style="margin-top:0.5rem;">📝 Analisis Per Struktur Data</div>', unsafe_allow_html=True)
    analysis_text = {
        "Array/List": "**Kelebihan:** Implementasi sederhana, insert di akhir O(1). **Kekurangan:** Search dan delete O(n) — sangat lambat untuk data besar. **Prediksi scaling:** Waktu naik linear; 10x data → ~10x lebih lambat.",
        "Hash Table": "**Kelebihan:** Search, insert, delete rata-rata O(1) — tercepat secara teoritis. **Kekurangan:** Performa menurun jika banyak collision (dataset terurut). Tidak mendukung operasi ordered. **Prediksi scaling:** Relatif stabil hingga terjadi resize tabel.",
        "BST": "**Kelebihan:** Operasi O(log n) pada kasus rata-rata. **Kekurangan:** Dataset terurut menyebabkan BST degenerasi menjadi linked list → O(n). **Prediksi scaling:** Bergantung distribusi data; berbahaya untuk input terurut.",
        "AVL Tree": "**Kelebihan:** Self-balancing menjamin O(log n) di semua kasus. **Kekurangan:** Overhead rotasi pada insert/delete. **Prediksi scaling:** Konsisten logaritmik; sangat andal untuk data besar.",
    }
    cols2 = st.columns(2)
    for i, ds in enumerate(selected_ds):
        with cols2[i % 2]:
            st.markdown(f"""
            <div class="card">
                <span style="color:{DS_COLORS[ds]};font-family:'JetBrains Mono',monospace;font-weight:700;">{ds}</span>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(analysis_text.get(ds, ""), unsafe_allow_html=False)

elif comp_btn:
    if not selected_ds:
        st.warning("Pilih minimal satu struktur data di sidebar.")
        st.stop()

    SIZES = [100, 1000, 10000]
    TYPES = ["Random", "Ascending", "Descending"]
    TYPE_LABELS = {"Random": "Random", "Ascending": "Sorted", "Descending": "Descending"}
    TYPE_COLORS = {"Random": "#38bdf8", "Ascending": "#4ade80", "Descending": "#f97316"}
    OPS = [("search", "Searching"), ("insert", "Insertion"), ("delete", "Deletion")]

    try:
        with st.spinner("Menjalankan seluruh kombinasi benchmark (100/1.000/10.000 × Random/Ascending/Descending)..."):
            comp_results = {}
            for ds_name in selected_ds:
                comp_results[ds_name] = {}
                for size in SIZES:
                    comp_results[ds_name][size] = {}
                    for t in TYPES:
                        dataset = generate_dataset(size, t)
                        comp_results[ds_name][size][t] = benchmark(ds_name, DS_MAP[ds_name], dataset)
    except Exception as e:
        st.error(f"Analisis lengkap gagal dijalankan: {e}")
        st.stop()

    st.markdown('<div class="section-header">🔬 Analisis Lengkap — Semua Ukuran &amp; Jenis Dataset</div>', unsafe_allow_html=True)

    for ds_name in selected_ds:
        st.markdown(f"""
        <div style="text-align:center;font-family:'JetBrains Mono',monospace;
        font-size:1.05rem;color:#e2e8f0;font-weight:700;margin:1.4rem 0 0.6rem 0;">
        Hasil Benchmarking Struktur Data <span style="color:{DS_COLORS[ds_name]};">{ds_name}</span>
        </div>
        """, unsafe_allow_html=True)

        fig, axes = plt.subplots(1, 3, figsize=(15, 4.6))
        fig.patch.set_facecolor("#0d0f14")

        for ax, (op_key, op_label) in zip(axes, OPS):
            ax.set_facecolor("#161b27")
            x = np.arange(len(SIZES))
            w = 0.8 / len(TYPES)
            for i, t in enumerate(TYPES):
                # nilai dijaga > 0 agar aman dipakai pada skala log
                vals = [max(comp_results[ds_name][size][t][op_key], 1e-6) for size in SIZES]
                offset = (i - len(TYPES) / 2 + 0.5) * w
                ax.bar(x + offset, vals, w * 0.85, label=TYPE_LABELS[t],
                       color=TYPE_COLORS[t], zorder=3)
            ax.set_yscale("log")
            ax.set_xticks(x)
            ax.set_xticklabels([f"{s:,}".replace(",", ".") for s in SIZES],
                                color="#94a3b8", fontfamily="monospace", fontsize=8.5)
            ax.set_title(op_label, color="#e2e8f0", fontfamily="monospace",
                         fontsize=12, pad=10)
            ax.set_xlabel("Ukuran Dataset", color="#64748b", fontsize=9)
            if op_key == "search":
                ax.set_ylabel("Waktu (ms, skala log)", color="#64748b", fontsize=9)
            ax.tick_params(colors="#94a3b8", labelsize=8)
            ax.spines[:].set_color("#1e293b")
            ax.grid(axis="y", which="major", color="#1e293b", linewidth=0.7, zorder=0)

        handles, labels = axes[0].get_legend_handles_labels()
        fig.legend(handles, labels, loc="upper center", ncol=3,
                   facecolor="#161b27", edgecolor="#334155",
                   labelcolor="#e2e8f0", fontsize=9, frameon=True)
        plt.tight_layout(rect=[0, 0, 1, 0.88])
        st.pyplot(fig)

    st.caption("Skala sumbu-Y logaritmik, supaya selisih waktu antar ukuran dataset (100 → 10.000) tetap kelihatan jelas walau bedanya ratusan kali lipat.")

else:
    st.markdown("""
    <div class="card" style="text-align:center;padding:3rem;">
        <div style="font-size:3rem;margin-bottom:1rem;">⚡</div>
        <div style="font-family:'JetBrains Mono',monospace;color:#64748b;font-size:1rem;">
            Atur konfigurasi di sidebar, lalu klik <b style="color:#38bdf8;">▶ Jalankan Benchmark</b>
        </div>
        <br>
        <div style="color:#475569;font-size:0.85rem;">
            Struktur Data: Array/List · Hash Table · BST · AVL Tree<br>
            Operasi: Insert · Search · Delete
        </div>
    </div>
    """, unsafe_allow_html=True)
import streamlit as st
import random
import time
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from data_structures import Array, BSTWrapper, HashTableWrapper, AVLWrapper

st.set_page_config(
    page_title="DS Benchmark",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CSS ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.main { background: #0f1117; }

.hero {
    background: linear-gradient(135deg, #1a1f2e 0%, #0f1117 50%, #1a1f2e 100%);
    border: 1px solid #2d3748;
    border-radius: 16px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle at 30% 50%, rgba(99,102,241,0.08) 0%, transparent 50%),
                radial-gradient(circle at 70% 50%, rgba(16,185,129,0.06) 0%, transparent 50%);
    pointer-events: none;
}
.hero h1 {
    font-size: 2.2rem;
    font-weight: 700;
    color: #f1f5f9;
    margin: 0 0 0.4rem 0;
    letter-spacing: -0.5px;
}
.hero p {
    color: #94a3b8;
    font-size: 1rem;
    margin: 0;
}
.hero .badge {
    display: inline-block;
    background: rgba(99,102,241,0.15);
    color: #818cf8;
    border: 1px solid rgba(99,102,241,0.3);
    border-radius: 20px;
    padding: 0.2rem 0.8rem;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
}

.metric-card {
    background: #1e2433;
    border: 1px solid #2d3748;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1rem;
}
.metric-card .label {
    color: #64748b;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 0.3rem;
}
.metric-card .value {
    color: #f1f5f9;
    font-size: 1.6rem;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
}
.metric-card .sub {
    color: #64748b;
    font-size: 0.8rem;
    margin-top: 0.2rem;
}

.winner-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(16,185,129,0.12);
    border: 1px solid rgba(16,185,129,0.3);
    color: #10b981;
    border-radius: 8px;
    padding: 0.3rem 0.8rem;
    font-size: 0.8rem;
    font-weight: 600;
}

.analysis-box {
    background: #1e2433;
    border-left: 3px solid #6366f1;
    border-radius: 0 10px 10px 0;
    padding: 1.2rem 1.5rem;
    margin: 0.6rem 0;
    color: #cbd5e1;
    font-size: 0.9rem;
    line-height: 1.6;
}
.analysis-box strong { color: #f1f5f9; }

.section-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: #f1f5f9;
    margin: 1.5rem 0 0.8rem 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.stButton > button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 0.6rem 2rem !important;
    transition: all 0.2s ease !important;
    font-family: 'Inter', sans-serif !important;
}
.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}

div[data-testid="stSelectbox"] > div > div {
    background: #1e2433 !important;
    border-color: #2d3748 !important;
    color: #f1f5f9 !important;
    border-radius: 8px !important;
}
div[data-testid="stMultiSelect"] > div > div {
    background: #1e2433 !important;
    border-color: #2d3748 !important;
    border-radius: 8px !important;
}

.complexity-table { width: 100%; border-collapse: collapse; margin: 1rem 0; }
.complexity-table th {
    background: #1e2433;
    color: #94a3b8;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    padding: 0.7rem 1rem;
    text-align: left;
    border-bottom: 1px solid #2d3748;
}
.complexity-table td {
    padding: 0.65rem 1rem;
    color: #cbd5e1;
    font-size: 0.85rem;
    border-bottom: 1px solid #1a1f2e;
    font-family: 'JetBrains Mono', monospace;
}
.complexity-table tr:hover td { background: #1e2433; }
.o1 { color: #10b981; font-weight: 600; }
.ologn { color: #6366f1; font-weight: 600; }
.on { color: #f59e0b; font-weight: 600; }
.onlogn { color: #ef4444; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# ─── HERO ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="badge">⚡ UAS Struktur Data</div>
    <h1>Data Structure Benchmark</h1>
    <p>Bandingkan performa Array · BST · Hash Table · AVL Tree pada operasi Search, Insert, dan Delete</p>
</div>
""", unsafe_allow_html=True)

# ─── SIDEBAR ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Konfigurasi")

    dataset_size = st.selectbox(
        "Ukuran Dataset",
        options=[100, 1000, 10000],
        format_func=lambda x: f"Kecil — {x:,} data" if x == 100 else (
            f"Sedang — {x:,} data" if x == 1000 else f"Besar — {x:,} data")
    )

    dataset_type = st.selectbox(
        "Jenis Dataset",
        options=["random", "sorted", "descending"],
        format_func=lambda x: {"random": "🎲 Acak", "sorted": "📈 Terurut (Ascending)", "descending": "📉 Descending"}[x]
    )

    operations = st.multiselect(
        "Operasi",
        options=["search", "insert", "delete"],
        default=["search", "insert", "delete"],
        format_func=lambda x: {"search": "🔍 Search", "insert": "➕ Insert", "delete": "🗑️ Delete"}[x]
    )

    structures = st.multiselect(
        "Struktur Data",
        options=["Array", "BST", "Hash Table", "AVL Tree"],
        default=["Array", "BST", "Hash Table", "AVL Tree"]
    )

    st.markdown("---")
    run_btn = st.button("▶  Jalankan Benchmark", use_container_width=True)

    st.markdown("---")
    st.markdown("#### 📚 Kompleksitas Teoritis")
    st.markdown("""
    <table class="complexity-table">
    <tr><th>Struktur</th><th>Search</th><th>Insert</th><th>Delete</th></tr>
    <tr><td>Array</td><td class="on">O(n)</td><td class="on">O(n)</td><td class="on">O(n)</td></tr>
    <tr><td>BST</td><td class="ologn">O(log n)</td><td class="ologn">O(log n)</td><td class="ologn">O(log n)</td></tr>
    <tr><td>Hash Table</td><td class="o1">O(1)</td><td class="o1">O(1)</td><td class="o1">O(1)</td></tr>
    <tr><td>AVL Tree</td><td class="ologn">O(log n)</td><td class="ologn">O(log n)</td><td class="ologn">O(log n)</td></tr>
    </table>
    """, unsafe_allow_html=True)

# ─── HELPERS ────────────────────────────────────────────────────────────────
def generate_dataset(size, dtype):
    base = list(range(1, size + 1))
    if dtype == "random":
        random.shuffle(base)
    elif dtype == "sorted":
        pass
    else:
        base = base[::-1]
    return base

STRUCT_MAP = {
    "Array": Array,
    "BST": BSTWrapper,
    "Hash Table": HashTableWrapper,
    "AVL Tree": AVLWrapper,
}
COLORS = {
    "Array": "#f59e0b",
    "BST": "#6366f1",
    "Hash Table": "#10b981",
    "AVL Tree": "#ec4899",
}

def run_benchmark(data, structs, ops):
    results = []
    progress = st.progress(0, text="Mempersiapkan benchmark...")
    total = len(structs) * len(ops)
    step = 0

    for sname in structs:
        ds = STRUCT_MAP[sname]()
        # Build structure first
        for val in data:
            ds.insert(val)

        for op in ops:
            step += 1
            progress.progress(step / total, text=f"Benchmarking {sname} — {op}...")

            target = data[len(data) // 2]   # middle element as target
            REPS = min(200, len(data))
            targets = random.choices(data, k=REPS)

            if op == "search":
                t0 = time.perf_counter()
                for t in targets:
                    ds.search(t)
                elapsed = (time.perf_counter() - t0) / REPS * 1e6  # µs per op

            elif op == "insert":
                new_vals = [max(data) + i + 1 for i in range(REPS)]
                t0 = time.perf_counter()
                for v in new_vals:
                    ds.insert(v)
                elapsed = (time.perf_counter() - t0) / REPS * 1e6

            else:  # delete
                del_targets = random.choices(data[:len(data)//2], k=min(REPS, len(data)//2))
                t0 = time.perf_counter()
                for t in del_targets:
                    ds.delete(t)
                elapsed = (time.perf_counter() - t0) / len(del_targets) * 1e6

            results.append({
                "Struktur Data": sname,
                "Operasi": op.capitalize(),
                "Waktu (µs)": round(elapsed, 4),
            })

    progress.empty()
    return pd.DataFrame(results)

# ─── MAIN CONTENT ───────────────────────────────────────────────────────────
if not run_btn:
    st.markdown("""
    <div style="text-align:center; padding: 3rem 2rem; color: #475569;">
        <div style="font-size: 3rem; margin-bottom: 1rem;">📊</div>
        <div style="font-size: 1.1rem; font-weight: 600; color: #94a3b8; margin-bottom: 0.4rem;">Siap untuk Benchmark</div>
        <div style="font-size: 0.9rem;">Atur konfigurasi di sidebar, lalu tekan <strong style="color:#6366f1">▶ Jalankan Benchmark</strong></div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

if not operations:
    st.warning("⚠️ Pilih minimal satu operasi!")
    st.stop()
if not structures:
    st.warning("⚠️ Pilih minimal satu struktur data!")
    st.stop()

# Generate & run
with st.spinner("Generating dataset..."):
    dataset = generate_dataset(dataset_size, dataset_type)

df = run_benchmark(dataset, structures, operations)

# ─── SUMMARY METRICS ────────────────────────────────────────────────────────
st.markdown('<div class="section-title">📈 Ringkasan Hasil</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
fastest = df.loc[df["Waktu (µs)"].idxmin()]
slowest = df.loc[df["Waktu (µs)"].idxmax()]

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="label">Total Pengujian</div>
        <div class="value">{len(df)}</div>
        <div class="sub">{len(structures)} struktur × {len(operations)} operasi</div>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="label">Dataset</div>
        <div class="value">{dataset_size:,}</div>
        <div class="sub">{dataset_type.capitalize()} order</div>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="label">⚡ Tercepat</div>
        <div class="value" style="color:#10b981">{fastest['Waktu (µs)']:.4f}</div>
        <div class="sub">{fastest['Struktur Data']} — {fastest['Operasi']} (µs/op)</div>
    </div>""", unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="label">🐢 Terlambat</div>
        <div class="value" style="color:#f59e0b">{slowest['Waktu (µs)']:.4f}</div>
        <div class="sub">{slowest['Struktur Data']} — {slowest['Operasi']} (µs/op)</div>
    </div>""", unsafe_allow_html=True)

# ─── CHARTS ─────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">📊 Visualisasi Performa</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["  Bar Chart  ", "  Grouped Comparison  ", "  Heatmap  "])

chart_layout = dict(
    paper_bgcolor="#0f1117",
    plot_bgcolor="#0f1117",
    font=dict(family="Inter", color="#94a3b8"),
    margin=dict(t=40, b=40, l=10, r=10),
    legend=dict(bgcolor="#1e2433", bordercolor="#2d3748", borderwidth=1),
    xaxis=dict(gridcolor="#1e2433", zerolinecolor="#2d3748"),
    yaxis=dict(gridcolor="#1e2433", zerolinecolor="#2d3748"),
)

with tab1:
    for op in [o.capitalize() for o in operations]:
        sub = df[df["Operasi"] == op]
        if sub.empty:
            continue
        fig = go.Figure()
        for sname in structures:
            row = sub[sub["Struktur Data"] == sname]
            if not row.empty:
                fig.add_trace(go.Bar(
                    x=[sname], y=row["Waktu (µs)"].values,
                    name=sname,
                    marker_color=COLORS.get(sname, "#6366f1"),
                    marker_line_width=0,
                ))
        fig.update_layout(
            **chart_layout,
            title=dict(text=f"Operasi <b>{op}</b>", font=dict(color="#f1f5f9", size=14)),
            yaxis_title="Waktu (µs/operasi)",
            showlegend=False,
            height=280,
            bargap=0.35,
        )
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    pivot = df.pivot_table(index="Struktur Data", columns="Operasi", values="Waktu (µs)")
    fig2 = go.Figure()
    for op in pivot.columns:
        fig2.add_trace(go.Bar(
            name=op,
            x=pivot.index,
            y=pivot[op],
            text=[f"{v:.4f}" for v in pivot[op]],
            textposition="outside",
            textfont=dict(size=10),
        ))
    fig2.update_layout(
        **chart_layout,
        barmode="group",
        yaxis_title="Waktu (µs/operasi)",
        height=420,
        bargap=0.2,
        bargroupgap=0.08,
    )
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    pivot2 = df.pivot_table(index="Struktur Data", columns="Operasi", values="Waktu (µs)")
    fig3 = go.Figure(data=go.Heatmap(
        z=pivot2.values,
        x=pivot2.columns.tolist(),
        y=pivot2.index.tolist(),
        colorscale=[[0, "#10b981"], [0.5, "#6366f1"], [1, "#ef4444"]],
        text=[[f"{v:.4f} µs" for v in row] for row in pivot2.values],
        texttemplate="%{text}",
        showscale=True,
    ))
    fig3.update_layout(
        **chart_layout,
        height=350,
        title=dict(text="Heatmap Waktu Eksekusi (µs) — hijau = cepat", font=dict(color="#f1f5f9", size=13)),
    )
    st.plotly_chart(fig3, use_container_width=True)

# ─── DATA TABLE ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">📋 Tabel Hasil Benchmark</div>', unsafe_allow_html=True)

display_df = df.copy()
display_df["Waktu (µs)"] = display_df["Waktu (µs)"].map(lambda x: f"{x:.6f}")
st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Struktur Data": st.column_config.TextColumn("Struktur Data", width="medium"),
        "Operasi": st.column_config.TextColumn("Operasi", width="small"),
        "Waktu (µs)": st.column_config.TextColumn("Waktu (µs/op)", width="medium"),
    }
)

# ─── ANALYSIS ───────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">🔬 Analisis Otomatis</div>', unsafe_allow_html=True)

best_per_op = df.loc[df.groupby("Operasi")["Waktu (µs)"].idxmin()].set_index("Operasi")
worst_per_op = df.loc[df.groupby("Operasi")["Waktu (µs)"].idxmax()].set_index("Operasi")

for op in [o.capitalize() for o in operations]:
    if op not in best_per_op.index:
        continue
    b = best_per_op.loc[op]
    w = worst_per_op.loc[op]
    speedup = w["Waktu (µs)"] / b["Waktu (µs)"] if b["Waktu (µs)"] > 0 else 0
    st.markdown(f"""
    <div class="analysis-box">
        <strong>Operasi {op}</strong><br>
        🏆 Tercepat: <strong style="color:#10b981">{b['Struktur Data']}</strong> ({b['Waktu (µs)']:.4f} µs/op) &nbsp;|&nbsp;
        🐢 Terlambat: <strong style="color:#f59e0b">{w['Struktur Data']}</strong> ({w['Waktu (µs)']:.4f} µs/op)<br>
        {b['Struktur Data']} lebih cepat <strong style="color:#6366f1">{speedup:.1f}×</strong> dibanding {w['Struktur Data']} pada dataset {dataset_type} berukuran {dataset_size:,} data.
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="analysis-box" style="border-left-color: #10b981; margin-top:1rem;">
    <strong>📌 Kesimpulan Umum</strong><br>
    • <strong>Hash Table</strong> unggul di operasi <em>search</em> karena kompleksitas O(1) — langsung ke bucket tanpa traversal.<br>
    • <strong>AVL Tree & BST</strong> seimbang di O(log n) untuk search/insert/delete berkat struktur tree yang menjaga keseimbangan (khusus AVL).<br>
    • <strong>Array</strong> paling lambat untuk dataset besar karena harus scan linear O(n) saat search dan shift elemen saat insert/delete.<br>
    • Semakin besar dataset, selisih performa antar struktur semakin signifikan — terutama antara O(1) Hash Table vs O(n) Array.
</div>
""", unsafe_allow_html=True)

# ─── FOOTER ─────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#475569; font-size:0.8rem;'>"
    "Data Structure Benchmark · UAS Struktur Data · Built with Streamlit & Plotly"
    "</div>",
    unsafe_allow_html=True
)

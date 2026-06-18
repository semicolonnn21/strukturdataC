import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Circle
import numpy as np
import re
import pandas as pd

st.set_page_config(page_title="Tugas Struktur Data", layout="centered")

st.title("📘 Tugas Mandiri – Struktur Data")
st.caption("Set & Dictionary | Informatika UINSSC MMXXVI")
st.markdown("---")

tab1, tab2 = st.tabs(["🔵 Operasi Set", "💬 Word Count Komentar"])

# ════════════════════════════════════════════════════════════
# TAB 1 – OPERASI SET
# ════════════════════════════════════════════════════════════
with tab1:
    st.header("Visualisasi Operasi Set")

    col1, col2 = st.columns(2)
    with col1:
        input_a = st.text_input("Set A (pisahkan dengan koma)", value="1, 2, 3, 4, 5", key="seta")
    with col2:
        input_b = st.text_input("Set B (pisahkan dengan koma)", value="4, 5, 6, 7, 8", key="setb")

    def parse_set(text):
        try:
            return set(int(x.strip()) for x in text.split(",") if x.strip())
        except ValueError:
            return set(x.strip() for x in text.split(",") if x.strip())

    set_a = parse_set(input_a)
    set_b = parse_set(input_b)

    col3, col4 = st.columns(2)
    col3.info(f"**Set A:** `{sorted(set_a)}`")
    col4.info(f"**Set B:** `{sorted(set_b)}`")

    st.markdown("---")
    operasi = st.selectbox(
        "Pilih Operasi:",
        ["Union (A ∪ B)", "Intersection (A ∩ B)", "Difference (A - B)", "Symmetric Difference (A △ B)"]
    )

    # Hitung hasil & tentukan warna diagram
    if operasi == "Union (A ∪ B)":
        hasil   = set_a | set_b
        desc    = "**Union** menggabungkan semua anggota Set A dan Set B."
        wa, wb, wab = "#4C9BE8", "#4C9BE8", "#4C9BE8"
    elif operasi == "Intersection (A ∩ B)":
        hasil   = set_a & set_b
        desc    = "**Intersection** mencari anggota yang ada di Set A **dan** Set B sekaligus."
        wa, wb, wab = "white", "white", "#4C9BE8"
    elif operasi == "Difference (A - B)":
        hasil   = set_a - set_b
        desc    = "**Difference** mencari anggota yang ada di Set A tetapi **tidak** ada di Set B."
        wa, wb, wab = "#4C9BE8", "white", "white"
    else:
        hasil   = set_a ^ set_b
        desc    = "**Symmetric Difference** mencari anggota yang ada di A atau B, tetapi **tidak** di keduanya."
        wa, wb, wab = "#4C9BE8", "#4C9BE8", "white"

    st.info(desc)
    st.success(f"**Hasil:** `{sorted(hasil)}`")

    # ── Diagram Venn ─────────────────────────────────────────
    st.subheader("📊 Diagram Venn")
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor("#F5F7FA")

    # Lingkaran dasar
    ca = Circle((3.5, 3), 2.2, color=wa, alpha=0.55, zorder=2)
    cb = Circle((6.5, 3), 2.2, color=wb, alpha=0.55, zorder=2)
    ax.add_patch(ca)
    ax.add_patch(cb)

    # Irisan (clipping)
    if wab != "white":
        clip_b = Circle((6.5, 3), 2.2, transform=ax.transData)
        clip_a = Circle((3.5, 3), 2.2, transform=ax.transData)
        p1 = Circle((3.5, 3), 2.2, color=wab, alpha=0.7, zorder=3)
        p2 = Circle((6.5, 3), 2.2, color=wab, alpha=0.7, zorder=3)
        p1.set_clip_path(clip_b)
        p2.set_clip_path(clip_a)
        ax.add_patch(p1)
        ax.add_patch(p2)

    # Border
    ax.add_patch(Circle((3.5, 3), 2.2, fill=False, edgecolor="#1a5fb4", linewidth=2.5, zorder=5))
    ax.add_patch(Circle((6.5, 3), 2.2, fill=False, edgecolor="#1a5fb4", linewidth=2.5, zorder=5))

    # Label A / B
    ax.text(2.2, 3, "A", fontsize=22, fontweight="bold", ha="center", va="center",
            color="#1a3a6b", zorder=6)
    ax.text(7.8, 3, "B", fontsize=22, fontweight="bold", ha="center", va="center",
            color="#1a3a6b", zorder=6)

    # Judul di atas diagram
    ax.text(5.0, 5.6, operasi, fontsize=12, ha="center", va="center",
            color="#333", style="italic", fontweight="bold")

    # Anggota tiap zona
    only_a  = sorted(set_a - set_b)
    both_ab = sorted(set_a & set_b)
    only_b  = sorted(set_b - set_a)

    ax.text(2.3, 2.7, "\n".join(str(x) for x in only_a[:6]),
            fontsize=10, ha="center", va="center", color="#1a3a6b", zorder=7)
    ax.text(5.0, 2.7, "\n".join(str(x) for x in both_ab[:6]),
            fontsize=10, ha="center", va="center", color="#1a3a6b", zorder=7)
    ax.text(7.7, 2.7, "\n".join(str(x) for x in only_b[:6]),
            fontsize=10, ha="center", va="center", color="#1a3a6b", zorder=7)

    st.pyplot(fig)

    # ── Detail anggota ────────────────────────────────────────
    st.markdown("---")
    st.subheader("📋 Detail Anggota")
    d1, d2, d3 = st.columns(3)
    with d1:
        st.markdown("**Hanya di A**")
        st.write(sorted(set_a - set_b) or "–")
    with d2:
        st.markdown("**A ∩ B (irisan)**")
        st.write(sorted(set_a & set_b) or "–")
    with d3:
        st.markdown("**Hanya di B**")
        st.write(sorted(set_b - set_a) or "–")

    # ── Kode Python ──────────────────────────────────────────
    with st.expander("🐍 Lihat kode Python operasi ini"):
        kode_map = {
            "Union (A ∪ B)":                   "hasil = set_a | set_b\n# atau\nhasil = set_a.union(set_b)",
            "Intersection (A ∩ B)":            "hasil = set_a & set_b\n# atau\nhasil = set_a.intersection(set_b)",
            "Difference (A - B)":              "hasil = set_a - set_b\n# atau\nhasil = set_a.difference(set_b)",
            "Symmetric Difference (A △ B)":    "hasil = set_a ^ set_b\n# atau\nhasil = set_a.symmetric_difference(set_b)",
        }
        st.code(f"set_a = {set(set_a)}\nset_b = {set(set_b)}\n\n{kode_map[operasi]}\nprint(hasil)  # {sorted(hasil)}", language="python")


# ════════════════════════════════════════════════════════════
# TAB 2 – WORD COUNT
# ════════════════════════════════════════════════════════════
with tab2:
    st.header("Word Count Komentar Sosial Media")
    st.caption("Key = kata | Value = frekuensi kemunculan")

    STOP_WORDS = {
        "yang", "dan", "di", "ke", "dari", "ini", "itu", "dengan", "untuk",
        "adalah", "ada", "atau", "juga", "tidak", "sudah", "akan", "bisa",
        "pada", "aku", "kamu", "dia", "kami", "mereka", "saya", "kita",
        "ya", "oh", "si", "nya", "lah", "kan", "deh", "sih", "nih", "dong",
        "the", "a", "an", "is", "in", "of", "to", "and", "i", "it", "be",
        "sangat", "lebih", "tapi", "jadi", "kalau", "banget"
    }

    contoh = """Produk ini sangat bagus dan berkualitas tinggi
Pengiriman cepat dan packaging aman, sangat puas
Barang bagus tapi pengiriman lambat, semoga bisa lebih cepat
Kualitas produk sesuai deskripsi, sangat recommended
Seller responsif dan barang sampai dengan aman
Produk bagus harga terjangkau, pasti beli lagi
Pengiriman super cepat, barang aman dan berkualitas
Sangat puas dengan produk ini, kualitas terbaik
Barang sesuai foto, packaging aman dan seller ramah
Produk recommended banget, harga murah kualitas bagus"""

    komentar_input = st.text_area(
        "Masukkan komentar (satu per baris):",
        value=contoh,
        height=210
    )

    w1, w2 = st.columns(2)
    with w1:
        top_n = st.slider("Tampilkan Top N kata:", 5, 30, 10, key="topn")
    with w2:
        hapus_sw = st.checkbox("Hapus stop words", value=True, key="sw")

    st.markdown("---")

    if st.button("🔍 Analisis Komentar", use_container_width=True):

        teks   = komentar_input.lower()
        words  = re.findall(r'\b[a-zA-Z]+\b', teks)

        if hapus_sw:
            words = [w for w in words if w not in STOP_WORDS]

        # ── Bangun dictionary secara manual ──────────────────
        word_count: dict = {}
        for w in words:
            word_count[w] = word_count.get(w, 0) + 1

        if not word_count:
            st.warning("Tidak ada kata yang ditemukan.")
            st.stop()

        top_items = sorted(word_count.items(), key=lambda x: x[1], reverse=True)[:top_n]
        kata_top  = [i[0] for i in top_items]
        freq_top  = [i[1] for i in top_items]

        # ── Statistik ─────────────────────────────────────────
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Kata", len(words))
        m2.metric("Kata Unik", len(word_count))
        m3.metric("Kata Terbanyak", f"{kata_top[0]} ({freq_top[0]}x)")

        st.markdown("---")

        # ── Bar chart ─────────────────────────────────────────
        st.subheader(f"📈 Top {top_n} Kata Terbanyak")
        fig2, ax2 = plt.subplots(figsize=(9, 5))
        fig2.patch.set_facecolor("#F5F7FA")
        ax2.set_facecolor("#F5F7FA")

        colors = plt.cm.Blues(
            [0.35 + 0.65 * (freq_top[i] / max(freq_top)) for i in range(len(freq_top))]
        )[::-1]

        bars = ax2.barh(kata_top[::-1], freq_top[::-1], color=colors,
                        edgecolor="white", linewidth=0.8)

        for bar, freq in zip(bars, freq_top[::-1]):
            ax2.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height() / 2,
                     str(freq), va="center", fontsize=10, color="#333")

        ax2.set_xlabel("Frekuensi", fontsize=11)
        ax2.set_title(f"Top {top_n} Kata dalam Komentar Sosial Media",
                      fontsize=13, fontweight="bold", pad=12)
        ax2.spines[["top", "right", "left"]].set_visible(False)
        ax2.xaxis.grid(True, linestyle="--", alpha=0.4)
        ax2.set_axisbelow(True)
        plt.tight_layout()
        st.pyplot(fig2)

        # ── Tabel dictionary ──────────────────────────────────
        st.markdown("---")
        st.subheader("📚 Dictionary Word Count")
        df = pd.DataFrame(top_items, columns=["Kata (Key)", "Frekuensi (Value)"])
        df.index = df.index + 1
        st.dataframe(df, use_container_width=True)

        # ── Representasi kode ─────────────────────────────────
        with st.expander("🐍 Lihat representasi dictionary"):
            st.code(
                "word_count = {\n" +
                "\n".join(f'    "{k}": {v},' for k, v in top_items) +
                "\n    ...\n}",
                language="python"
            )
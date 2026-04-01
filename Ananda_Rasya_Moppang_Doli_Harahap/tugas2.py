import streamlit as st
import matplotlib.pyplot as plt
import re
from collections import Counter

st.set_page_config(page_title="Word Count Komentar Sosmed", layout="centered")

st.title("💬 Word Count Komentar Sosial Media")
st.markdown("Visualisasi frekuensi kata menggunakan **Dictionary** (Key = kata, Value = frekuensi)")
st.markdown("---")

# ── Stop words sederhana ────────────────────────────────────
STOP_WORDS = {
    "yang", "dan", "di", "ke", "dari", "ini", "itu", "dengan", "untuk",
    "adalah", "ada", "atau", "juga", "tidak", "sudah", "akan", "bisa",
    "pada", "aku", "kamu", "dia", "kami", "mereka", "saya", "kita",
    "ya", "oh", "si", "nya", "lah", "kan", "deh", "sih", "nih", "dong",
    "the", "a", "an", "is", "in", "of", "to", "and", "i", "it", "be"
}

# ── Contoh komentar default ─────────────────────────────────
contoh_komentar = """Produk ini sangat bagus dan berkualitas tinggi
Pengiriman cepat dan packaging aman, sangat puas
Barang bagus tapi pengiriman lambat, semoga bisa lebih cepat
Kualitas produk sesuai deskripsi, sangat recommended
Seller responsif dan barang sampai dengan aman
Produk bagus harga terjangkau, pasti beli lagi
Pengiriman super cepat, barang aman dan berkualitas
Sangat puas dengan produk ini, kualitas terbaik
Barang sesuai foto, packaging aman dan seller ramah
Produk recommended banget, harga murah kualitas bagus"""

# ── Input ───────────────────────────────────────────────────
st.subheader("📝 Input Komentar")
komentar_input = st.text_area(
    "Masukkan komentar (satu komentar per baris):",
    value=contoh_komentar,
    height=200
)

col_a, col_b = st.columns(2)
with col_a:
    top_n = st.slider("Tampilkan Top N kata:", min_value=5, max_value=30, value=10)
with col_b:
    hapus_stopword = st.checkbox("Hapus stop words", value=True)

st.markdown("---")

if st.button("🔍 Analisis Komentar", use_container_width=True):

    # ── Proses teks ─────────────────────────────────────────
    teks_gabung = komentar_input.lower()
    kata_list   = re.findall(r'\b[a-zA-Z]+\b', teks_gabung)

    if hapus_stopword:
        kata_list = [k for k in kata_list if k not in STOP_WORDS]

    # ── Dictionary word count ────────────────────────────────
    word_count: dict = {}
    for kata in kata_list:
        if kata in word_count:
            word_count[kata] += 1
        else:
            word_count[kata] = 1

    if not word_count:
        st.warning("Tidak ada kata yang ditemukan. Coba ubah input komentar.")
        st.stop()

    # Urutkan & ambil top N
    top_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)[:top_n]
    kata_top  = [item[0] for item in top_words]
    freq_top  = [item[1] for item in top_words]

    # ── Statistik ringkas ────────────────────────────────────
    st.subheader("📊 Statistik")
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Kata", len(kata_list))
    c2.metric("Kata Unik", len(word_count))
    c3.metric("Kata Terbanyak", f"{kata_top[0]} ({freq_top[0]}x)")

    st.markdown("---")

    # ── Bar chart ────────────────────────────────────────────
    st.subheader(f"📈 Top {top_n} Kata Terbanyak")

    fig, ax = plt.subplots(figsize=(9, 5))
    fig.patch.set_facecolor("#F5F5F5")
    ax.set_facecolor("#F5F5F5")

    colors = plt.cm.Blues(
        [0.4 + 0.6 * (freq_top[i] / max(freq_top)) for i in range(len(freq_top))]
    )[::-1]

    bars = ax.barh(kata_top[::-1], freq_top[::-1], color=colors, edgecolor="white",
                   linewidth=0.8)

    for bar, freq in zip(bars, freq_top[::-1]):
        ax.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height() / 2,
                str(freq), va="center", fontsize=10, color="#333")

    ax.set_xlabel("Frekuensi", fontsize=11)
    ax.set_title(f"Top {top_n} Kata dalam Komentar Sosial Media", fontsize=13,
                 fontweight="bold", pad=12)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.xaxis.grid(True, linestyle="--", alpha=0.4)
    ax.set_axisbelow(True)
    plt.tight_layout()

    st.pyplot(fig)

    # ── Dictionary hasil ─────────────────────────────────────
    st.markdown("---")
    st.subheader("📚 Dictionary Word Count (Key → Value)")
    st.caption("Menampilkan dictionary: {kata: frekuensi}")

    # Tampilkan sebagai tabel
    import pandas as pd
    df = pd.DataFrame(top_words, columns=["Kata (Key)", "Frekuensi (Value)"])
    df.index = df.index + 1
    st.dataframe(df, use_container_width=True)

    st.code(
        "word_count = {\n" +
        "\n".join(f'    "{k}": {v},' for k, v in top_words) +
        "\n    ...\n}",
        language="python"
    )
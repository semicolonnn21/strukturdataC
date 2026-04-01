import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Circle
import numpy as np

st.set_page_config(page_title="Visualisasi Operasi Set", layout="centered")

st.title("🔵 Visualisasi Operasi Set")
st.markdown("---")

# ── Input Set ──────────────────────────────────────────────
st.subheader("📥 Input Set")

col1, col2 = st.columns(2)
with col1:
    input_a = st.text_input("Set A (pisahkan dengan koma)", value="1, 2, 3, 4, 5")
with col2:
    input_b = st.text_input("Set B (pisahkan dengan koma)", value="4, 5, 6, 7, 8")

def parse_set(text):
    try:
        return set(int(x.strip()) for x in text.split(",") if x.strip())
    except ValueError:
        return set(x.strip() for x in text.split(",") if x.strip())

set_a = parse_set(input_a)
set_b = parse_set(input_b)

st.write(f"**Set A:** `{sorted(set_a)}`")
st.write(f"**Set B:** `{sorted(set_b)}`")

st.markdown("---")

# ── Pilih Operasi ───────────────────────────────────────────
st.subheader("⚙️ Pilih Operasi")

operasi = st.selectbox(
    "Operasi Set:",
    ["Union (A ∪ B)", "Intersection (A ∩ B)", "Difference (A - B)", "Symmetric Difference (A △ B)"]
)

# ── Hitung Hasil ────────────────────────────────────────────
if operasi == "Union (A ∪ B)":
    hasil = set_a | set_b
    deskripsi = "**Union** menggabungkan semua anggota dari Set A dan Set B."
    warna_a   = "#4C9BE8"
    warna_b   = "#4C9BE8"
    warna_ab  = "#4C9BE8"
elif operasi == "Intersection (A ∩ B)":
    hasil = set_a & set_b
    deskripsi = "**Intersection** mencari anggota yang ada di Set A **dan** Set B sekaligus."
    warna_a   = "white"
    warna_b   = "white"
    warna_ab  = "#4C9BE8"
elif operasi == "Difference (A - B)":
    hasil = set_a - set_b
    deskripsi = "**Difference** mencari anggota yang ada di Set A tetapi **tidak** ada di Set B."
    warna_a   = "#4C9BE8"
    warna_b   = "white"
    warna_ab  = "white"
else:
    hasil = set_a ^ set_b
    deskripsi = "**Symmetric Difference** mencari anggota yang ada di A atau B, tetapi **tidak** di keduanya."
    warna_a   = "#4C9BE8"
    warna_b   = "#4C9BE8"
    warna_ab  = "white"

st.info(deskripsi)
st.success(f"**Hasil:** `{sorted(hasil)}`")

# ── Diagram Venn ────────────────────────────────────────────
st.subheader("📊 Diagram Venn")

fig, ax = plt.subplots(figsize=(7, 4))
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.set_aspect("equal")
ax.axis("off")
fig.patch.set_facecolor("#F5F5F5")

circle_a = Circle((3.5, 3), 2.2, color=warna_a, alpha=0.6, zorder=2)
circle_b = Circle((6.5, 3), 2.2, color=warna_b, alpha=0.6, zorder=2)
ax.add_patch(circle_a)
ax.add_patch(circle_b)

# Irisan (gambar ulang dengan warna khusus agar bisa di-overlap)
theta = np.linspace(0, 2 * np.pi, 300)
# Buat path irisan sederhana via clip
from matplotlib.patches import PathPatch
from matplotlib.path import Path

circle_a2 = Circle((3.5, 3), 2.2, color=warna_ab, alpha=0.7, zorder=3)
circle_b2 = Circle((6.5, 3), 2.2, color=warna_ab, alpha=0.7, zorder=3)

# Clip A ke lingkaran B dan sebaliknya untuk irisan
from matplotlib.patches import Circle as MplCircle
import matplotlib.transforms as transforms

# Cara sederhana: gambar irisan dengan patch terpisah di atas
if warna_ab != "white":
    patch_ab_a = Circle((3.5, 3), 2.2, color=warna_ab, alpha=0.7, zorder=3)
    patch_ab_b = Circle((6.5, 3), 2.2, color=warna_ab, alpha=0.7, zorder=3)
    # Clip B ke dalam A untuk irisan
    clip_a = Circle((3.5, 3), 2.2, transform=ax.transData)
    clip_b = Circle((6.5, 3), 2.2, transform=ax.transData)
    patch_ab_a.set_clip_path(clip_b)
    patch_ab_b.set_clip_path(clip_a)
    ax.add_patch(patch_ab_a)
    ax.add_patch(patch_ab_b)

# Border
border_a = Circle((3.5, 3), 2.2, fill=False, edgecolor="#1a5fb4", linewidth=2, zorder=5)
border_b = Circle((6.5, 3), 2.2, fill=False, edgecolor="#1a5fb4", linewidth=2, zorder=5)
ax.add_patch(border_a)
ax.add_patch(border_b)

# Label
ax.text(2.5, 3, "A", fontsize=18, fontweight="bold", ha="center", va="center",
        color="#1a3a6b", zorder=6)
ax.text(7.5, 3, "B", fontsize=18, fontweight="bold", ha="center", va="center",
        color="#1a3a6b", zorder=6)
ax.text(5.0, 5.5, operasi, fontsize=11, ha="center", va="center",
        color="#333333", style="italic")

# Anggota di tiap zona
only_a  = sorted(set_a - set_b)
both_ab = sorted(set_a & set_b)
only_b  = sorted(set_b - set_a)

ax.text(2.5, 2.5, "\n".join(str(x) for x in only_a[:5]),
        fontsize=9, ha="center", va="center", color="#1a3a6b", zorder=7)
ax.text(5.0, 2.5, "\n".join(str(x) for x in both_ab[:5]),
        fontsize=9, ha="center", va="center", color="#1a3a6b", zorder=7)
ax.text(7.5, 2.5, "\n".join(str(x) for x in only_b[:5]),
        fontsize=9, ha="center", va="center", color="#1a3a6b", zorder=7)

st.pyplot(fig)

# ── Detail ──────────────────────────────────────────────────
st.markdown("---")
st.subheader("📋 Detail Anggota")

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("**Hanya di A**")
    st.write(sorted(set_a - set_b) or "-")
with c2:
    st.markdown("**A ∩ B (irisan)**")
    st.write(sorted(set_a & set_b) or "-")
with c3:
    st.markdown("**Hanya di B**")
    st.write(sorted(set_b - set_a) or "-")
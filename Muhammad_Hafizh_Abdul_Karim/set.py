import streamlit as st
import matplotlib.pyplot as plt
from matplotlib_venn import venn2

st.set_page_config(page_title="Visualisasi Set - Struktur Data")
st.title("🔵 Operasi Set (Elemen Terlihat)")

# Input User
st.info("Masukkan elemen dipisahkan dengan koma (contoh: a, b, c atau 1, 2, 3)")
col1, col2 = st.columns(2)
with col1:
    raw_a = st.text_input("Input Set A:", )
with col2:
    raw_b = st.text_input("Input Set B:", )

# Proses Set
set_a = set([x.strip() for x in raw_a.split(",") if x.strip()])
set_b = set([x.strip() for x in raw_b.split(",") if x.strip()])

operasi = st.selectbox("Pilih Operasi:", 
                      ["Union", "Intersection", "Difference (A-B)", "Symmetric Difference"])

# Logika
if operasi == "Union":
    hasil = set_a | set_b
elif operasi == "Intersection":
    hasil = set_a & set_b
elif operasi == "Difference (A-B)":
    hasil = set_a - set_b
else:
    hasil = set_a ^ set_b

st.success(f"**Hasil {operasi}:** `{hasil if hasil else 'Set Kosong'}`")

# VISUALISASI DENGAN LABEL ELEMEN
st.subheader("📊 Visualisasi Diagram Venn")
if set_a or set_b:
    fig, ax = plt.subplots(figsize=(8, 5))
    v = venn2([set_a, set_b], set_labels=('Set A', 'Set B'))

    # Fungsi untuk mengubah angka (count) menjadi isi data (elements)
    # id '10' = A saja, '01' = B saja, '11' = Irisan
    labels = {
        '10': set_a - set_b,
        '01': set_b - set_a,
        '11': set_a & set_b
    }

    for idx, data in labels.items():
        if v.get_label_by_id(idx):
            # Menggabungkan isi set menjadi string "1, 3" dst
            isi_teks = ", ".join(sorted(list(data))) if data else ""
            v.get_label_by_id(idx).set_text(isi_teks)

    plt.title(f"Diagram Venn: {operasi}")
    st.pyplot(fig)
else:
    st.warning("Silakan isi data terlebih dahulu.")
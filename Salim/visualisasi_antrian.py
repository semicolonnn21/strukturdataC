import streamlit as st

st.title("🔄 Simple Circular Queue")

# Inisialisasi antrean (kapasitas 8)
if 'queue' not in st.session_state:
    st.session_state.queue = [None] * 8
    st.session_state.head = -1
    st.session_state.tail = -1

q = st.session_state # Shortcut

# UI Kontrol
data = st.text_input("Masukan 4 karakter:")
col1, col2 = st.columns(2)

# Logika Enqueue (Tambah)
if col1.button("Tambah antrean"):
    if ((q.tail + 1) % 8 == q.head):
        st.error("Antrean Penuh!")
    else:
        if q.head == -1: q.head = 0
        q.tail = (q.tail + 1) % 8
        q.queue[q.tail] = data
        st.rerun()

# Logika Dequeue (Hapus)
if col2.button("Hapus antrean"):
    if q.head == -1:
        st.error("Antrean Kosong!")
    else:
        q.queue[q.head] = None
        if q.head == q.tail:
            q.head = q.tail = -1
        else:
            q.head = (q.head + 1) % 8
        st.rerun()

# Visualisasi Grid Sederhana
st.write("### Antrean:")
cols = st.columns(8)
for i in range(8):
    # Tandai posisi Head dan Tail
    label = "⚪"
    if i == q.head: label = "🟢 Head"
    if i == q.tail: label = "🔵 Tail"
    if i == q.head == q.tail and q.head != -1: label = "🎯 Both"

    cols[i].metric(label, f"{q.queue[i] if q.queue[i] else '-'}")

if st.button("Reset"):
    st.session_state.clear()
    st.rerun()
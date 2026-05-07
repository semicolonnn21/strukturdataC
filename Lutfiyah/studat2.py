import streamlit as st

# 1. INISIALISASI (Buat variabel untuk menyimpan data antrian)
if 'queue' not in st.session_state:
    st.session_state.size = 5
    st.session_state.queue = [None] * st.session_state.size
    st.session_state.front = -1
    st.session_state.rear = -1

st.title("Circular Queue Visualization")

# 2. FUNGSI UNTUK ENQUEUE DAN DEQUEUE
def tambah_data(item):
    s = st.session_state
    # Cek apakah penuh
    if (s.rear + 1) % s.size == s.front:
        st.warning("Antrian sudah penuh!")
    else:
        if s.front == -1: s.front = 0
        s.rear = (s.rear + 1) % s.size
        s.queue[s.rear] = item

def hapus_data():
    s = st.session_state
    if s.front == -1:
        st.warning("Antrian kosong!")
    else:
        s.queue[s.front] = None # Hapus datanya
        if s.front == s.rear: # Jika data terakhir habis
            s.front = -1
            s.rear = -1
        else:
            s.front = (s.front + 1) % s.size

# 3. INTERAKSI USER
menu_tambah = st.text_input("Ketik data:")
col1, col2 = st.columns(2)
if col1.button("Tambah (Enqueue)"):
    if menu_tambah: tambah_data(menu_tambah)

if col2.button("Hapus (Dequeue)"):
    hapus_data()

# 4. VISUALISASI 
st.write("### Kondisi antrian saat ini:")
cols = st.columns(st.session_state.size)
for i in range(st.session_state.size):
    with cols[i]:
        label = ""
        if i == st.session_state.front: label += "🔴F"
        if i == st.session_state.rear: label += "🔵R"
        
        st.code(f"{st.session_state.queue[i]}\n{label}")

st.sidebar.write(f"Front Index: {st.session_state.front}")
st.sidebar.write(f"Rear Index: {st.session_state.rear}")
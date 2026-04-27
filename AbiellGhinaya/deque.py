import streamlit as st

st.set_page_config(page_title="Project Circular queue 🎡", layout="wide")
st.title("Circular Queue Dinamis 🎡")
st.write("Menggunakan Circular queue")
st.caption("***Untuk memenuhi Tugas Mata kuliah: Struktur Data😁***")

st.divider()
col_nama, col_nim, col_mk, col_class = st.columns(4)
with col_nama:
    st.write("**Nama:** Abil Ghinaya Azka")
with col_nim:
    st.write("**NIM:** 2530801056")
with col_mk:
    st.write("**Mata kuliah:** Struktur Data")
with col_class:
    st.write("**Kelas:** II C")
st.divider()

# Input untuk menentukan MAX_SIZE
# Kita simpan di variabel agar bisa digunakan sebagai batas
new_max_size = st.number_input(
    label="Tentukan Kapasitas Antrean:", 
    min_value=2, 
    max_value=10, 
    value=5, 
    step=1
)

# Inisialisasi data
# Kita cek apakah 'queue' belum ada atau ukurannya berbeda dengan input terbaru
if ('queue' not in st.session_state) or (len(st.session_state.queue) != new_max_size):
    st.session_state.queue = [None] * new_max_size
    st.session_state.head = -1
    st.session_state.tail = -1
    st.info(f"Antrean diatur ulang ke kapasitas {new_max_size}")

# Simpan ukuran saat ini ke variabel lokal
current_max = len(st.session_state.queue)

# --- Sama kek biasa yhaaa min ---

def enqueue(nama):
    if ((st.session_state.tail + 1) % current_max == st.session_state.head):
        st.error("Antrean Penuh!")
    else:
        if st.session_state.head == -1:
            st.session_state.head = 0
        st.session_state.tail = (st.session_state.tail + 1) % current_max
        st.session_state.queue[st.session_state.tail] = nama

def dequeue():
    if st.session_state.head == -1:
        st.warning("Antrean Kosong!")
    else:
        nama = st.session_state.queue[st.session_state.head]
        st.session_state.queue[st.session_state.head] = None
        if st.session_state.head == st.session_state.tail:
            st.session_state.head = -1
            st.session_state.tail = -1
        else:
            st.session_state.head = (st.session_state.head + 1) % current_max

# Tampilan Tombol
nama_input = st.text_input("Nama Tamu:")
c1, c2 = st.columns(2)
with c1:
    if st.button("Tambah"): enqueue(nama_input)
with c2:
    if st.button("Hapus"): dequeue()

st.write("### Kondisi Kursi:")
st.write(st.session_state.queue)
st.write(f"Front: {st.session_state.head} | Rear: {st.session_state.tail}")
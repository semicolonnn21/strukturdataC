import streamlit as st

# Judul dengan Nama Nona Cantik
st.title("Sistem Visualisasi Circular Queue")
st.subheader("Oleh: Cindy Amelia")

# Inisialisasi State (Agar data tidak hilang saat refresh)
MAX_SIZE = 5

if 'queue' not in st.session_state:
    st.session_state.queue = [None] * MAX_SIZE
    st.session_state.front = -1
    st.session_state.rear = -1

def enqueue(item):
    # Cek apakah penuh
    if ((st.session_state.rear + 1) % MAX_SIZE == st.session_state.front):
        st.error("Antrian Penuh! Wah, harus ada yang keluar dulu nih.")
    else:
        if st.session_state.front == -1:
            st.session_state.front = 0
        
        st.session_state.rear = (st.session_state.rear + 1) % MAX_SIZE
        st.session_state.queue[st.session_state.rear] = item
        st.success(f"Berhasil menambah '{item}' ke antrian.")

def dequeue():
    # Cek apakah kosong
    if st.session_state.front == -1:
        st.warning("Antriannya kosong, Nona Cantik!")
    else:
        item = st.session_state.queue[st.session_state.front]
        st.session_state.queue[st.session_state.front] = None
        
        # Jika elemen terakhir diambil
        if st.session_state.front == st.session_state.rear:
            st.session_state.front = -1
            st.session_state.rear = -1
        else:
            st.session_state.front = (st.session_state.front + 1) % MAX_SIZE
        st.info(f"Elemen '{item}' telah keluar dari antrian.")

# --- Bagian Input ---
col1, col2 = st.columns(2)

with col1:
    input_data = st.text_input("Masukkan Nama/Data:")
    if st.button("Tambah ke Antrian (Enqueue)"):
        if input_data:
            enqueue(input_data)
        else:
            st.warning("Isi dulu datanya ya!")

with col2:
    st.write("Aksi Keluar:")
    if st.button("Hapus dari Antrian (Dequeue)"):
        dequeue()

# --- Visualisasi Antrian ---
st.write("---")
st.write("### Visualisasi Slot Antrian")

cols = st.columns(MAX_SIZE)
for i in range(MAX_SIZE):
    with cols[i]:
        val = st.session_state.queue[i]
        label = "KOSONG" if val is None else val
        
        # Memberi warna khusus untuk Front dan Rear
        status = ""
        if i == st.session_state.front: status += "🔵 [FRONT]"
        if i == st.session_state.rear: status += "🔴 [REAR]"
        
        st.metric(label=f"Indeks {i}", value=label, delta=status)

st.write("---")
st.info(f"Catatan: Indeks akan melingkar kembali ke 0 jika mencapai indeks {MAX_SIZE-1}")



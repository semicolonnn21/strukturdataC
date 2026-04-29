import streamlit as st

st.set_page_config(page_title="Circular Queue Visualizer", layout="wide")

# Inisialisasi State (Biar data nggak ilang pas diklik)
if 'queue' not in st.session_state:
    st.session_state.max_size = 8
    st.session_state.queue = [None] * st.session_state.max_size
    st.session_state.f = -1 # Pake f biar simpel (Front)
    st.session_state.r = -1 # Pake r biar simpel (Rear)

# Fungsi Tambah Data
def tambah_data(item):
    n = st.session_state.max_size
    # Cek kondisi penuh
    if (st.session_state.r + 1) % n == st.session_state.f:
        st.error("Waduh, antrean udah penuh nih!")
    else:
        if st.session_state.f == -1:
            st.session_state.f = 0
        
        st.session_state.r = (st.session_state.r + 1) % n
        st.session_state.queue[st.session_state.r] = item
        st.toast(f"{item} berhasil masuk antrean")

# Fungsi Hapus Data
def hapus_data():
    n = st.session_state.max_size
    # Cek kondisi kosong
    if st.session_state.f == -1:
        st.warning("Antrean masih kosong, apa yang mau dihapus?")
    else:
        item = st.session_state.queue[st.session_state.f]
        st.session_state.queue[st.session_state.f] = None
        
        # Reset kalau data terakhir diambil
        if st.session_state.f == st.session_state.r:
            st.session_state.f = -1
            st.session_state.r = -1
        else:
            st.session_state.f = (st.session_state.f + 1) % n
        st.toast(f"{item} sudah keluar")

# --- Tampilan Header ---
st.title("🔄 Visualiasi Circular Queue")
st.caption("Tugas Struktur Data - Hafidzar Ashyawal Sinatryas")
st.divider()

# Layout Kontrol
with st.sidebar:
    st.header("Kontrol Antrean")
    txt_input = st.text_input("Input Data", placeholder="Ketik sesuatu...")
    
    col1, col2 = st.columns(2)
    if col1.button("Enqueue", use_container_width=True):
        if txt_input:
            tambah_data(txt_input)
            
    if col2.button("Dequeue", use_container_width=True):
        hapus_data()

# Data Pasien
st.subheader("Data Pasien")
grid = st.columns(st.session_state.max_size)

for i in range(st.session_state.max_size):
    with grid[i]:
        # Penanda posisi Front dan Rear
        posisi = ""
        if i == st.session_state.f: posisi += " 🏁 F"
        if i == st.session_state.r: posisi += " 📦 R"
        
        isi = st.session_state.queue[i]
        
        # Tampilan box per indeks
        container = st.container(border=True)
        container.write(f"**[{i}]**")
        container.subheader(isi if isi else "-")
        st.caption(posisi)

# Info Debugging (di bawah biar rapi)
st.write("")
with st.expander("Lihat Status Pointer"):
    st.code(f"Front Index: {st.session_state.f}\nRear Index: {st.session_state.r}")
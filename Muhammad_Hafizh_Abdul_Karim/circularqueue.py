import streamlit as st

# Konfigurasi Halaman
st.set_page_config(page_title="Visualisasi Circular Queue", layout="centered")

st.title("🔄 Visualisasi Circular Queue")
st.write("Implementasi konsep *wrap-around* menggunakan Streamlit.")

# 1. Inisialisasi State Antrean
MAX_SIZE = 8  # Sesuai gambar pada tugas Anda (indeks 0-7)

if 'queue' not in st.session_state:
    st.session_state.queue = [None] * MAX_SIZE
    st.session_state.front = -1
    st.session_state.rear = -1

# Fungsi Logika Circular Queue
def enqueue(data):
    if (st.session_state.rear + 1) % MAX_SIZE == st.session_state.front:
        st.error("Queue Penuh! (Overflow)")
    else:
        if st.session_state.front == -1:
            st.session_state.front = 0
        st.session_state.rear = (st.session_state.rear + 1) % MAX_SIZE
        st.session_state.queue[st.session_state.rear] = data
        st.success(f"Berhasil menambahkan: {data}")

def dequeue():
    if st.session_state.front == -1:
        st.warning("Queue Kosong! (Underflow)")
    else:
        removed_item = st.session_state.queue[st.session_state.front]
        st.session_state.queue[st.session_state.front] = None
        
        if st.session_state.front == st.session_state.rear:
            st.session_state.front = -1
            st.session_state.rear = -1
        else:
            st.session_state.front = (st.session_state.front + 1) % MAX_SIZE
        st.info(f"Berhasil menghapus: {removed_item}")

# 2. Sidebar untuk Kontrol
st.sidebar.header("Kontrol Antrean")
input_data = st.sidebar.text_input("Masukkan Data:")
col1, col2 = st.sidebar.columns(2)

if col1.button("Enqueue (Tambah)"):
    if input_data:
        enqueue(input_data)
    else:
        st.sidebar.error("Isi data dulu!")

if col2.button("Dequeue (Hapus)"):
    dequeue()

if st.sidebar.button("Reset Queue"):
    st.session_state.queue = [None] * MAX_SIZE
    st.session_state.front = -1
    st.session_state.rear = -1
    st.rerun()

# 3. Visualisasi
st.subheader("Status Antrean Saat Ini")

# Membuat kolom untuk merepresentasikan slot memori
cols = st.columns(MAX_SIZE)

for i in range(MAX_SIZE):
    with cols[i]:
        val = st.session_state.queue[i]
        
        # Logika warna dan label
        is_front = (i == st.session_state.front)
        is_rear = (i == st.session_state.rear)
        
        color = "lightblue" if val is not None else "#f0f2f6"
        border = "3px solid #ff4b4b" if (is_front or is_rear) else "1px solid #ddd"
        
        # HTML untuk kotak visualisasi
        st.markdown(
            f"""
            <div style="
                border: {border};
                border-radius: 10px;
                padding: 10px;
                text-align: center;
                background-color: {color};
                min-height: 80px;
            ">
                <p style="margin:0; font-size: 12px; color: gray;">Idx: {i}</p>
                <h4 style="margin:0; color: black;">{val if val is not None else "-"}</h4>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # Penanda Front dan Rear
        if is_front and is_rear:
            st.caption("⬅️ F & R")
        elif is_front:
            st.caption("⬅️ FRONT")
        elif is_rear:
            st.caption("⬅️ REAR")

# 4. Informasi Teknis
st.divider()
st.write(f"**Indeks Front:** `{st.session_state.front}` | **Indeks Rear:** `{st.session_state.rear}`")

with st.expander("Penjelasan Konsep Wrap-Around"):
    st.write("""
    Dalam Circular Queue, ketika `rear` mencapai batas maksimal, ia tidak berhenti tapi 
    kembali ke indeks `0` menggunakan operasi modulo:
    """)
    st.latex(r"Rear = (Rear + 1) \pmod{MaxSize}")
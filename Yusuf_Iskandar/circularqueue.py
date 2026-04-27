import streamlit as st

# Judul aplikasi
st.title("🔄 Visualisasi Circular Queue")
st.markdown("Antrian melingkar dengan kapasitas tetap. Elemen terakhir terhubung kembali ke awal (wrap-around).")

# Inisialisasi session state
if 'capacity' not in st.session_state:
    st.session_state.capacity = 5  # Kapasitas tetap
if 'queue' not in st.session_state:
    st.session_state.queue = [None] * st.session_state.capacity
if 'front' not in st.session_state:
    st.session_state.front = -1
if 'rear' not in st.session_state:
    st.session_state.rear = -1
if 'message' not in st.session_state:
    st.session_state.message = ""

# Fungsi helper
def is_empty():
    return st.session_state.front == -1

def is_full():
    return (st.session_state.rear + 1) % st.session_state.capacity == st.session_state.front

def enqueue(value):
    if is_full():
        st.session_state.message = "❌ Antrian PENUH! Tidak bisa menambah elemen."
        return False
    elif is_empty():
        st.session_state.front = 0
        st.session_state.rear = 0
    else:
        st.session_state.rear = (st.session_state.rear + 1) % st.session_state.capacity
    st.session_state.queue[st.session_state.rear] = value
    st.session_state.message = f"✅ Berhasil menambah: {value}"
    return True

def dequeue():
    if is_empty():
        st.session_state.message = "⚠️ Antrian KOSONG! Tidak bisa menghapus elemen."
        return None
    removed = st.session_state.queue[st.session_state.front]
    st.session_state.queue[st.session_state.front] = None
    if st.session_state.front == st.session_state.rear:
        # Hanya satu elemen
        st.session_state.front = -1
        st.session_state.rear = -1
    else:
        st.session_state.front = (st.session_state.front + 1) % st.session_state.capacity
    st.session_state.message = f"🗑️ Berhasil menghapus: {removed}"
    return removed

def reset():
    st.session_state.queue = [None] * st.session_state.capacity
    st.session_state.front = -1
    st.session_state.rear = -1
    st.session_state.message = "🔄 Antrian telah direset."

# Layout dua kolom untuk kontrol
col1, col2, col3 = st.columns(3)
with col1:
    new_element = st.text_input("Masukkan elemen (string atau angka):", key="input")
    if st.button("➕ Enqueue", use_container_width=True):
        if new_element.strip():
            enqueue(new_element.strip())
        else:
            st.session_state.message = "⚠️ Masukkan nilai terlebih dahulu."
        st.rerun()

with col2:
    if st.button("➖ Dequeue", use_container_width=True):
        dequeue()
        st.rerun()

with col3:
    if st.button("🔄 Reset", use_container_width=True):
        reset()
        st.rerun()

# Tampilkan pesan status
if st.session_state.message:
    st.info(st.session_state.message)

# Visualisasi Circular Queue
st.subheader("📦 Keadaan Antrian Saat Ini")
capacity = st.session_state.capacity
queue = st.session_state.queue
front = st.session_state.front
rear = st.session_state.rear

# Buat kolom untuk setiap slot
cols = st.columns(capacity)
for i in range(capacity):
    with cols[i]:
        # Tentukan warna latar berdasarkan posisi front/rear
        if i == front and i == rear and front != -1:
            bg_color = "#FFD966"  # Kuning jika front dan rear sama
            label = "🚩 Front & Rear"
        elif i == front and front != -1:
            bg_color = "#6AA84F"  # Hijau untuk front
            label = "🚩 Front"
        elif i == rear and rear != -1:
            bg_color = "#3C78D8"  # Biru untuk rear
            label = "📍 Rear"
        else:
            bg_color = "#F0F2F6"
            label = f"Indeks {i}"
        
        value = queue[i] if queue[i] is not None else "—"
        st.markdown(
            f"""
            <div style="
                background-color: {bg_color};
                padding: 20px 0;
                text-align: center;
                border-radius: 12px;
                border: 1px solid #ccc;
                margin: 5px;
                font-weight: bold;
            ">
                <div style="font-size: 24px;">{value}</div>
                <div style="font-size: 12px; color: #555;">{label}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

# Tampilkan informasi front, rear, dan kondisi
st.markdown("---")
col_info1, col_info2, col_info3 = st.columns(3)
with col_info1:
    st.metric("Front Index", front if front != -1 else "—")
with col_info2:
    st.metric("Rear Index", rear if rear != -1 else "—")
with col_info3:
    if is_empty():
        st.metric("Status", "🟢 Kosong")
    elif is_full():
        st.metric("Status", "🔴 Penuh")
    else:
        st.metric("Status", "🟡 Terisi")

# Penjelasan wrap-around
with st.expander("ℹ️ Bagaimana Circular Queue Bekerja?"):
    st.markdown("""
    - **Circular Queue** menghubungkan elemen terakhir kembali ke elemen pertama (wrap-around).
    - Ketika `rear` mencapai batas kapasitas, ia akan kembali ke indeks 0 selama slot tersebut kosong.
    - Operasi **enqueue** menambah elemen di posisi `rear` lalu `rear` bergerak maju.
    - Operasi **dequeue** menghapus elemen di posisi `front` lalu `front` bergerak maju.
    - Antrian dikatakan **penuh** jika `(rear + 1) % capacity == front`.
    - Kondisi **kosong** ditandai dengan `front == -1`.
    """)

# Catatan untuk pengguna
st.caption("💡 Tips: Masukkan angka atau kata. Kapasitas tetap 5 untuk demonstrasi yang mudah dipahami.")
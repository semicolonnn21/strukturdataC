import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Konfigurasi Halaman
st.set_page_config(page_title="Visualisasi Circular Queue", layout="centered")

# Inisialisasi Circular Queue dalam Session State
if 'size' not in st.session_state:
    st.session_state.size = 8
    st.session_state.queue = [None] * st.session_state.size
    st.session_state.head = -1
    st.session_state.tail = -1

def enqueue(data):
    size = st.session_state.size
    # Cek apakah penuh
    if ((st.session_state.tail + 1) % size == st.session_state.head):
        st.error("Queue Penuh (Overflow)!")
    else:
        if st.session_state.head == -1:
            st.session_state.head = 0
        
        st.session_state.tail = (st.session_state.tail + 1) % size
        st.session_state.queue[st.session_state.tail] = data
        st.success(f"Berhasil menambahkan: {data}")

def dequeue():
    size = st.session_state.size
    # Cek apakah kosong
    if st.session_state.head == -1:
        st.error("Queue Kosong (Underflow)!")
    else:
        removed = st.session_state.queue[st.session_state.head]
        st.session_state.queue[st.session_state.head] = None
        
        if st.session_state.head == st.session_state.tail:
            st.session_state.head = -1
            st.session_state.tail = -1
        else:
            st.session_state.head = (st.session_state.head + 1) % size
        st.warning(f"Berhasil menghapus: {removed}")

# --- UI STREAMLIT ---
st.title("🔄 Visualisasi Circular Queue")
st.markdown("Elemen terakhir terhubung kembali ke awal menggunakan konsep **wrap-around**.")

# Sidebar untuk Kontrol
with st.sidebar:
    st.header("Kontrol Antrean")
    val = st.text_input("Input Data (String/Angka)")
    col1, col2 = st.columns(2)
    if col1.button("Enqueue", use_container_width=True):
        if val:
            enqueue(val)
        else:
            st.warning("Isi data dulu!")
            
    if col2.button("Dequeue", use_container_width=True):
        dequeue()
        
    if st.button("Reset Queue"):
        st.session_state.queue = [None] * st.session_state.size
        st.session_state.head = -1
        st.session_state.tail = -1
        st.rerun()

# --- VISUALISASI ---
fig, ax = plt.subplots(figsize=(6, 6))
size = st.session_state.size
indices = np.arange(size)
colors = []

# Tentukan warna tiap slot
for i in range(size):
    if i == st.session_state.head and i == st.session_state.tail:
        colors.append('#ff4b4b') # Head & Tail sama
    elif i == st.session_state.head:
        colors.append('#31333f') # Head
    elif i == st.session_state.tail:
        colors.append('#1c83e1') # Tail
    else:
        colors.append('#f0f2f6')

# Membuat chart donat (Pie Chart dengan lubang di tengah)
wedges, texts = ax.pie(
    [1] * size, 
    labels=indices, 
    colors=colors, 
    startangle=90, 
    counterclock=False,
    wedgeprops={'width': 0.4, 'edgecolor': 'white', 'linewidth': 2}
)

# Menambahkan teks data di dalam setiap segmen
for i, p in enumerate(wedges):
    ang = (p.theta2 - p.theta1)/2. + p.theta1
    y = np.sin(np.deg2rad(ang))
    x = np.cos(np.deg2rad(ang))
    
    val_text = st.session_state.queue[i] if st.session_state.queue[i] is not None else "-"
    ax.text(x*0.8, y*0.8, val_text, ha='center', va='center', fontweight='bold')

plt.title(f"Status: Head={st.session_state.head}, Tail={st.session_state.tail}")

# Tampilkan di Streamlit
st.pyplot(fig)

# Info Legend
st.markdown("""
**Keterangan Warna:**
* ⚪ **Abu-abu Muda**: Slot Kosong.
* ⚫ **Hitam**: Posisi **Head** (Awal).
* 🔵 **Biru**: Posisi **Tail** (Akhir).
* 🔴 **Merah**: Posisi Head & Tail berada di slot yang sama.
""")

# Tampilan Array Linear untuk pembanding
st.write("### Representasi Array:")
st.write(st.session_state.queue)

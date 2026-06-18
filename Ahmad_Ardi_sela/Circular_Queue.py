import streamlit as st

st.set_page_config(page_title="Circular Queue Visualization", layout="wide")
st.title("🔄 Circular Queue Visualization")

# 1. Menyiapkan Variabel (Sesuai gambar, kapasitas antrian = 5)
if 'max_size' not in st.session_state:
    st.session_state.max_size = 5
if 'queue' not in st.session_state:
    st.session_state.queue = ["-"] * 5  # Menggunakan tanda "-" untuk kotak kosong
if 'head' not in st.session_state:
    st.session_state.head = -1
if 'tail' not in st.session_state:
    st.session_state.tail = -1

# 2. Tata Letak Input dan Tombol
col1, col2 = st.columns(2)

with col1:
    item = st.text_input("Input Data")
    tombol_tambah = st.button("Enqueue (Tambah)")

with col2:
    st.write("") # Sekadar spasi agar sejajar
    st.write("")
    tombol_hapus = st.button("Dequeue (Hapus)")

# Logika Tambah Data (Enqueue)
if tombol_tambah:
    # Cek apakah antrian penuh
    if (st.session_state.tail + 1) % st.session_state.max_size == st.session_state.head:
        st.error("Antrian Penuh!")
    elif item:
        if st.session_state.head == -1: 
            st.session_state.head = 0
            
        # Pindahkan tail melingkar
        st.session_state.tail = (st.session_state.tail + 1) % st.session_state.max_size
        st.session_state.queue[st.session_state.tail] = item

# Logika Hapus Data (Dequeue)
if tombol_hapus:
    # Cek apakah antrian kosong
    if st.session_state.head == -1:
        st.error("Antrian Kosong!")
    else:
        st.session_state.queue[st.session_state.head] = "-" # Kembalikan ke kosong
        
        # Jika itu adalah data terakhir di dalam antrian
        if st.session_state.head == st.session_state.tail:  
            st.session_state.head = -1
            st.session_state.tail = -1
        else: 
            # Pindahkan head melingkar
            st.session_state.head = (st.session_state.head + 1) % st.session_state.max_size

# 3. Tampilan Visual (Kotak Berjejer Sesuai Gambar)
st.subheader("Status Antrian Saat Ini:")

# Membuat kolom sejajar sebanyak ukuran antrian
kolom_antrian = st.columns(st.session_state.max_size)

for i in range(st.session_state.max_size):
    with kolom_antrian[i]:
        # Jika kotak kosong warnanya abu-abu, jika ada isinya warnanya biru
        warna_bg = "#0011ff" if st.session_state.queue[i] != "-" else "#8a8a8a"
        
        # Membuat kotak menggunakan HTML/CSS dasar
        desain_kotak = f"""
        <div style="background-color: {warna_bg}; color: white; padding: 30px 10px; 
                    text-align: center; border-radius: 8px; font-size: 20px; 
                    font-weight: bold; border: 2px solid black;">
            {st.session_state.queue[i]}
        </div>
        <div style="text-align: center; margin-top: 10px; font-size: 16px;">
            Index {i}
        </div>
        """
        st.markdown(desain_kotak, unsafe_allow_html=True)
        
        # Menambahkan teks panah HEAD atau TAIL persis di bawah kotaknya
        penanda = ""
        if i == st.session_state.head:
            penanda += "➡️ HEAD<br>"
        if i == st.session_state.tail:
            penanda += "⬅️ TAIL"
            
        if penanda != "":
            st.markdown(f"<div style='text-align: center; font-weight: bold;'>{penanda}</div>", unsafe_allow_html=True)
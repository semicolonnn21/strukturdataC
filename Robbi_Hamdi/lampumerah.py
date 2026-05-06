import streamlit as st
import time


# 1. Definisi Node yang Lengkap
class Node:
    def __init__(self, warna: str, durasi: int):
        self.warna = warna
        self.durasi = durasi
        self.next = None  # Penunjuk ke lampu berikutnya


# 2. Inisialisasi Objek
merah = Node("MERAH 🔴", 40)
hijau = Node("HIJAU 🟢", 20)
kuning = Node("KUNING 🟡", 5)

# 3. Menyambungkan secara Sirkular (Circular)
merah.next = hijau
hijau.next = kuning
kuning.next = merah

# 4. Tampilan Streamlit
st.title("🚦 Simulasi Lampu Lalu Lintas")
placeholder = st.empty()

if st.button("Mulai Simulasi"):
    # Kita mulai dari lampu merah
    current = merah

    while True:
        # Menampilkan durasi hitung mundur
        for i in range(current.durasi, 0, -1):
            with placeholder.container():
                st.header(current.warna)
                st.subheader(f"Waktu: {i} detik")
            time.sleep(1)

        # Pindah ke lampu berikutnya menggunakan pointer .next
        if current.next is not None:
            current = current.next

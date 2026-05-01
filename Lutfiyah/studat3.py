import streamlit as st
import time

# 1. Definisi Node untuk Circular Linked List
class Node:
    def __init__(self, warna, durasi, hex_code):
        self.warna = warna
        self.durasi = durasi
        self.hex_code = hex_code
        self.next = None

# 2. Inisialisasi Struktur Data
merah = Node("Merah", 40, "#FF0000")
hijau = Node("Hijau", 20, "#00FF00")
kuning = Node("Kuning", 5, "#FFFF00")

# Menghubungkan secara sirkular
merah.next = hijau
hijau.next = kuning
kuning.next = merah

# 3. UI Streamlit
st.title("🚦 Visualisasi Lampu Lalu Lintas")
st.subheader("Penerapan Circular Linked List")

placeholder = st.empty()

# Memulai simulasi
current = merah

while True:
    for detik in range(current.durasi, 0, -1):
        with placeholder.container():
            # Membuat visualisasi lingkaran lampu
            st.markdown(
                f"""
                <div style="
                    display: flex; 
                    flex-direction: column; 
                    align-items: center; 
                    background-color: #333; 
                    padding: 20px; 
                    border-radius: 50px; 
                    width: 150px;
                    margin: auto;">
                    <div style="
                        width: 100px; 
                        height: 100px; 
                        background-color: {current.hex_code if current.warna == 'Merah' else '#555'}; 
                        border-radius: 50%; 
                        margin: 10px;"></div>
                    <div style="
                        width: 100px; 
                        height: 100px; 
                        background-color: {current.hex_code if current.warna == 'Kuning' else '#555'}; 
                        border-radius: 50%; 
                        margin: 10px;"></div>
                    <div style="
                        width: 100px; 
                        height: 100px; 
                        background-color: {current.hex_code if current.warna == 'Hijau' else '#555'}; 
                        border-radius: 50%; 
                        margin: 10px;"></div>
                </div>
                <h2 style="text-align: center;">Lampu {current.warna}</h2>
                <h1 style="text-align: center; color: {current.hex_code};">{detik} Detik</h1>
                """,
                unsafe_allow_html=True
            )
            time.sleep(1)
    
    # Pindah ke node berikutnya (Circular)
    current = current.next
import streamlit as st
import time

# 1. Struktur Data Circular Linked List (Sesuai kode asli kamu)
class LampuNode:
    def __init__(self, warna, durasi, warna_hex):
        self.warna = warna
        self.durasi = durasi
        self.warna_hex = warna_hex  # Tambahan untuk warna visual
        self.next = None

# 2. Fungsi untuk membangun struktur Circular Linked List
def buat_siklus_lampu():
    merah = LampuNode("MERAH", 40, "#FF0000")
    hijau = LampuNode("HIJAU", 20, "#00FF00")
    kuning = LampuNode("KUNING", 5, "#FFFF00")
    
    # Menghubungkan secara Circular
    hijau.next = kuning
    kuning.next = merah
    merah.next = hijau
    return hijau

# --- UI STREAMLIT ---
st.set_page_config(page_title="Simulasi Lampu Lalu Lintas", page_icon="🚦")
st.title("🚦 Simulasi Circular Linked List")
st.write("Visualisasi siklus lampu lalu lintas menggunakan logika struktur data.")

# Inisialisasi state agar posisi lampu tidak hilang saat script rerun
if 'node_aktif' not in st.session_state:
    st.session_state.node_aktif = buat_siklus_lampu()

# Wadah kosong untuk update tampilan secara real-time
placeholder = st.empty()

# Tombol Kontrol
col1, col2 = st.columns(2)
mulai = col1.button("▶️ Mulai Simulasi")
stop = col2.button("⏹️ Berhenti")

if mulai:
    while not stop:
        current = st.session_state.node_aktif
        
        # Perulangan untuk hitung mundur durasi lampu
        for detik_sisa in range(current.durasi, 0, -1):
            with placeholder.container():
                # Visualisasi Lampu Bulat dengan CSS sederhana
                st.markdown(f"""
                    <div style="display: flex; flex-direction: column; align-items: center; background-color: #222; padding: 20px; border-radius: 20px; width: 120px; margin: auto;">
                        <div style="width: 70px; height: 70px; background-color: {current.warna_hex if current.warna == 'MERAH' else '#444'}; border-radius: 50%; margin: 5px;"></div>
                        <div style="width: 70px; height: 70px; background-color: {current.warna_hex if current.warna == 'KUNING' else '#444'}; border-radius: 50%; margin: 5px;"></div>
                        <div style="width: 70px; height: 70px; background-color: {current.warna_hex if current.warna == 'HIJAU' else '#444'}; border-radius: 50%; margin: 5px;"></div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Teks Status
                st.markdown(f"<h2 style='text-align: center; color: {current.warna_hex};'>{current.warna}</h2>", unsafe_allow_html=True)
                st.markdown(f"<h1 style='text-align: center;'>{detik_sisa}</h1>", unsafe_allow_html=True)
                
            time.sleep(1)
        
        # Logika Pindah Node (Circular)
        st.session_state.node_aktif = current.next

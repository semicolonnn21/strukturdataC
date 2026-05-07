import streamlit as st
import time

class NodeLampu:
    def __init__(self, warna, durasi):
        self.warna = warna
        self.durasi = durasi
        self.next = None

merah = NodeLampu("Merah", 40)
kuning = NodeLampu("Kuning", 5)
hijau = NodeLampu("Hijau", 20)

# Menghubungkan yhaa minnnn
merah.next = kuning
hijau.next = merah
kuning.next = hijau

st.set_page_config(page_title="Project Lampu Lalu Lintas 🚦", layout="wide")
st.title("Visualisasi Lampu Lalu Lintas 🚦")
st.write("Menggunakan Circular Linked List")
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

wadah_teks = st.empty()
wadah_lampu = st.empty()
wadah_timer = st.empty()
curr = merah # Mulai dari merah

with wadah_teks.container(): # Penammpung
    st.warning("Siap untuk memulai jalan")
    siap = st.button("**Go Go Go!**")

if siap:
    wadah_teks.empty() # Menghapus penampung
    st.balloons()
    st.toast("Mulai!", icon="🚦")
    
    while True:
        with wadah_lampu.container():
            st.markdown("### 🚦 Jl.Malioboro traffic light")
            
            # Menentukan warnanyaaaaa
            c_merah = "🔴" if curr.warna == "Merah" else "⚪"
            c_kuning = "🟡" if curr.warna == "Kuning" else "⚪"
            c_hijau = "🟢" if curr.warna == "Hijau" else "⚪"
            
            st.header(f"{c_merah} {c_kuning} {c_hijau}")
            st.subheader(f"Lampu: {curr.warna}")

        # Hitung mundur durasi
        for detik_sisa in range(curr.durasi, 0, -1):
            wadah_timer.metric("Durasi Sisa", f"{detik_sisa} detik") # Menampilkan Angka yaaaa
            time.sleep(1) # Tunggu 1 detik
        
        # Pindah ke node berikutnya
        curr = curr.next
    

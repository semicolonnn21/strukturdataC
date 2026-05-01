# Visualisasi Lampu Lalu Lintas Menggunakan Circular Linked List dan Streamlit

import streamlit as st
import time

# Node untuk Circular Linked List
class Node:
    def __init__(self, warna, durasi):
        self.warna = warna
        self.durasi = durasi
        self.next = None


# Circular Linked List
class CircularLinkedList:
    def __init__(self):
        self.head = None

    def tambah_node(self, warna, durasi):
        new_node = Node(warna, durasi)

        if not self.head:
            self.head = new_node
            new_node.next = self.head
        else:
            temp = self.head
            while temp.next != self.head:
                temp = temp.next

            temp.next = new_node
            new_node.next = self.head


# Membuat Circular Linked List
lampu = CircularLinkedList()
lampu.tambah_node("Merah", 40)
lampu.tambah_node("Hijau", 20)
lampu.tambah_node("Kuning", 5)


# Inisialisasi session state
if "current" not in st.session_state:
    st.session_state.current = lampu.head
    st.session_state.sisa = lampu.head.durasi


# Tampilan Judul
st.title("🚦 Simulasi Lampu Lalu Lintas")
st.write("Visualisasi Circular Linked List pada Lampu Merah, Hijau, dan Kuning")

# Menampilkan lampu
col1, col2, col3 = st.columns(3)

with col1:
    if st.session_state.current.warna == "Merah":
        st.markdown("## 😡 SABARR")
    else:
        st.markdown("## 🌑 Merah")

with col2:
    if st.session_state.current.warna == "Hijau":
        st.markdown("## 🐸 LETSGOO")
    else:
        st.markdown("## 🌑 Hijau")

with col3:
    if st.session_state.current.warna == "Kuning":
        st.markdown("## 🌞 GASPOLLL")
    else:
        st.markdown("## 🌑 Kuning")

# Menampilkan durasi
st.subheader(f"Sisa Waktu: {st.session_state.sisa} detik")

# Countdown
placeholder = st.empty()

for i in range(st.session_state.sisa, 0, -1):
    placeholder.subheader(f"Sisa Waktu: {i} detik")
    time.sleep(1)

# Pindah ke node berikutnya
st.session_state.current = st.session_state.current.next
st.session_state.sisa = st.session_state.current.durasi

# Refresh halaman otomatis
st.rerun()
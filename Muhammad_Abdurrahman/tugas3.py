import streamlit as st
import time

# Node Circular Linked List
class Node:
    def __init__(self, warna, durasi):
        self.warna = warna
        self.durasi = durasi
        self.next = None

# Circular Linked List
class CircularTrafficLight:
    def __init__(self):
        self.head = None

    def tambah(self, warna, durasi):
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

# Inisialisasi
traffic = CircularTrafficLight()
traffic.tambah("MERAH", 40)
traffic.tambah("HIJAU", 20)
traffic.tambah("KUNING", 5)

st.title("🚦 Simulasi Lampu Lalu Lintas")

start = st.button("Mulai")

lampu_placeholder = st.empty()
countdown_placeholder = st.empty()  # <-- ini kunci

def tampilkan_lampu(warna):
    if warna == "MERAH":
        lampu_placeholder.markdown(
            "<h1 style='text-align:center; color:red;'>🔴 MERAH</h1>",
            unsafe_allow_html=True
        )
    elif warna == "KUNING":
        lampu_placeholder.markdown(
            "<h1 style='text-align:center; color:orange;'>🟡 KUNING</h1>",
            unsafe_allow_html=True
        )
    elif warna == "HIJAU":
        lampu_placeholder.markdown(
            "<h1 style='text-align:center; color:green;'>🟢 HIJAU</h1>",
            unsafe_allow_html=True
        )

if start:
    current = traffic.head
    while True:
        for i in range(current.durasi, 0, -1):
            tampilkan_lampu(current.warna)
            
            # UPDATE teks, bukan tambah baris baru
            countdown_placeholder.markdown(
                f"<h3 style='text-align:center;'>Sisa waktu: {i} detik</h3>",
                unsafe_allow_html=True
            )
            
            time.sleep(1)

        current = current.next
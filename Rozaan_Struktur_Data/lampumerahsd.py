import streamlit as st
import time

class Node:
    def __init__(self, warna, durasi):
        self.warna = warna
        self.durasi = durasi
        self.next = None

class CircularLinkedList:
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

    def get_head(self):
        return self.head

lampu = CircularLinkedList()
lampu.tambah("Merah", 40)
lampu.tambah("Hijau", 20)
lampu.tambah("Kuning", 5)

st.title("Simulasi Lampu Lalu Lintas")

placeholder = st.empty()

if st.button("Mulai"):
    current = lampu.get_head()

    while True:
        for i in range(current.durasi, 0, -1):

            if current.warna == "Merah":
                warna = "red"
            elif current.warna == "Hijau":
                warna = "green"
            else:
                warna = "orange"

            placeholder.markdown(f"""
                <div style='text-align:center;'>
                    <h1 style='color:{warna};'>{current.warna}</h1>
                    <h2>{i} detik</h2>
                </div>
            """, unsafe_allow_html=True)

            time.sleep(1)

        current = current.next
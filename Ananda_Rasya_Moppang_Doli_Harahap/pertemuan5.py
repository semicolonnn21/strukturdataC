import streamlit as st
import time

# ======================
# Struktur Data
# ======================
class Node:
    def __init__(self, color, duration):
        self.color = color
        self.duration = duration
        self.next = None

class CircularLinkedList:
    def __init__(self):
        self.head = None

    def append(self, color, duration):
        new_node = Node(color, duration)

        if not self.head:
            self.head = new_node
            new_node.next = self.head
            return

        temp = self.head
        while temp.next != self.head:
            temp = temp.next

        temp.next = new_node
        new_node.next = self.head


# ======================
# Inisialisasi Data
# ======================
cll = CircularLinkedList()
cll.append("Merah", 40)
cll.append("Hijau", 20)
cll.append("Kuning", 5)

# ======================
# UI
# ======================
st.title("Simulasi Lampu Lalu Lintas 🚦")

placeholder = st.empty()

def render_lamp(active_color, time_left):
    def get_style(color):
        if color == active_color:
            return "opacity: 1;"
        else:
            return "opacity: 0.2;"

    html = f"""
    <div style="display:flex; flex-direction:column; align-items:center;">
        <div style="width:80px; height:80px; border-radius:50%; background:red; {get_style('Merah')}"></div>
        <div style="width:80px; height:80px; border-radius:50%; background:yellow; {get_style('Kuning')}"></div>
        <div style="width:80px; height:80px; border-radius:50%; background:green; {get_style('Hijau')}"></div>
        <h2>{active_color}</h2>
        <h3>{time_left} detik</h3>
    </div>
    """
    placeholder.markdown(html, unsafe_allow_html=True)


current = cll.head

if st.button("Mulai Simulasi"):
    while True:
        for i in range(current.duration, 0, -1):
            render_lamp(current.color, i)
            time.sleep(1)

        current = current.next
import streamlit as st
import time

# Node
class Node:
    def __init__(self, name, emoji, duration):
        self.name = name
        self.emoji = emoji
        self.duration = duration
        self.next = None

# Circular Linked List
class CircularLinkedList:
    def __init__(self):
        self.head = None

    def append(self, name, emoji, duration):
        new_node = Node(name, emoji, duration)
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
lampu = CircularLinkedList()
lampu.append("MERAH", "🔴", 40)
lampu.append("HIJAU", "🟢", 20)
lampu.append("KUNING", "🟡", 5)

# UI
st.title("🚦 Simulasi Lampu Lalu Lintas")
st.caption("Circular Linked List")

start = st.button("▶️ Start Simulasi")

placeholder = st.empty()
progress_bar = st.progress(0)

if start:
    current = lampu.head

    while True:
        for i in range(current.duration, 0, -1):

            # Tampilan lampu
            if current.name == "MERAH":
                tampilan = "🔴\n⚫\n⚫"
            elif current.name == "KUNING":
                tampilan = "⚫\n🟡\n⚫"
            else:
                tampilan = "⚫\n⚫\n🟢"

            # Update UI
            placeholder.markdown(f"""
{tampilan}

### {current.name}
⏳ Sisa waktu: {i} detik
""")

            # Progress bar
            progress = (current.duration - i + 1) / current.duration
            progress_bar.progress(progress)

            time.sleep(1)

        current = current.next
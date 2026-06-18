import streamlit as st
import time

# ==============================
# CIRCULAR LINKED LIST
# ==============================
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


# ==============================
# DATA
# ==============================
lampu = CircularLinkedList()
lampu.tambah("MERAH", 40)
lampu.tambah("HIJAU", 20)
lampu.tambah("KUNING", 5)

# ==============================
# UI
# ==============================
st.set_page_config(page_title="Lampu Lalu Lintas", layout="centered")
st.title("🚦 Simulasi Lampu Lalu Lintas")

placeholder = st.empty()

if "running" not in st.session_state:
    st.session_state.running = False

if "current" not in st.session_state:
    st.session_state.current = lampu.get_head()

col1, col2 = st.columns(2)
with col1:
    if st.button("▶️ Start"):
        st.session_state.running = True

with col2:
    if st.button("⏹ Stop"):
        st.session_state.running = False


# ==============================
# LAMPU VISUAL (GLOW EFFECT)
# ==============================
def lampu_visual(warna):
    def style(active, color):
        if active:
            return f"""
            background:{color};
            box-shadow: 0 0 40px {color}, 0 0 80px {color};
            """
        else:
            return "background:#222;"

    merah = style(warna == "MERAH", "red")
    kuning = style(warna == "KUNING", "yellow")
    hijau = style(warna == "HIJAU", "lime")

    return f"""
    <div style="display:flex; flex-direction:column; align-items:center;">
        <div style="width:90px;height:90px;border-radius:50%;margin:12px;{merah}"></div>
        <div style="width:90px;height:90px;border-radius:50%;margin:12px;{kuning}"></div>
        <div style="width:90px;height:90px;border-radius:50%;margin:12px;{hijau}"></div>
    </div>
    """


# ==============================
# SIMULASI
# ==============================
if st.session_state.running:
    current = st.session_state.current

    while st.session_state.running:
        warna = current.warna
        durasi = current.durasi

        for i in range(durasi, 0, -1):
            if not st.session_state.running:
                break

            placeholder.markdown(f"""
            {lampu_visual(warna)}
            <h2 style='text-align:center;'>🚦 {warna}</h2>
            <p style='text-align:center;'>⏱ {i} detik</p>
            """, unsafe_allow_html=True)

            time.sleep(1)

        current = current.next
        st.session_state.current = current
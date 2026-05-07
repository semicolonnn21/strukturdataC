import streamlit as st
import time

# ================= STATE =================
if "running" not in st.session_state:
    st.session_state.running = False

# ================= STYLE =================
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}

/* Navbar */
.navbar {
    font-size: 28px;
    font-weight: bold;
    padding: 15px;
    text-align: center;
    background: rgba(0,0,0,0.5);
    border-radius: 10px;
    margin-bottom: 20px;
}

/* Card */
.card {
    background: rgba(0,0,0,0.6);
    padding: 30px;
    border-radius: 20px;
    text-align: center;
}

/* Lampu */
.lamp {
    width: 90px;
    height: 90px;
    border-radius: 50%;
    margin: 10px auto;
    opacity: 0.2;
}
.red { background: red; }
.yellow { background: yellow; }
.green { background: lime; }

.active {
    opacity: 1 !important;
    box-shadow: 0 0 40px white;
}

/* Tombol */
.stButton > button {
    border-radius: 10px;
    height: 50px;
    width: 140px;
    font-size: 18px;
    font-weight: bold;
    transition: 0.3s;
}

/* Mulai */
div[data-testid="column"]:nth-of-type(1) button {
    background-color: #28a745;
    color: white;
}
div[data-testid="column"]:nth-of-type(1) button:hover {
    background-color: #218838;
}

/* Stop */
div[data-testid="column"]:nth-of-type(2) button {
    background-color: #dc3545;
    color: white;
}
div[data-testid="column"]:nth-of-type(2) button:hover {
    background-color: #c82333;
}

/* Mobil */
.car {
    font-size: 30px;
    animation: move 3s linear infinite;
}

@keyframes move {
    from { transform: translateX(-200px); }
    to { transform: translateX(200px); }
}

</style>
""", unsafe_allow_html=True)

# ================= LINKED LIST =================
class Node:
    def __init__(self, warna, durasi):
        self.warna = warna
        self.durasi = durasi
        self.next = None

class CircularLinkedList:
    def __init__(self):
        self.head = None

    def tambah(self, warna, durasi):
        node = Node(warna, durasi)
        if not self.head:
            self.head = node
            node.next = node
        else:
            temp = self.head
            while temp.next != self.head:
                temp = temp.next
            temp.next = node
            node.next = self.head

lampu = CircularLinkedList()
lampu.tambah("MERAH", 40)
lampu.tambah("HIJAU", 20)
lampu.tambah("KUNING", 5)

# ================= NAVBAR =================
st.markdown('<div class="navbar">🚦 Smart Traffic Light Dashboard</div>', unsafe_allow_html=True)

# ================= CONTROL =================
speed = st.slider("⚡ Kecepatan", 0.1, 1.0, 0.5)

col1, col2 = st.columns(2)

if col1.button("▶️ Mulai"):
    st.session_state.running = True

if col2.button("⏹ Stop"):
    st.session_state.running = False

placeholder = st.empty()

# ================= DISPLAY =================
def tampil(warna, detik):
    r, y, g = "lamp red", "lamp yellow", "lamp green"

    if warna == "MERAH":
        r += " active"
    elif warna == "KUNING":
        y += " active"
    else:
        g += " active"

    mobil = "🚗 Jalan" if warna == "HIJAU" else "⛔ Stop"

    html = f"""
    <div class="card">
        <div class="{r}"></div>
        <div class="{y}"></div>
        <div class="{g}"></div>
        <h2>{warna}</h2>
        <h3>{detik} detik</h3>
        <div class="car">{mobil}</div>
    </div>
    """
    placeholder.markdown(html, unsafe_allow_html=True)

# ================= LOOP =================
if st.session_state.running:
    if "current" not in st.session_state:
        st.session_state.current = lampu.head
        st.session_state.timer = lampu.head.durasi

    tampil(st.session_state.current.warna, st.session_state.timer)

    time.sleep(speed)

    st.session_state.timer -= 1

    if st.session_state.timer <= 0:
        st.session_state.current = st.session_state.current.next
        st.session_state.timer = st.session_state.current.durasi

    st.rerun()
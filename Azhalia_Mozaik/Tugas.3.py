import streamlit as st
import time

# 1. Struktur Data (Circular Linked List)
class Node:
    def __init__(self, warna, durasi):
        self.warna = warna
        self.durasi = durasi
        self.next = None

class CircularLinkedList:
    def __init__(self):
        self.head = None

    def add_node(self, warna, durasi):
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

# Inisialisasi Data
traffic_light = CircularLinkedList()
traffic_light.add_node("Merah", 40)
traffic_light.add_node("Hijau", 20)
traffic_light.add_node("Kuning", 5)

# 2. Pengaturan Tampilan Streamlit
st.set_page_config(page_title="Pro Simulasi Lalin", layout="wide")

# CSS kustom untuk mempercantik teks dan layout
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        background: linear-gradient(145deg, #2e3139, #1a1c23);
        color: white;
        border: none;
        padding: 10px;
        font-weight: bold;
    }
    .status-card {
        background: #1a1c23;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #343946;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚦 Sistem Lampu Lalu Lintas")

# Layout Kolom
col_space1, col_light, col_info, col_space2 = st.columns([1, 1.5, 2, 1])

with col_light:
    container_visual = st.empty()

with col_info:
    st.markdown("<div class='status-card'>", unsafe_allow_html=True)
    container_timer = st.empty()
    container_msg = st.empty()
    st.markdown("</div>", unsafe_allow_html=True)
    st.write("---")
    start_btn = st.button("JALANKAN SIMULASI")

def draw_traffic_light(active_color=""):
    # Warna palet modern (dim vs glow)
    colors = {
        "Merah": {"on": "#ff3e3e", "off": "#3a1515", "shadow": "0 0 40px #ff3e3e"},
        "Kuning": {"on": "#ffcc00", "off": "#3a2e00", "shadow": "0 0 40px #ffcc00"},
        "Hijau": {"on": "#00ff88", "off": "#003a1f", "shadow": "0 0 40px #00ff88"}
    }

    m_style = colors["Merah"]["on"] if active_color == "Merah" else colors["Merah"]["off"]
    m_glow = colors["Merah"]["shadow"] if active_color == "Merah" else "none"
    
    k_style = colors["Kuning"]["on"] if active_color == "Kuning" else colors["Kuning"]["off"]
    k_glow = colors["Kuning"]["shadow"] if active_color == "Kuning" else "none"
    
    h_style = colors["Hijau"]["on"] if active_color == "Hijau" else colors["Hijau"]["off"]
    h_glow = colors["Hijau"]["shadow"] if active_color == "Hijau" else "none"

    # HTML Tiang Lampu yang Estetik
    html_code = f"""
    <div style="display: flex; flex-direction: column; align-items: center;">
        <div style="
            background: #1a1c23;
            padding: 30px 20px;
            border-radius: 50px;
            border: 4px solid #343946;
            box-shadow: 10px 10px 20px #080a0e;
            width: 140px;
            display: flex;
            flex-direction: column;
            gap: 25px;
            align-items: center;
        ">
            <div style="width: 80px; height: 80px; background: {m_style}; border-radius: 50%; box-shadow: {m_glow}; border: 3px solid #000;"></div>
            <div style="width: 80px; height: 80px; background: {k_style}; border-radius: 50%; box-shadow: {k_glow}; border: 3px solid #000;"></div>
            <div style="width: 80px; height: 80px; background: {h_style}; border-radius: 50%; box-shadow: {h_glow}; border: 3px solid #000;"></div>
        </div>
        <div style="width: 20px; height: 100px; background: #343946;"></div>
    </div>
    """
    container_visual.markdown(html_code, unsafe_allow_html=True)

# Main Logic
if start_btn:
    curr = traffic_light.head
    for _ in range(6): 
        draw_traffic_light(curr.warna)
        
        # Tampilan Info Samping
        color_hex = "#ff3e3e" if curr.warna == "Merah" else ("#ffcc00" if curr.warna == "Kuning" else "#00ff88")
        
        # Logika Pesan Khusus
        if curr.warna == "Merah":
            container_msg.markdown(f"""
                <div style="padding: 15px; background: #3a1515; border-left: 5px solid #ff3e3e; color: #ffbcbc; border-radius: 5px; margin-top: 20px;">
                    <strong>ATTENTION:</strong><br>Kendaraan wajib berhenti secara total di belakang garis pemberhentian.
                </div>
            """, unsafe_allow_html=True)
        elif curr.warna == "Kuning":
            container_msg.markdown(f"""
                <div style="padding: 15px; background: #3a2e00; border-left: 5px solid #ffcc00; color: #ffeb99; border-radius: 5px; margin-top: 20px;">
                    <strong>WARNING:</strong><br>Peringatan bagi pengguna jalan untuk mengurangi kecepatan dan bersiap untuk berhenti.
                </div>
            """, unsafe_allow_html=True)
        elif curr.warna == "Hijau":
            container_msg.markdown(f"""
                <div style="padding: 15px; background: #003a1f; border-left: 5px solid #00ff88; color: #ccffeb; border-radius: 5px; margin-top: 20px;">
                    <strong>INFO:</strong><br>Mohon perhatian, kendaraan dipersilakan melanjutkan perjalanan, harap tetap waspada dan berhati-hati.
                </div>
            """, unsafe_allow_html=True)

        # Countdown Timer
        for sisa in range(curr.durasi, 0, -1):
            container_timer.markdown(f"""
                <h1 style='text-align: center; color: {color_hex}; font-size: 80px; margin: 0;'>{sisa}</h1>
                <p style='text-align: center; color: #888; letter-spacing: 5px;'>DETIK - {curr.warna.upper()}</p>
            """, unsafe_allow_html=True)
            time.sleep(1)
            
        curr = curr.next
else:
    draw_traffic_light()
    container_timer.markdown("<h2 style='text-align: center; color: #444;'>READY</h2>", unsafe_allow_html=True)
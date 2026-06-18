import streamlit as st
import time

# 1. Struktur Circular Linked List
class Node:
    def __init__(self, warna, durasi, warna_hex):
        self.warna = warna
        self.durasi = durasi
        self.warna_hex = warna_hex
        self.next = None

class CircularLinkedList:
    def __init__(self):
        self.head = None

    def tambah_lampu(self, warna, durasi, warna_hex):
        new_node = Node(warna, durasi, warna_hex)
        if not self.head:
            self.head = new_node
            new_node.next = self.head
        else:
            temp = self.head
            while temp.next != self.head:
                temp = temp.next
            temp.next = new_node
            new_node.next = self.head

# 2. Inisialisasi Data
cll = CircularLinkedList()
cll.tambah_lampu("Merah", 5, "#FF0000")
cll.tambah_lampu("Hijau", 5, "#00FF00")
cll.tambah_lampu("Kuning", 5, "#FFFF00")

st.set_page_config(page_title="Smart Traffic System", page_icon="🚦", layout="centered")

st.title("🚦 Smart Traffic Visualizer")
st.markdown("---")

if 'berjalan' not in st.session_state:
    st.session_state.berjalan = False

def play_beep_js():
    js_code = """
        <script>
        var context = new (window.AudioContext || window.webkitAudioContext)();
        var osc = context.createOscillator();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(800, context.currentTime);
        osc.connect(context.destination);
        osc.start();
        osc.stop(context.currentTime + 0.1);
        </script>
    """
    st.components.v1.html(js_code, height=0)

# Layout Tombol
col1, col2 = st.columns(2)
with col1:
    if st.button('▶️ Mulai Simulasi', use_container_width=True):
        st.session_state.berjalan = True
with col2:
    if st.button('🛑 Berhenti', use_container_width=True):
        st.session_state.berjalan = False
        st.rerun()

# Tempat display utama
display_lampu = st.empty()
display_timer = st.empty()
display_visual_list = st.empty()

if st.session_state.berjalan:
    current = cll.head
    while st.session_state.berjalan:
        play_beep_js()
        
        # 1. Visualisasi Lampu (Glow)
        glow_style = f"box-shadow: 0 0 50px {current.warna_hex}, 0 0 20px {current.warna_hex};"
        with display_lampu.container():
            st.markdown(
                f"""
                <div style="display: flex; flex-direction: column; align-items: center; background-color: #222; padding: 25px; border-radius: 50px; width: 140px; margin: auto; border: 4px solid #444;">
                    <div style="width: 70px; height: 70px; border-radius: 50%; background-color: {current.warna_hex if current.warna == 'Merah' else '#333'}; margin-bottom: 15px; {glow_style if current.warna == 'Merah' else ''} border: 2px solid #555;"></div>
                    <div style="width: 70px; height: 70px; border-radius: 50%; background-color: {current.warna_hex if current.warna == 'Kuning' else '#333'}; margin-bottom: 15px; {glow_style if current.warna == 'Kuning' else ''} border: 2px solid #555;"></div>
                    <div style="width: 70px; height: 70px; border-radius: 50%; background-color: {current.warna_hex if current.warna == 'Hijau' else '#333'}; {glow_style if current.warna == 'Hijau' else ''} border: 2px solid #555;"></div>
                </div>
                """, unsafe_allow_html=True
            )

        # 2. Visualisasi Struktur Circular Linked List (Bawah Lampu)
        with display_visual_list.container():
            st.write("### 🧩 Struktur Data: Circular Linked List")
            cols = st.columns(3)
            list_warna = ["Merah", "Hijau", "Kuning"]
            for idx, w in enumerate(list_warna):
                is_active = (current.warna == w)
                border = "3px solid #fff" if is_active else "1px solid #555"
                bg = current.warna_hex if is_active else "#222"
                cols[idx].markdown(
                    f"<div style='text-align:center; padding:10px; border-radius:10px; border:{border}; background-color:{bg}; color:{'black' if is_active else 'white'}'>{w}</div>", 
                    unsafe_allow_html=True
                )
            st.caption("Pointer otomatis kembali dari Kuning ke Merah karena 'next' node terakhir menunjuk ke head.")

        # 3. Timer
        for i in range(current.durasi, 0, -1):
            display_timer.metric("Lampu Sedang Aktif", current.warna, f"{i} detik")
            time.sleep(1)
        
        current = current.next
else:
    st.info("Sistem siap. Klik Mulai untuk mengaktifkan Circular Linked List.")
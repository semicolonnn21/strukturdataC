import streamlit as st
import time
import queue
import threading

# desian ui/ux
st.set_page_config(
    page_title="Sistem Lampu Merah 2 Arah", 
    page_icon="🚦",
    layout="wide"
)

class TrafficLight2Way:
    def __init__(self):
        self.durations = {'GREEN': 15, 'YELLOW': 3, 'RED': 0}
        self.intersections = {
            'US': {'current': 'RED', 'time': 0},  # utara-selatan
            'TB': {'current': 'RED', 'time': 0}   # timur-barat
        }
        self.is_running = False
        self.thread = None
        self.current_active = 'US'
    
    def start(self):
        if not self.is_running:
            self.is_running = True
            self.thread = threading.Thread(target=self.run_cycle, daemon=True)
            self.thread.start()
    
    def stop(self):
        self.is_running = False
    
    def set_green(self, direction):
        self.intersections[direction]['current'] = 'GREEN'
        self.intersections[direction]['time'] = self.durations['GREEN']
        self.current_active = direction
        # lawan jadi merah
        other = 'TB' if direction == 'US' else 'US'
        self.intersections[other]['current'] = 'RED'
        self.intersections[other]['time'] = 0
    
    def set_yellow(self, direction):
        self.intersections[direction]['current'] = 'YELLOW'
        self.intersections[direction]['time'] = self.durations['YELLOW']
        other = 'TB' if direction == 'US' else 'US'
        self.intersections[other]['current'] = 'RED'
        self.intersections[other]['time'] = 0
    
    def tick(self):
        for direction in self.intersections:
            if self.intersections[direction]['time'] > 0:
                self.intersections[direction]['time'] -= 1
    
    def run_cycle(self):
        while self.is_running:
            # us ijo
            self.set_green('US')
            while self.intersections['US']['time'] > 0 and self.is_running:
                time.sleep(1)
                self.tick()
            
            # us kuning
            self.set_yellow('US')
            while self.intersections['US']['time'] > 0 and self.is_running:
                time.sleep(1)
                self.tick()
            
            # tb ijo
            self.set_green('TB')
            while self.intersections['TB']['time'] > 0 and self.is_running:
                time.sleep(1)
                self.tick()
            
            # tb kuning
            self.set_yellow('TB')
            while self.intersections['TB']['time'] > 0 and self.is_running:
                time.sleep(1)
                self.tick()

# inisialisasi
if 'system' not in st.session_state:
    st.session_state.system = TrafficLight2Way()
    st.session_state.logs = []

system = st.session_state.system

# header dan kontrol panel
st.markdown("---")
header_col1, header_col2, header_col3 = st.columns([2, 2, 1])

with header_col1:
    st.title("🚦 **Sistem Lampu Merah 2 Arah**")

with header_col2:
    st.markdown("### *Utara-Selatan ↔ Timur-Barat*")

with header_col3:
    if st.button("🚀 **MULAI**", type="primary", use_container_width=True):
        system.start()
    
    if st.button("⏹️ **STOP**", type="secondary", use_container_width=True):
        system.stop()

# status
status_col1, status_col2 = st.columns(2)
with status_col1:
    status_emoji = "🟢 **AKTIF**" if system.is_running else "🔴 **MATI**"
    st.metric("Status", status_emoji)

with status_col2:
    active_dir = system.current_active if system.is_running else "NONE"
    st.metric("Arah Aktif", f"**{active_dir}**")

#lampu merah
st.markdown("---")
st.subheader("🚦 **Visualisasi Lampu Lalu Lintas**")

light_col1, light_col2 = st.columns([1, 1], gap="large")

colors = {'RED': "#ff0000", 'YELLOW': "#ffe601", 'GREEN': "#00ff00"}

#lampu utara selatan
with light_col1:
    st.markdown("### 🠉🠋 **UTARA-SELATAN (US)**")
    
    us_status = system.intersections['US']['current']
    us_time = system.intersections['US']['time']
    
    led_style = f"background: radial-gradient(circle, {colors[us_status]}, #ddd);"
    
    st.markdown(f"""
    <div style="
        {led_style}
        width: 220px; height: 220px;
        border-radius: 50%;
        border: 12px solid #333;
        margin: 0 auto 20px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        font-size: 40px;
        font-weight: 900;
        color: #000;
        animation: pulse 2s infinite;
    ">
        {us_status}
    </div>
    """, unsafe_allow_html=True)
    
    us_col1, us_col2 = st.columns(2)
    with us_col1:
        st.metric("⏱️ US", f"{us_time}s")
    with us_col2:
        st.progress(us_time / 18.0)

#lampu timur barat
with light_col2:
    st.markdown("### 🠊🠈 **TIMUR-BARAT (TB)**")
    
    tb_status = system.intersections['TB']['current']
    tb_time = system.intersections['TB']['time']
    
    led_style = f"background: radial-gradient(circle, {colors[tb_status]}, #ddd);"
    
    st.markdown(f"""
    <div style="
        {led_style}
        width: 220px; height: 220px;
        border-radius: 50%;
        border: 12px solid #333;
        margin: 0 auto 20px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        font-size: 40px;
        font-weight: 900;
        color: #000;
        animation: pulse 2s infinite;
    ">
        {tb_status}
    </div>
    """, unsafe_allow_html=True)
    
    tb_col1, tb_col2 = st.columns(2)
    with tb_col1:
        st.metric("⏱️ TB", f"{tb_time}s")
    with tb_col2:
        st.progress(tb_time / 18.0)

#refres sistem
if system.is_running:
    time.sleep(0.5)
    st.rerun()
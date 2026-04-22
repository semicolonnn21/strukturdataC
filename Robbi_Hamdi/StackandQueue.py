import streamlit as st
import streamlit.components.v1 as components
import math

st.set_page_config(page_title="Circular Queue", page_icon="🔄", layout="centered")


# ─── Logic Circular Queue (Tetap Sama) ───────────────────────────────────────
class CircularQueue:
    def __init__(self, k):
        self.k = k
        self.queue = [None] * k
        self.front = -1
        self.rear = -1

    def is_empty(self):
        return self.front == -1

    def is_full(self):
        return (self.rear + 1) % self.k == self.front

    def size(self):
        if self.is_empty():
            return 0
        if self.rear >= self.front:
            return self.rear - self.front + 1
        return self.k - self.front + self.rear + 1

    def enqueue(self, value):
        if self.is_full():
            return False
        if self.is_empty():
            self.front = self.rear = 0
        else:
            self.rear = (self.rear + 1) % self.k
        self.queue[self.rear] = value
        return True

    def dequeue(self):
        if self.is_empty():
            return None
        data = self.queue[self.front]
        self.queue[self.front] = None
        if self.front == self.rear:
            self.front = self.rear = -1
        else:
            self.front = (self.front + 1) % self.k
        return data


# ─── Session State ───────────────────────────────────────────────────────────
if "cq" not in st.session_state:
    st.session_state.cq = CircularQueue(6)
    st.session_state.log = []


def add_log(msg):
    st.session_state.log.insert(0, msg)
    if len(st.session_state.log) > 5:
        st.session_state.log.pop()


cq = st.session_state.cq

# ─── UI ──────────────────────────────────────────────────────────────────────
st.title("🔄 Circular Queue Visualizer")


# Fungsi Visualisasi Menggunakan st.components.v1
def draw_circular_queue_component(cq):
    size = 350
    radius = 120
    center = size / 2
    nodes_html = ""

    for i in range(cq.k):
        angle = (i / cq.k) * 2 * math.pi - (math.pi / 2)
        node_size = 55
        x = center + radius * math.cos(angle) - (node_size / 2)
        y = center + radius * math.sin(angle) - (node_size / 2)

        val = cq.queue[i]
        is_f = (i == cq.front) and not cq.is_empty()
        is_r = (i == cq.rear) and not cq.is_empty()

        # Penentuan Warna
        bg = "#3498db" if val is not None else "#2c3e50"
        border = "#ecf0f1"
        badge = ""

        if is_f and is_r:
            border = "#f1c40f"
            badge = "F&R"
        elif is_f:
            border = "#2ecc71"
            badge = "F"
        elif is_r:
            border = "#e74c3c"
            badge = "R"

        nodes_html += f"""
        <div style="position: absolute; left: {x}px; top: {y}px; width: {node_size}px; height: {node_size}px; 
                    background: {bg}; border: 3px solid {border}; border-radius: 50%; 
                    display: flex; justify-content: center; align-items: center; 
                    color: white; font-family: sans-serif; font-weight: bold; font-size: 18px;
                    box-shadow: 0 4px 10px rgba(0,0,0,0.3); transition: all 0.3s;">
            {val if val is not None else ""}
            <div style="position: absolute; top: -15px; width: 100%; text-align: center; color: {border}; font-size: 12px;">{badge}</div>
            <div style="position: absolute; bottom: -22px; color: #95a5a6; font-size: 11px;">[{i}]</div>
        </div>
        """

    html_content = f"""
    <div style="background: transparent; display: flex; justify-content: center; align-items: center; height: {size}px;">
        <div style="position: relative; width: {size}px; height: {size}px;">
            <div style="position: absolute; width: {radius * 2}px; height: {radius * 2}px; border: 2px dashed #444; 
                        border-radius: 50%; left: {center - radius}px; top: {center - radius}px; opacity: 0.3;"></div>
            {nodes_html}
        </div>
    </div>
    """
    # Render menggunakan komponen HTML khusus
    components.html(html_content, height=size + 50)


# Jalankan Visualisasi
draw_circular_queue_component(cq)

# ─── Controls ────────────────────────────────────────────────────────────────
st.write(
    f"**Status:** {'🔴 Full' if cq.is_full() else '🟢 OK'} | **Size:** {cq.size()}/{cq.k}"
)

col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    input_val = st.text_input(
        "Value", placeholder="Input angka/teks", label_visibility="collapsed"
    )
with col2:
    if st.button("Enqueue", use_container_width=True):
        if input_val:
            if cq.enqueue(input_val):
                add_log(f"Added: {input_val}")
            else:
                st.error("Queue Full!")
            st.rerun()
with col3:
    if st.button("Dequeue", use_container_width=True):
        res = cq.dequeue()
        if res:
            add_log(f"Removed: {res}")
        else:
            st.error("Queue Empty!")
        st.rerun()

new_k = st.slider("Ubah Kapasitas", 3, 12, cq.k)
if st.button("Reset & Terapkan Kapasitas Baru"):
    st.session_state.cq = CircularQueue(new_k)
    st.session_state.log = []
    st.rerun()

st.subheader("📋 Log Terakhir")
for l in st.session_state.log:
    st.caption(l)

import streamlit as st
import time

# Circular Linked List

class Node:
    def __init__(self, name: str, duration: int, color_hex: str):
        self.name = name
        self.duration = duration
        self.color_hex = color_hex
        self.next: "Node | None" = None

    def __repr__(self):
        return f"Node({self.name}, {self.duration}s)"


def build_circular_list() -> Node:
    """Membangun circular linked list: MERAH → HIJAU → KUNING → (kembali ke MERAH)"""
    merah  = Node("MERAH",  100, "#FF4444")
    hijau  = Node("HIJAU",  15, "#44EE44")
    kuning = Node("KUNING",  3, "#FFDD00")

    merah.next  = hijau
    hijau.next  = kuning
    kuning.next = merah          # circular: kembali ke head

    return merah


def traverse_list(head: Node) -> list[Node]:
    """Traverse circular linked list sekali putaran, kembalikan list of nodes."""
    result = []
    current = head
    while True:
        result.append(current)
        current = current.next
        if current is head:
            break
    return result


st.set_page_config(
    page_title="Lampu Lalu Lintas - Circular Linked List",
    page_icon="🚦",
    layout="centered",
)

st.title("🚦 Visualisasi Lampu Lalu Lintas")
st.caption("Implementasi menggunakan **Circular Linked List** | Struktur Data")

# Inisialisasi session state
if "current_node" not in st.session_state:
    head = build_circular_list()
    st.session_state.head = head
    st.session_state.current_node = head
    st.session_state.remaining = head.duration
    st.session_state.paused = False
    st.session_state.cycle_count = 0
    st.session_state.history = []

current: Node = st.session_state.current_node
remaining: int = st.session_state.remaining

# Tampilan lampu

def lamp_html(color_active: str, is_on: bool) -> str:
    if is_on:
        style = (
            f"background-color:{color_active};"
            f"box-shadow: 0 0 30px 12px {color_active}88;"
        )
    else:
        style = "background-color:#2a2a2a;"
    return (
        f'<div style="width:90px;height:90px;border-radius:50%;'
        f'{style}border:3px solid #444;margin:0 auto 12px;"></div>'
    )

traffic_light_html = f"""
<div style="
    background:#1a1a1a;
    border-radius:16px;
    padding:24px 40px;
    display:inline-block;
    border:2px solid #333;
    text-align:center;
">
    {lamp_html('#FF4444', current.name == 'MERAH')}
    {lamp_html('#FFDD00', current.name == 'KUNING')}
    {lamp_html('#44EE44', current.name == 'HIJAU')}
</div>
"""

col_light, col_info = st.columns([1, 2], gap="large")

with col_light:
    st.markdown(traffic_light_html, unsafe_allow_html=True)

with col_info:
    st.markdown(f"### Status: **{current.name}**")
    st.markdown(f"Durasi total: **{current.duration} detik**")

    # Progress bar
    progress_pct = remaining / current.duration
    st.progress(progress_pct, text=f"⏱ Sisa waktu: **{remaining} detik**")

    st.markdown(f"🔄 Siklus ke-**{st.session_state.cycle_count}**")

# Struktur Circular Linked List

nodes = traverse_list(st.session_state.head)
cols = st.columns(len(nodes))

for i, (col, node) in enumerate(zip(cols, nodes)):
    is_active = node.name == current.name
    border = f"3px solid {node.color_hex}" if is_active else "1px solid #555"
    bg = "#1a1a1a" if is_active else "#111"
    arrow = " ➜" if i < len(nodes) - 1 else " ↩"

    col.markdown(
        f"""
        <div style="
            background:{bg};
            border:{border};
            border-radius:10px;
            padding:10px;
            text-align:center;
            color:#eee;
            font-family:monospace;
        ">
            <div style="color:{node.color_hex};font-weight:bold;font-size:15px;">
                {node.name}
            </div>
            <div style="font-size:12px;color:#aaa;">{node.duration} detik</div>
            <div style="font-size:12px;color:#666;">next{arrow}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Kontrol tombol

st.divider()
btn_col1, btn_col2, btn_col3 = st.columns(3)

with btn_col1:
    if st.button("⏸ Pause / Lanjut", use_container_width=True):
        st.session_state.paused = not st.session_state.paused

with btn_col2:
    if st.button("⏭ Lewati ke Berikutnya", use_container_width=True):
        st.session_state.history.append(
            f"{current.name} ({current.duration}s) → {current.next.name}"
        )
        st.session_state.current_node = current.next
        st.session_state.remaining = current.next.duration
        st.session_state.cycle_count += 1
        st.rerun()

with btn_col3:
    if st.button("🔄 Reset", use_container_width=True):
        head = build_circular_list()
        st.session_state.head = head
        st.session_state.current_node = head
        st.session_state.remaining = head.duration
        st.session_state.paused = False
        st.session_state.cycle_count = 0
        st.session_state.history = []
        st.rerun()

# Auto-tick

if not st.session_state.paused:
    time.sleep(1)
    st.session_state.remaining -= 1
    if st.session_state.remaining <= 0:
        st.session_state.history.append(
            f"{current.name} ({current.duration}s) → {current.next.name}"
        )
        st.session_state.current_node = current.next
        st.session_state.remaining = current.next.duration
        st.session_state.cycle_count += 1
    st.rerun()

# Riwayat

if st.session_state.history:
    st.divider()
    st.subheader("📜 Riwayat Pergantian")
    for entry in reversed(st.session_state.history[-10:]):
        st.markdown(f"- {entry}")
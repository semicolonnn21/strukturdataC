import streamlit as st
import time
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Traffic Light + Zebra Cross",
    page_icon="🚦",
    layout="wide"
)

# =========================
# NODE CLL
# =========================
class Node:
    def __init__(self, us, tb, duration):
        self.us = us
        self.tb = tb
        self.duration = duration
        self.next = None


# =========================
# BUILD CYCLE (DURASI REALISTIS)
# =========================
def build_cycle():
    n1 = Node("GREEN", "RED", 20)   # Hijau 20 detik
    n2 = Node("YELLOW", "RED", 5)   # Kuning 5 detik
    n3 = Node("RED", "GREEN", 20)   # Hijau arah lain
    n4 = Node("RED", "YELLOW", 5)   # Kuning arah lain

    # RED otomatis terjadi saat lawan GREEN/YELLOW (40 detik total)

    n1.next = n2
    n2.next = n3
    n3.next = n4
    n4.next = n1

    return n1


# =========================
# VISUAL LAMPU
# =========================
def draw_light(active):
    def lamp(color, on):
        glow = f"0 0 20px {color}" if on else "none"
        opacity = "1" if on else "0.2"

        return f"""
        <div style="
            width:60px;height:60px;
            border-radius:50%;
            margin:8px auto;
            background:{color};
            opacity:{opacity};
            box-shadow:{glow};
        "></div>
        """

    return f"""
    <div style="
        background:#111;
        padding:20px;
        border-radius:20px;
        width:110px;
        margin:auto;
    ">
        {lamp("#ff3b3b", active=="RED")}
        {lamp("#ffd633", active=="YELLOW")}
        {lamp("#00cc44", active=="GREEN")}
    </div>
    """


# =========================
# ZEBRA CROSS
# =========================
def draw_zebra(is_walk):
    color = "#00cc44" if is_walk else "#ff3b3b"
    text = "BOLEH MENYEBRANG" if is_walk else "DILARANG MENYEBRANG"

    return f"""
    <div style="text-align:center; margin-top:15px;">
        
        <div style="
            font-size:14px;
            color:#aaa;
            margin-bottom:5px;
        ">
            Zebra Cross
        </div>

        <div style="
            width:150px;
            margin:auto;
            padding:10px;
            border-radius:10px;
            background:#222;
            color:white;
            font-weight:bold;
        ">
            <div style="
                background:{color};
                padding:10px;
                border-radius:8px;
                box-shadow:0 0 15px {color};
            ">
                🚶 {text}
            </div>
        </div>
    </div>
    """


# =========================
# SESSION STATE
# =========================
if "running" not in st.session_state:
    st.session_state.running = False

if "node" not in st.session_state:
    st.session_state.node = build_cycle()
    st.session_state.time_left = st.session_state.node.duration


# =========================
# HEADER
# =========================
st.title("🚦 Traffic Light 2-Way + Zebra Cross")
st.caption("Durasi: Merah 40s | Kuning 5s | Hijau 20s")

col1, col2 = st.columns(2)

with col1:
    if st.button("Start"):
        st.session_state.running = True

with col2:
    if st.button("Stop"):
        st.session_state.running = False


# =========================
# DISPLAY
# =========================
st.markdown("---")
col_us, col_tb = st.columns(2)

node = st.session_state.node

# LOGIKA ZEBRA
zebra_us = True if node.us == "RED" else False
zebra_tb = True if node.tb == "RED" else False


# ===== UTARA - SELATAN =====
with col_us:
    st.subheader("↑↓ Utara - Selatan")

    components.html(draw_light(node.us), height=260)
    components.html(draw_zebra(zebra_us), height=180)

    st.markdown(
        f"<h4 style='text-align:center'>{node.us}</h4>",
        unsafe_allow_html=True
    )


# ===== TIMUR - BARAT =====
with col_tb:
    st.subheader("→← Timur - Barat")

    components.html(draw_light(node.tb), height=260)
    components.html(draw_zebra(zebra_tb), height=180)

    st.markdown(
        f"<h4 style='text-align:center'>{node.tb}</h4>",
        unsafe_allow_html=True
    )


# =========================
# TIMER
# =========================
st.markdown("---")
st.markdown(
    f"<h2 style='text-align:center'>⏱️ {st.session_state.time_left} detik</h2>",
    unsafe_allow_html=True
)


# =========================
# LOOP CLL
# =========================
if st.session_state.running:
    time.sleep(1)
    st.session_state.time_left -= 1

    if st.session_state.time_left <= 0:
        st.session_state.node = st.session_state.node.next
        st.session_state.time_left = st.session_state.node.duration

    st.rerun()

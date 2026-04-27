import streamlit as st
import time

st.title("Simulasi Lampu Lalu Lintas")

# tombol start di bawah judul (biar gak di tengah)
start = st.button(" Start ")

# style CSS
st.markdown("""
<style>
.traffic-box {
    width: 200px;
    background-color: #222;
    padding: 20px;
    border-radius: 20px;
    margin: 20px auto;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.lamp {
    width: 90px;
    height: 90px;
    border-radius: 50%;
    margin: 10px 0;
}

.red {background-color: red;}
.yellow {background-color: gold;}
.green {background-color: limegreen;}
.off {background-color: #444;}

.timer {
    text-align: center;
    font-size: 24px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

box = st.empty()
timer = st.empty()

def show_lamp(active):
    colors = {
        "red": "off",
        "yellow": "off",
        "green": "off"
    }

    colors[active] = active

    box.markdown(f"""
    <div class="traffic-box">
        <div class="lamp {colors['red']}"></div>
        <div class="lamp {colors['yellow']}"></div>
        <div class="lamp {colors['green']}"></div>
    </div>
    """, unsafe_allow_html=True)

def countdown(sec):
    for i in range(sec, 0, -1):
        timer.markdown(f"<div class='timer'>{i} detik</div>", unsafe_allow_html=True)
        time.sleep(1)

if start:
    for _ in range(2):

        # MERAH
        show_lamp("red")
        countdown(40)

        # KUNING
        show_lamp("yellow")
        countdown(5)

        # HIJAU
        show_lamp("green")
        countdown(20)

    show_lamp("off")
    timer.markdown("<div class='timer'>🚦 Selesai</div>", unsafe_allow_html=True)
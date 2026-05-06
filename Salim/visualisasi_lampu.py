

import streamlit as st
import time

# ══════════════════════════════════════════════════════════════════
#  CIRCULAR LINKED LIST
# ══════════════════════════════════════════════════════════════════

class Node:
    def __init__(self, name, color_hex, duration, label):
        self.name      = name
        self.color_hex = color_hex
        self.duration  = duration
        self.label     = label
        self.next      = None

class CircularLinkedList:
    def __init__(self):
        self.head = self.tail = None
        self.size = 0

    def append(self, name, color_hex, duration, label):
        node = Node(name, color_hex, duration, label)
        if not self.head:
            self.head = self.tail = node
            node.next = node
        else:
            self.tail.next = node
            self.tail      = node
            node.next      = self.head
        self.size += 1

    def to_list(self):
        result, cur = [], self.head
        for _ in range(self.size):
            result.append(cur)
            cur = cur.next
        return result

def build_cll():
    cll = CircularLinkedList()
    cll.append("red",    "#FF2D2D", 40, "STOP!")
    cll.append("yellow", "#FFD600",  5, "SABAR BANG!")
    cll.append("green",  "#00E676", 20, "GASSS!")
    return cll

# ══════════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════════════════════════

st.set_page_config(page_title="🚦 Traffic Light", page_icon="🚦", layout="centered")

# ══════════════════════════════════════════════════════════════════
#  CSS
# ══════════════════════════════════════════════════════════════════

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;500;700&display=swap');

html, body, [class*="css"] {
    background: #07090d;
    font-family: 'Rajdhani', sans-serif;
    color: #dde8f0;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 520px; }

body::before {
    content:'';
    position:fixed; inset:0; z-index:-1;
    background:
        radial-gradient(ellipse 70% 45% at 50% 0%,   rgba(255,45,45,0.08)  0%, transparent 65%),
        radial-gradient(ellipse 70% 45% at 50% 100%, rgba(0,230,118,0.07)  0%, transparent 65%),
        repeating-linear-gradient(0deg,  transparent, transparent 50px, rgba(255,255,255,0.014) 51px),
        repeating-linear-gradient(90deg, transparent, transparent 50px, rgba(255,255,255,0.014) 51px),
        #07090d;
}

/* title */
.tl-title {
    font-family: 'Orbitron', monospace;
    font-size: clamp(1.1rem, 3.5vw, 1.65rem);
    font-weight: 900;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    text-align: center;
    color: #ffffff;
    text-shadow: 0 0 30px rgba(255,255,255,0.15);
    margin-bottom: 2px;
}
.tl-sub {
    font-size: 0.7rem;
    letter-spacing: 0.4em;
    text-transform: uppercase;
    text-align: center;
    color: rgba(221,232,240,0.25);
    margin-bottom: 1.8rem;
}

/* scene wrapper */
.scene { display:flex; flex-direction:column; align-items:center; }

/* top arm */
.pole-arm {
    width: 3px; height: 48px;
    background: linear-gradient(180deg, #2a2e3e, #1a1d28);
    border-radius: 2px;
}

/* housing */
.housing {
    width: 176px;
    background: linear-gradient(165deg, #1c2030 0%, #111420 55%, #0d0f1a 100%);
    border: 2px solid rgba(255,255,255,0.08);
    border-radius: 28px;
    padding: 24px 18px 20px;
    box-shadow:
        0 0 0 1px rgba(255,255,255,0.03),
        0 36px 90px rgba(0,0,0,0.9),
        inset 0 1px 0 rgba(255,255,255,0.08),
        inset 0 -1px 0 rgba(0,0,0,0.6);
    position: relative;
}
.housing::before, .housing::after {
    content:'';
    position:absolute;
    left:50%; transform:translateX(-50%);
    width:9px; height:9px;
    border-radius:50%;
    background:#181b28;
    border:1px solid rgba(255,255,255,0.09);
    box-shadow: inset 0 1px 3px rgba(0,0,0,0.9);
}
.housing::before { top:10px; }
.housing::after  { bottom:10px; }

/* divider between lamps */
.lamp-divider {
    width: 60%; height: 1px;
    background: rgba(255,255,255,0.05);
    margin: 0 auto;
}

/* lamp */
.lamp {
    width: 120px; height: 120px;
    border-radius: 50%;
    margin: 0 auto 14px;
    position: relative;
    background: rgba(0,0,0,0.5);
    border: 2.5px solid rgba(255,255,255,0.04);
    box-shadow: inset 0 6px 18px rgba(0,0,0,0.7);
    transition: all 0.45s cubic-bezier(0.4,0,0.2,1);
}
.lamp:last-child { margin-bottom:0; }

/* active lamps */
.lamp-red.ON {
    background: radial-gradient(circle at 36% 30%, #ff9090, #FF2D2D 50%, #7a0000 100%);
    border-color: rgba(255,50,50,0.5);
    box-shadow:
        0 0 30px 10px rgba(255,45,45,0.6),
        0 0 90px 25px rgba(255,45,45,0.2),
        inset 0 4px 12px rgba(255,180,180,0.2);
}
.lamp-yellow.ON {
    background: radial-gradient(circle at 36% 30%, #fff59d, #FFD600 50%, #6a5000 100%);
    border-color: rgba(255,214,0,0.5);
    box-shadow:
        0 0 30px 10px rgba(255,214,0,0.6),
        0 0 90px 25px rgba(255,214,0,0.2),
        inset 0 4px 12px rgba(255,255,180,0.2);
    animation: blink 0.75s ease-in-out infinite;
}
.lamp-green.ON {
    background: radial-gradient(circle at 36% 30%, #80ffb8, #00E676 50%, #003d1a 100%);
    border-color: rgba(0,230,118,0.5);
    box-shadow:
        0 0 30px 10px rgba(0,230,118,0.6),
        0 0 90px 25px rgba(0,230,118,0.2),
        inset 0 4px 12px rgba(180,255,210,0.2);
}

@keyframes blink {
    0%,100%{ opacity:1; } 50%{ opacity:0.4; }
}

/* glare */
.lamp::after {
    content:'';
    position:absolute;
    top:18px; left:22px;
    width:28px; height:16px;
    border-radius:50%;
    background:rgba(255,255,255,0.22);
    filter:blur(5px);
    opacity:0;
    transition:opacity 0.45s;
}
.lamp.ON::after { opacity:1; }

/* pole */
.pole-body {
    width:20px; height:68px;
    background: linear-gradient(90deg, #232638 0%, #191c28 45%, #232638 100%);
    border-left:  1px solid rgba(255,255,255,0.05);
    border-right: 1px solid rgba(0,0,0,0.4);
}
.pole-base {
    width:88px; height:15px;
    background: linear-gradient(180deg, #1e2232, #111420);
    border-radius:8px;
    border:1px solid rgba(255,255,255,0.06);
    box-shadow:0 6px 20px rgba(0,0,0,0.7);
}

/* status */
.status-wrap { text-align:center; margin:1.8rem 0 0; }
.status-label {
    font-family:'Orbitron', monospace;
    font-size: clamp(1.5rem, 5vw, 2.1rem);
    font-weight:700;
    letter-spacing:0.18em;
    display:block;
    transition:color 0.4s;
}
.status-hint {
    font-size:0.7rem;
    letter-spacing:0.35em;
    text-transform:uppercase;
    color:rgba(221,232,240,0.28);
    margin-top:3px;
}

/* ring */
.ring-outer {
    position:relative;
    width:168px; height:168px;
    margin:1.5rem auto 0;
}
.ring-outer svg { transform:rotate(-90deg); }
.ring-center {
    position:absolute; inset:0;
    display:flex; flex-direction:column;
    align-items:center; justify-content:center;
}
.ring-num {
    font-family:'Orbitron', monospace;
    font-size:3rem;
    font-weight:900;
    line-height:1;
    transition:color 0.4s;
}
.ring-unit {
    font-size:0.62rem;
    letter-spacing:0.3em;
    text-transform:uppercase;
    color:rgba(221,232,240,0.28);
    margin-top:4px;
}

/* phase pills */
.phase-strip {
    display:flex;
    justify-content:center;
    gap:10px;
    margin:1.6rem auto 0;
    max-width:400px;
}
.phase-pill {
    flex:1;
    padding:11px 6px;
    border-radius:14px;
    text-align:center;
    background:rgba(255,255,255,0.03);
    border:1.5px solid rgba(255,255,255,0.07);
    transition:all 0.35s;
}
.phase-pill.act {
    box-shadow:0 0 14px 2px currentColor, inset 0 0 10px rgba(255,255,255,0.03);
    background:rgba(255,255,255,0.055);
}
.pill-dur {
    font-family:'Orbitron', monospace;
    font-size:1.05rem;
    font-weight:700;
    display:block;
}
.pill-name {
    font-size:0.6rem;
    letter-spacing:0.22em;
    text-transform:uppercase;
    color:rgba(221,232,240,0.35);
    display:block;
    margin-top:2px;
}

/* progress bar */
.pbar-track {
    height:5px;
    background:rgba(255,255,255,0.05);
    border-radius:3px;
    overflow:hidden;
    margin:1.3rem auto 0;
    max-width:400px;
}
.pbar-fill {
    height:100%;
    border-radius:3px;
    transition:width 0.9s linear;
}

/* cycle */
.cycle-badge {
    text-align:center;
    margin-top:0.9rem;
    font-size:0.67rem;
    letter-spacing:0.28em;
    text-transform:uppercase;
    color:rgba(221,232,240,0.2);
}
.cycle-badge span {
    font-family:'Orbitron', monospace;
    font-size:0.78rem;
    color:rgba(221,232,240,0.42);
}

/* buttons */
.stButton > button {
    width:100% !important;
    font-family:'Orbitron', monospace !important;
    font-size:0.67rem !important;
    font-weight:700 !important;
    letter-spacing:0.2em !important;
    text-transform:uppercase !important;
    border-radius:12px !important;
    padding:0.65rem !important;
    background:rgba(255,255,255,0.04) !important;
    border:1px solid rgba(255,255,255,0.09) !important;
    color:rgba(221,232,240,0.7) !important;
    transition:all 0.2s !important;
}
.stButton > button:hover {
    background:rgba(255,255,255,0.09) !important;
    border-color:rgba(255,255,255,0.22) !important;
    color:#fff !important;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  SESSION STATE
# ══════════════════════════════════════════════════════════════════

cll   = build_cll()
nodes = cll.to_list()   # siklus: [red, green, yellow]

# Urutan FISIK lampu di housing (atas → bawah)
DISPLAY = ["red", "yellow", "green"]

if "running" not in st.session_state: st.session_state.running = False
if "nidx"    not in st.session_state: st.session_state.nidx    = 0
if "elapsed" not in st.session_state: st.session_state.elapsed = 0
if "cycle"   not in st.session_state: st.session_state.cycle   = 1

cur      = nodes[st.session_state.nidx]
remain   = cur.duration - st.session_state.elapsed
progress = st.session_state.elapsed / cur.duration

# ══════════════════════════════════════════════════════════════════
#  RENDER
# ══════════════════════════════════════════════════════════════════

st.markdown('<p class="tl-title">🚦 Simulasi Lampu Lalu Lintas</p>', unsafe_allow_html=True)
st.markdown('<p class="tl-sub">Struktur Data · UINSSC</p>', unsafe_allow_html=True)

# ── Traffic Light ─────────────────────────────────────
light_ph = st.empty()

def render_light(active):
    lamps = ""
    for i, name in enumerate(DISPLAY):
        on = "ON" if name == active else ""
        lamps += f'<div class="lamp lamp-{name} {on}"></div>'
        if i < len(DISPLAY) - 1:
            lamps += '<div class="lamp-divider"></div>'
    return f"""
    <div class="scene">
        <div class="pole-arm"></div>
        <div class="housing">{lamps}</div>
        <div class="pole-body"></div>
        <div class="pole-base"></div>
    </div>
    """

light_ph.markdown(render_light(cur.name), unsafe_allow_html=True)

# ── Status ────────────────────────────────────────────
status_ph = st.empty()
status_ph.markdown(f"""
<div class="status-wrap">
    <span class="status-label" style="color:{cur.color_hex};">{cur.label}</span>
</div>
""", unsafe_allow_html=True)

# ── Ring Timer ────────────────────────────────────────
timer_ph = st.empty()

def render_ring(remaining, total, color):
    R   = 72
    C   = 2 * 3.14159265 * R
    off = C * (1 - remaining / total)
    return f"""
    <div class="ring-outer">
        <svg width="168" height="168" viewBox="0 0 168 168">
            <circle cx="84" cy="84" r="{R}"
                fill="none" stroke="rgba(255,255,255,0.06)" stroke-width="9"/>
            <circle cx="84" cy="84" r="{R}"
                fill="none" stroke="{color}" stroke-width="9"
                stroke-linecap="round"
                stroke-dasharray="{C:.3f}"
                stroke-dashoffset="{off:.3f}"/>
        </svg>
        <div class="ring-center">
            <span class="ring-num" style="color:{color};">{remaining}</span>
            <span class="ring-unit">detik</span>
        </div>
    </div>
    """

timer_ph.markdown(render_ring(remain, cur.duration, cur.color_hex), unsafe_allow_html=True)

# ── Phase Pills ───────────────────────────────────────
pills_ph = st.empty()

def render_pills(active_name):
    data = [
        ("red",    "#FF2D2D", "40s", ""),
        ("yellow", "#FFD600",  "5s", ""),
        ("green",  "#00E676", "20s", ""),
    ]
    html = '<div class="phase-strip">'
    for name, color, dur, label in data:
        act = "act" if name == active_name else ""
        c   = color if name == active_name else "rgba(221,232,240,0.38)"
        style = f'style="color:{color};"' if name == active_name else ""
        html += f"""
        <div class="phase-pill {act}" {style}>
            <span class="pill-dur" style="color:{c};">{dur}</span>
            <span class="pill-name">{label}</span>
        </div>"""
    html += '</div>'
    return html

pills_ph.markdown(render_pills(cur.name), unsafe_allow_html=True)

# ── Progress Bar ──────────────────────────────────────
prog_ph = st.empty()
prog_ph.markdown(f"""
<div class="pbar-track">
    <div class="pbar-fill" style="width:{int(progress*100)}%;
        background:{cur.color_hex};
        box-shadow:0 0 10px 2px {cur.color_hex}77;"></div>
</div>
""", unsafe_allow_html=True)

# ── Cycle ─────────────────────────────────────────────
cycle_ph = st.empty()
cycle_ph.markdown(f'<p class="cycle-badge">Putaran ke-<span>{st.session_state.cycle}</span></p>', unsafe_allow_html=True)

# ── Controls ──────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("▶ Mulai"):
        st.session_state.running = True
with c2:
    if st.button("⏸ Jeda"):
        st.session_state.running = False
with c3:
    if st.button("↺ Reset"):
        st.session_state.running = False
        st.session_state.nidx    = 0
        st.session_state.elapsed = 0
        st.session_state.cycle   = 1
        st.rerun()

# ══════════════════════════════════════════════════════════════════
#  AUTO-TICK
# ══════════════════════════════════════════════════════════════════

if st.session_state.running:
    time.sleep(1)
    st.session_state.elapsed += 1

    if st.session_state.elapsed >= nodes[st.session_state.nidx].duration:
        st.session_state.elapsed = 0
        nxt = (st.session_state.nidx + 1) % len(nodes)
        if nxt == 0:
            st.session_state.cycle += 1
        st.session_state.nidx = nxt

    st.rerun()
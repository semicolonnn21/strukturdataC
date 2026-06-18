import streamlit as st
import time
import math

# ─────────────────────────────────────────────
#  CIRCULAR LINKED LIST
# ─────────────────────────────────────────────
class Node:
    def __init__(self, color: str, duration: int, label: str):
        self.color = color
        self.duration = duration
        self.label = label
        self.next = None

class CircularLinkedList:
    def __init__(self):
        self.head = None
        self._current = None

    def append(self, color: str, duration: int, label: str):
        new_node = Node(color, duration, label)
        if not self.head:
            self.head = new_node
            new_node.next = self.head
            self._current = self.head
        else:
            temp = self.head
            while temp.next != self.head:
                temp = temp.next
            temp.next = new_node
            new_node.next = self.head

    @property
    def current(self):
        return self._current

    def advance(self):
        self._current = self._current.next

    def to_list(self):
        result, temp = [], self.head
        while True:
            result.append(temp)
            temp = temp.next
            if temp == self.head:
                break
        return result

# ─────────────────────────────────────────────
#  BUILD THE CLL  — urutan: Merah → Kuning → Hijau
# ─────────────────────────────────────────────
@st.cache_resource
def build_cll():
    cll = CircularLinkedList()
    cll.append("#FF2D2D", 40, "MERAH")
    cll.append("#FFD600",  5, "KUNING")   # ← Kuning sekarang urutan ke-2
    cll.append("#00C853", 20, "HIJAU")    # ← Hijau urutan ke-3
    return cll

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Traffic Light – Struktur Data",
    page_icon="🚦",
    layout="wide",
)

# ─────────────────────────────────────────────
#  GLOBAL CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap');

html, body, [class*="css"] {
    font-family: 'Share Tech Mono', monospace;
    background-color: #0a0a0f;
    color: #e0e0e0;
}

.stApp {
    background: radial-gradient(ellipse at 20% 0%, #0d1a2e 0%, #0a0a0f 60%);
}

.hero-title {
    font-family: 'Orbitron', monospace;
    font-size: clamp(1.6rem, 4vw, 2.8rem);
    font-weight: 900;
    letter-spacing: 0.12em;
    text-align: center;
    background: linear-gradient(135deg, #FF2D2D 0%, #FFD600 50%, #00C853 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.2rem;
    text-transform: uppercase;
}
.hero-sub {
    text-align: center;
    font-size: 0.75rem;
    letter-spacing: 0.35em;
    color: #4a5568;
    text-transform: uppercase;
    margin-bottom: 2rem;
}

.tl-housing {
    background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    border: 2px solid #2d3748;
    border-radius: 2rem;
    padding: 2rem 1.5rem;
    width: 180px;
    margin: 0 auto;
    box-shadow:
        0 0 40px rgba(0,0,0,0.8),
        inset 0 0 20px rgba(255,255,255,0.03);
    position: relative;
}
.tl-housing::before {
    content: '';
    position: absolute;
    top: -1px; left: 30px; right: 30px;
    height: 14px;
    background: #2d3748;
    border-radius: 0 0 8px 8px;
}

.bulb-wrap {
    display: flex;
    justify-content: center;
    margin: 0.9rem 0;
}
.bulb {
    width: 90px;
    height: 90px;
    border-radius: 50%;
    border: 3px solid #1a202c;
    transition: all 0.4s ease;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.6rem;
}
.bulb.off {
    background: #0f0f18;
    box-shadow: inset 0 0 20px rgba(0,0,0,0.9);
    opacity: 0.25;
}
.bulb.red-on {
    background: radial-gradient(circle at 35% 35%, #ff6b6b, #FF2D2D 50%, #8b0000);
    box-shadow:
        0 0 30px #FF2D2D,
        0 0 60px rgba(255,45,45,0.5),
        0 0 100px rgba(255,45,45,0.2),
        inset 0 0 20px rgba(255,100,100,0.3);
    opacity: 1;
}
.bulb.yellow-on {
    background: radial-gradient(circle at 35% 35%, #fff176, #FFD600 50%, #7a6500);
    box-shadow:
        0 0 30px #FFD600,
        0 0 60px rgba(255,214,0,0.5),
        0 0 100px rgba(255,214,0,0.2),
        inset 0 0 20px rgba(255,230,100,0.3);
    opacity: 1;
}
.bulb.green-on {
    background: radial-gradient(circle at 35% 35%, #69f0ae, #00C853 50%, #004d20);
    box-shadow:
        0 0 30px #00C853,
        0 0 60px rgba(0,200,83,0.5),
        0 0 100px rgba(0,200,83,0.2),
        inset 0 0 20px rgba(100,255,150,0.3);
    opacity: 1;
}

.status-badge {
    display: inline-block;
    padding: 0.35rem 1.2rem;
    border-radius: 999px;
    font-family: 'Orbitron', monospace;
    font-size: 0.9rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
}

.cll-node {
    display: inline-flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
    padding: 0.6rem 1rem;
    border-radius: 0.75rem;
    border: 1px solid;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.8rem;
    min-width: 80px;
    text-align: center;
    transition: all 0.3s ease;
}
.cll-node .node-color-dot {
    width: 16px;
    height: 16px;
    border-radius: 50%;
    margin: 0 auto;
}
.cll-arrow {
    font-size: 1.2rem;
    color: #4a5568;
    display: flex;
    align-items: center;
    padding: 0 4px;
}

.info-card {
    background: linear-gradient(135deg, #0d1a2e, #0a0f1e);
    border: 1px solid #1e3a5f;
    border-radius: 0.75rem;
    padding: 1.2rem;
    margin-bottom: 0.75rem;
}
.info-card h4 {
    font-family: 'Orbitron', monospace;
    font-size: 0.7rem;
    color: #4a90d9;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin: 0 0 0.5rem;
}
.info-card p {
    font-size: 0.85rem;
    color: #a0aec0;
    margin: 0;
    line-height: 1.6;
}

.log-line {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.78rem;
    padding: 0.3rem 0.6rem;
    border-left: 2px solid;
    margin-bottom: 0.4rem;
    border-radius: 0 4px 4px 0;
}

div[data-testid="column"] button {
    font-family: 'Orbitron', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.15em !important;
    border-radius: 0.5rem !important;
}

hr { border-color: #1a2535 !important; }
#MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  INIT STATE
# ─────────────────────────────────────────────
cll = build_cll()

if "tick"      not in st.session_state: st.session_state.tick      = 0
if "running"   not in st.session_state: st.session_state.running   = False
if "phase_idx" not in st.session_state: st.session_state.phase_idx = 0
if "elapsed"   not in st.session_state: st.session_state.elapsed   = 0
if "log"       not in st.session_state: st.session_state.log       = []
if "speed"     not in st.session_state: st.session_state.speed     = 1.0

node_list    = cll.to_list()
n            = len(node_list)
current_node = node_list[st.session_state.phase_idx % n]
remaining    = current_node.duration - st.session_state.elapsed

# ─────────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────────
st.markdown('<div class="hero-title">🚦 Traffic Light Simulator</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Struktur Data · Circular Linked List · Informatika UINSSC MMXXVI</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  MAIN LAYOUT
# ─────────────────────────────────────────────
col_l, col_c, col_r = st.columns([1, 1.4, 1], gap="large")

# ── LEFT ────────────────────────────────────
with col_l:
    st.markdown("### ⚙️ Controls")

    btn_col1, btn_col2, btn_col3 = st.columns(3)
    with btn_col1:
        if st.button("▶ START", use_container_width=True):
            st.session_state.running = True
    with btn_col2:
        if st.button("⏸ PAUSE", use_container_width=True):
            st.session_state.running = False
    with btn_col3:
        if st.button("↺ RESET", use_container_width=True):
            st.session_state.running   = False
            st.session_state.phase_idx = 0
            st.session_state.elapsed   = 0
            st.session_state.tick      = 0
            st.session_state.log       = []
            st.rerun()

    st.markdown("---")
    st.markdown("**🕐 Simulation Speed**")
    speed = st.slider("", 0.5, 5.0, st.session_state.speed, 0.5,
                      format="%.1fx", label_visibility="collapsed")
    st.session_state.speed = speed

    st.markdown("---")
    st.markdown("""
    <div class="info-card">
        <h4>📋 Durasi Fase</h4>
        <p>🔴 Merah &nbsp;→ 40 detik<br>
           🟡 Kuning → 5 detik<br>
           🟢 Hijau &nbsp;&nbsp;→ 20 detik</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-card">
        <h4>🔗 Struktur Data</h4>
        <p>Circular Linked List dengan 3 node yang saling terhubung membentuk siklus tak berujung.</p>
    </div>
    """, unsafe_allow_html=True)

    cycle_time   = sum(nd.duration for nd in node_list)
    total_cycles = st.session_state.tick // cycle_time if cycle_time else 0
    st.markdown(f"""
    <div class="info-card">
        <h4>📊 Statistik</h4>
        <p>Total detik berjalan: <b>{st.session_state.tick}</b><br>
           Siklus selesai: <b>{total_cycles}</b><br>
           Fase saat ini: <b>{current_node.label}</b></p>
    </div>
    """, unsafe_allow_html=True)

# ── CENTER ───────────────────────────────────
with col_c:
    color_map = {
        "MERAH":  ("red-on",    "🔴", "#FF2D2D"),
        "KUNING": ("yellow-on", "🟡", "#FFD600"),
        "HIJAU":  ("green-on",  "🟢", "#00C853"),
    }

    def bulb_class(label):
        return color_map[label][0] if label == current_node.label else "off"

    # Urutan render: MERAH (atas) → KUNING (tengah) → HIJAU (bawah)
    red_cls    = bulb_class("MERAH")
    yellow_cls = bulb_class("KUNING")
    green_cls  = bulb_class("HIJAU")

    _, cur_icon, cur_hex = color_map[current_node.label]

    # SVG ring countdown
    pct   = remaining / current_node.duration if current_node.duration else 1
    R     = 70
    cx = cy = 80
    circ  = 2 * math.pi * R
    dash  = pct * circ
    gap   = circ - dash

    svg_ring = f"""
    <svg width="160" height="160" viewBox="0 0 160 160" style="display:block;margin:0 auto;">
      <circle cx="{cx}" cy="{cy}" r="{R}"
              fill="none" stroke="#1a2535" stroke-width="10"/>
      <circle cx="{cx}" cy="{cy}" r="{R}"
              fill="none"
              stroke="{cur_hex}"
              stroke-width="10"
              stroke-linecap="round"
              stroke-dasharray="{dash:.2f} {gap:.2f}"
              transform="rotate(-90 {cx} {cy})"
              style="filter:drop-shadow(0 0 6px {cur_hex});transition:all 0.8s ease;"/>
      <text x="{cx}" y="{cy - 8}" text-anchor="middle"
            fill="{cur_hex}"
            font-family="Orbitron,monospace"
            font-size="32" font-weight="900">{remaining}</text>
      <text x="{cx}" y="{cy + 18}" text-anchor="middle"
            fill="#4a5568"
            font-family="Share Tech Mono,monospace"
            font-size="11">DETIK</text>
    </svg>
    """

    housing_html = f"""
    <div style="text-align:center;">
      <div class="tl-housing">
        <div class="bulb-wrap"><div class="bulb {red_cls}"></div></div>
        <div class="bulb-wrap"><div class="bulb {yellow_cls}"></div></div>
        <div class="bulb-wrap"><div class="bulb {green_cls}"></div></div>
      </div>
      <div style="margin-top:1.5rem;">{svg_ring}</div>
      <div style="margin-top:1rem;">
        <span class="status-badge"
              style="background:rgba({','.join(str(int(cur_hex.lstrip('#')[i:i+2],16)) for i in (0,2,4))},0.15);
                     border:1px solid {cur_hex};
                     color:{cur_hex};">
          {cur_icon} {current_node.label}
        </span>
      </div>
    </div>
    """
    st.markdown(housing_html, unsafe_allow_html=True)

# ── RIGHT ────────────────────────────────────
with col_r:
    st.markdown("### 🔗 Circular Linked List")

    nodes = cll.to_list()
    node_colors_hex = {"MERAH": "#FF2D2D", "KUNING": "#FFD600", "HIJAU": "#00C853"}
    node_html = '<div style="display:flex;flex-direction:column;align-items:center;gap:6px;">'

    for i, nd in enumerate(nodes):
        is_active = (nd.label == current_node.label)
        hex_c  = node_colors_hex[nd.label]
        bg     = f"rgba({','.join(str(int(hex_c.lstrip('#')[j:j+2],16)) for j in (0,2,4))}, 0.15)"
        border = hex_c if is_active else "#2d3748"
        scale  = "transform:scale(1.08);" if is_active else ""
        glow   = f"box-shadow:0 0 16px {hex_c}80;" if is_active else ""

        node_html += f"""
        <div class="cll-node"
             style="background:{bg};border-color:{border};{scale}{glow}">
          <div class="node-color-dot" style="background:{hex_c};
               {'box-shadow:0 0 8px '+hex_c+';' if is_active else ''}"></div>
          <b style="color:{hex_c if is_active else '#e2e8f0'};">{nd.label}</b>
          <span style="color:#718096;font-size:0.7rem;">{nd.duration}s → next</span>
        </div>
        """
        if i < len(nodes) - 1:
            node_html += '<div class="cll-arrow">↓</div>'

    node_html += '<div class="cll-arrow" style="color:#4a5568;">↺ (back to HEAD)</div>'
    node_html += '</div>'
    st.markdown(node_html, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📜 Event Log")

    if not st.session_state.log:
        st.markdown('<p style="color:#4a5568;font-size:0.8rem;">Tekan START untuk memulai...</p>',
                    unsafe_allow_html=True)
    else:
        for entry in reversed(st.session_state.log[-8:]):
            col_hex = node_colors_hex.get(entry["phase"], "#718096")
            bg_log  = f"rgba({','.join(str(int(col_hex.lstrip('#')[j:j+2],16)) for j in (0,2,4))}, 0.1)"
            st.markdown(
                f'<div class="log-line" style="border-color:{col_hex};background:{bg_log};">'
                f'<span style="color:#4a5568;">[{entry["t"]:04d}s]</span> '
                f'<span style="color:{col_hex};">▶ {entry["phase"]}</span> '
                f'<span style="color:#718096;">{entry["msg"]}</span></div>',
                unsafe_allow_html=True
            )

# ─────────────────────────────────────────────
#  TICK ENGINE
# ─────────────────────────────────────────────
if st.session_state.running:
    sleep_s = max(0.1, 1.0 / st.session_state.speed)
    time.sleep(sleep_s)

    st.session_state.elapsed += 1
    st.session_state.tick    += 1

    if st.session_state.elapsed >= current_node.duration:
        st.session_state.log.append({
            "t":     st.session_state.tick,
            "phase": current_node.label,
            "msg":   f"selesai ({current_node.duration}s) → advance"
        })
        st.session_state.elapsed   = 0
        st.session_state.phase_idx = (st.session_state.phase_idx + 1) % n

    st.rerun()
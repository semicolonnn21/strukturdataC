import streamlit as st
import time

# ── Circular Linked List ──────────────────────
class Node:
    def __init__(self, label, duration, color, emoji):
        self.label    = label
        self.duration = duration
        self.color    = color
        self.emoji    = emoji
        self.next     = None

class CircularLinkedList:
    def __init__(self):
        self.head = None

    def append(self, label, duration, color, emoji):
        node = Node(label, duration, color, emoji)
        if not self.head:
            self.head = node
            node.next = self.head
        else:
            t = self.head
            while t.next != self.head:
                t = t.next
            t.next = node
            node.next = self.head

    def to_list(self):
        result, t = [], self.head
        while True:
            result.append(t)
            t = t.next
            if t == self.head:
                break
        return result

@st.cache_resource
def build_cll():
    cll = CircularLinkedList()
    cll.append("MERAH",  40, "#ff3333", "🔴")
    cll.append("KUNING",  5, "#facc15", "🟡")
    cll.append("HIJAU",  20, "#22c55e", "🟢")
    return cll

# ── Page Setup ────────────────────────────────
st.set_page_config(page_title="Traffic Light", page_icon="🚦", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Bebas+Neue&display=swap');

html, body, [class*="css"] {
    background: #111318 !important;
    font-family: 'Rajdhani', sans-serif;
    color: #e2e8f0;
}
.stApp { background: #111318 !important; }
#MainMenu, footer { visibility: hidden; }

/* ── HEADER ── */
.title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.4rem;
    text-align: center;
    letter-spacing: 0.12em;
    color: #f1f5f9;
    margin-bottom: 0;
    line-height: 1;
}
.subtitle {
    text-align: center;
    font-size: 0.72rem;
    color: #475569;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    margin-bottom: 2rem;
}

/* ── MAIN CARD ── */
.main-card {
    background: linear-gradient(160deg, #1e2130 0%, #161926 100%);
    border: 1px solid #2a2f45;
    border-radius: 24px;
    padding: 2rem 1.5rem;
    max-width: 340px;
    margin: 0 auto 1.5rem;
    box-shadow:
        0 20px 60px rgba(0,0,0,0.5),
        0 1px 0 rgba(255,255,255,0.04) inset;
}

/* ── HOUSING ── */
.housing-outer {
    background: linear-gradient(180deg, #0d0f18 0%, #181c2e 100%);
    border: 2px solid #252840;
    border-radius: 28px;
    padding: 20px 28px;
    width: 130px;
    margin: 0 auto 1.5rem;
    box-shadow:
        0 8px 32px rgba(0,0,0,0.6),
        0 0 0 1px rgba(255,255,255,0.03) inset;
    display: flex;
    flex-direction: column;
    gap: 16px;
    position: relative;
}
/* mounting bracket */
.housing-outer::before,
.housing-outer::after {
    content: '';
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    width: 30px;
    height: 8px;
    background: #1e2235;
    border: 1px solid #2a2f45;
    border-radius: 4px;
}
.housing-outer::before { top: -9px; }
.housing-outer::after  { bottom: -9px; }

.bulb-slot {
    width: 74px;
    height: 74px;
    border-radius: 50%;
    margin: 0 auto;
    position: relative;
    background: #0a0b10;
    border: 2px solid #1e2235;
    box-shadow: inset 0 2px 8px rgba(0,0,0,0.8);
    transition: all 0.4s ease;
    display: flex;
    align-items: center;
    justify-content: center;
}
/* reflection highlight */
.bulb-slot::after {
    content: '';
    position: absolute;
    top: 10px; left: 12px;
    width: 22px; height: 14px;
    border-radius: 50%;
    background: rgba(255,255,255,0.0);
    transition: background 0.4s ease;
}

/* OFF state */
.bulb-off { background: #0e0f18; }

/* ON states */
.bulb-red {
    background: radial-gradient(circle at 38% 32%, #ff8080, #ff3333 55%, #7a0000);
    border-color: #ff333355;
    box-shadow:
        inset 0 2px 8px rgba(0,0,0,0.4),
        0 0 24px rgba(255,51,51,0.6),
        0 0 60px rgba(255,51,51,0.25);
}
.bulb-red::after { background: rgba(255,255,255,0.18); }

.bulb-yellow {
    background: radial-gradient(circle at 38% 32%, #fef08a, #facc15 55%, #7a5f00);
    border-color: #facc1555;
    box-shadow:
        inset 0 2px 8px rgba(0,0,0,0.4),
        0 0 24px rgba(250,204,21,0.6),
        0 0 60px rgba(250,204,21,0.25);
}
.bulb-yellow::after { background: rgba(255,255,255,0.18); }

.bulb-green {
    background: radial-gradient(circle at 38% 32%, #86efac, #22c55e 55%, #064e20);
    border-color: #22c55e55;
    box-shadow:
        inset 0 2px 8px rgba(0,0,0,0.4),
        0 0 24px rgba(34,197,94,0.6),
        0 0 60px rgba(34,197,94,0.25);
}
.bulb-green::after { background: rgba(255,255,255,0.18); }

/* ── PHASE BADGE ── */
.phase-badge {
    text-align: center;
    margin-bottom: 1rem;
}
.phase-name {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2rem;
    letter-spacing: 0.1em;
    line-height: 1;
}
.phase-dur {
    font-size: 0.7rem;
    color: #64748b;
    letter-spacing: 0.15em;
    text-transform: uppercase;
}

/* ── TIMER ── */
.timer-wrap {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    margin-bottom: 0.8rem;
}
.timer-num {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 3.8rem;
    line-height: 1;
    letter-spacing: 0.05em;
}
.timer-unit {
    font-size: 0.75rem;
    color: #64748b;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    align-self: flex-end;
    padding-bottom: 0.5rem;
}

/* ── PROGRESS BAR ── */
.bar-track {
    height: 5px;
    background: #1e2235;
    border-radius: 99px;
    overflow: hidden;
    margin-bottom: 1.5rem;
}
.bar-fill {
    height: 100%;
    border-radius: 99px;
    transition: width 0.85s ease;
}

/* ── CLL ROW ── */
.cll-wrap {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
}
.cll-node {
    padding: 5px 10px;
    border-radius: 8px;
    border: 1.5px solid;
    font-size: 0.72rem;
    font-weight: 600;
    text-align: center;
    line-height: 1.6;
    min-width: 68px;
    letter-spacing: 0.04em;
    transition: all 0.3s ease;
}
.cll-node.active { transform: translateY(-3px); }
.cll-sep { color: #334155; font-size: 0.9rem; }

/* ── STATS ROW ── */
.stats-row {
    display: flex;
    justify-content: space-around;
    margin: 1rem 0 0.5rem;
    padding-top: 1rem;
    border-top: 1px solid #1e2235;
}
.stat-item { text-align: center; }
.stat-val {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.5rem;
    letter-spacing: 0.06em;
    line-height: 1;
}
.stat-lbl {
    font-size: 0.65rem;
    color: #475569;
    letter-spacing: 0.14em;
    text-transform: uppercase;
}

/* ── STATUS DOT ── */
.status-dot {
    display: inline-block;
    width: 8px; height: 8px;
    border-radius: 50%;
    margin-right: 6px;
    vertical-align: middle;
}

/* ── CONTROLS ── */
div[data-testid="column"] button {
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.06em !important;
    border-radius: 10px !important;
    background: #1e2235 !important;
    color: #94a3b8 !important;
    border: 1px solid #2a2f45 !important;
    transition: all 0.2s ease !important;
}
div[data-testid="column"] button:hover {
    background: #252a42 !important;
    color: #e2e8f0 !important;
}

/* slider */
.stSlider { padding: 0 4px; }
</style>
""", unsafe_allow_html=True)

# ── State ─────────────────────────────────────
cll   = build_cll()
nodes = cll.to_list()   # MERAH → KUNING → HIJAU
N     = len(nodes)

for k, v in [("running",False),("phase",0),("elapsed",0),("tick",0),("speed",1.0)]:
    if k not in st.session_state:
        st.session_state[k] = v

cur       = nodes[st.session_state.phase % N]
remaining = cur.duration - st.session_state.elapsed
pct       = remaining / cur.duration

bulb_class = {"MERAH": "bulb-red", "KUNING": "bulb-yellow", "HIJAU": "bulb-green"}

def bulb_html(label):
    cls = bulb_class[label] if label == cur.label else "bulb-off"
    return f'<div class="bulb-slot {cls}"></div>'

# ── Header ────────────────────────────────────
st.markdown('<div class="title">Traffic Light</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Circular Linked List · Struktur Data · UINSSC</div>', unsafe_allow_html=True)

# ── Main Card ─────────────────────────────────
bar_w = int(pct * 100)
cycle_total = sum(n.duration for n in nodes)
loops = st.session_state.tick // cycle_total if cycle_total else 0

# Phase badge
st.markdown(f"""
<div class="main-card">

  <!-- Traffic light: MERAH atas, KUNING tengah, HIJAU bawah -->
  <div class="housing-outer">
    {bulb_html("MERAH")}
    {bulb_html("KUNING")}
    {bulb_html("HIJAU")}
  </div>

  <!-- Phase name -->
  <div class="phase-badge">
    <div class="phase-name" style="color:{cur.color};">{cur.emoji} {cur.label}</div>
    <div class="phase-dur">Durasi fase: {cur.duration} detik</div>
  </div>

  <!-- Timer -->
  <div class="timer-wrap">
    <span class="timer-num" style="color:{cur.color};">{remaining:02d}</span>
    <span class="timer-unit">detik<br>tersisa</span>
  </div>

  <!-- Progress bar -->
  <div class="bar-track">
    <div class="bar-fill" style="width:{bar_w}%;background:{cur.color};
         box-shadow:0 0 8px {cur.color}88;"></div>
  </div>

  <!-- CLL diagram -->
  <div class="cll-wrap">
""", unsafe_allow_html=True)

# build CLL nodes
cll_html = ""
for i, nd in enumerate(nodes):
    active = nd.label == cur.label
    bg = f"{nd.color}20" if active else "#1a1e2e"
    shadow = f"box-shadow:0 0 12px {nd.color}55;" if active else ""
    cll_html += f"""
    <div class="cll-node {'active' if active else ''}"
         style="border-color:{nd.color if active else '#2a2f45'};
                color:{nd.color if active else '#475569'};
                background:{bg};{shadow}">
      {nd.emoji}<br>{nd.label}<br>
      <span style="color:#334155;">{nd.duration}s</span>
    </div>
    <span class="cll-sep">{"↺" if i == N-1 else "→"}</span>
    """

st.markdown(cll_html, unsafe_allow_html=True)

# Stats row + close card
status_color = "#22c55e" if st.session_state.running else "#475569"
status_text  = "BERJALAN" if st.session_state.running else "BERHENTI"

st.markdown(f"""
  </div><!-- end cll-wrap -->

  <!-- Stats -->
  <div class="stats-row">
    <div class="stat-item">
      <div class="stat-val" style="color:#94a3b8;">{st.session_state.tick:04d}</div>
      <div class="stat-lbl">Total Detik</div>
    </div>
    <div class="stat-item">
      <div class="stat-val" style="color:#94a3b8;">{loops}</div>
      <div class="stat-lbl">Siklus</div>
    </div>
    <div class="stat-item">
      <div class="stat-val" style="color:{status_color};">
        <span class="status-dot" style="background:{status_color};
              box-shadow:0 0 6px {status_color};"></span>{status_text}
      </div>
      <div class="stat-lbl">Status</div>
    </div>
  </div>

</div><!-- end main-card -->
""", unsafe_allow_html=True)

# ── Controls ──────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
with c1:
    if st.button("▶  Start", use_container_width=True):
        st.session_state.running = True
with c2:
    if st.button("⏸  Pause", use_container_width=True):
        st.session_state.running = False
with c3:
    if st.button("⏭  Skip", use_container_width=True):
        st.session_state.elapsed = 0
        st.session_state.phase   = (st.session_state.phase + 1) % N
        st.rerun()
with c4:
    if st.button("↺  Reset", use_container_width=True):
        st.session_state.running = False
        st.session_state.phase   = 0
        st.session_state.elapsed = 0
        st.session_state.tick    = 0
        st.rerun()

st.session_state.speed = st.slider(
    "Kecepatan simulasi", 0.5, 5.0,
    st.session_state.speed, 0.5, format="%.1fx"
)

# ── Tick ──────────────────────────────────────
if st.session_state.running:
    time.sleep(max(0.1, 1.0 / st.session_state.speed))
    st.session_state.elapsed += 1
    st.session_state.tick    += 1
    if st.session_state.elapsed >= cur.duration:
        st.session_state.elapsed = 0
        st.session_state.phase   = (st.session_state.phase + 1) % N
    st.rerun()
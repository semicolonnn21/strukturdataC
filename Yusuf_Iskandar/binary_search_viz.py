import streamlit as st
import time
import random

# ─────────────────────────────────────────────
#  Page config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Binary Search Visualizer",
    page_icon="🔍",
    layout="wide",
)

# ─────────────────────────────────────────────
#  Custom CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Space+Grotesk:wght@300;600;800&display=swap');

  html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }

  .main { background: #0d0f1a; }

  h1 { 
    font-size: 2.6rem !important; 
    font-weight: 800 !important;
    background: linear-gradient(135deg, #00f5c4, #7b61ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -1px;
  }

  .bar-container {
    display: flex;
    align-items: flex-end;
    justify-content: center;
    gap: 4px;
    padding: 20px;
    background: #12152b;
    border-radius: 16px;
    border: 1px solid #1e2340;
    min-height: 200px;
  }

  .step-box {
    background: #12152b;
    border: 1px solid #1e2340;
    border-radius: 12px;
    padding: 16px 20px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    color: #a0aec0;
    max-height: 320px;
    overflow-y: auto;
  }

  .step-box .highlight { color: #00f5c4; font-weight: 700; }
  .step-box .found     { color: #48bb78; font-weight: 700; }
  .step-box .notfound  { color: #fc8181; font-weight: 700; }

  .metric-card {
    background: #12152b;
    border: 1px solid #1e2340;
    border-radius: 12px;
    padding: 18px;
    text-align: center;
  }
  .metric-val  { font-size: 2rem; font-weight: 800; color: #00f5c4; }
  .metric-label{ font-size: 0.75rem; color: #718096; text-transform: uppercase; letter-spacing: 1px; }

  .legend-dot {
    display: inline-block;
    width: 12px; height: 12px;
    border-radius: 3px;
    margin-right: 6px;
  }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────
def binary_search_steps(arr, target):
    """Return list of step-dicts for animation."""
    steps = []
    lo, hi = 0, len(arr) - 1
    iteration = 0

    while lo <= hi:
        mid = (lo + hi) // 2
        iteration += 1
        steps.append({
            "lo": lo, "hi": hi, "mid": mid,
            "val": arr[mid],
            "iteration": iteration,
            "status": "searching",
        })
        if arr[mid] == target:
            steps.append({
                "lo": lo, "hi": hi, "mid": mid,
                "val": arr[mid],
                "iteration": iteration,
                "status": "found",
            })
            return steps, mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1

    steps.append({
        "lo": lo, "hi": hi, "mid": -1,
        "val": None,
        "iteration": iteration,
        "status": "notfound",
    })
    return steps, -1


def render_bars(arr, lo, hi, mid, found_idx=-1):
    """Build HTML bar chart."""
    max_val = max(arr) if arr else 1
    bars_html = ""
    for i, v in enumerate(arr):
        height = max(20, int((v / max_val) * 160))
        if found_idx != -1 and i == found_idx:
            color = "#48bb78"   # green – found
            border = "2px solid #9ae6b4"
            label_color = "#9ae6b4"
        elif i == mid:
            color = "#f6e05e"   # yellow – mid pointer
            border = "2px solid #fefcbf"
            label_color = "#fefcbf"
        elif lo <= i <= hi:
            color = "#7b61ff"   # purple – active range
            border = "1px solid #9f7aea"
            label_color = "#9f7aea"
        else:
            color = "#2d3561"   # dark – eliminated
            border = "1px solid #2d3561"
            label_color = "#4a5568"

        bars_html += f"""
        <div style="display:flex;flex-direction:column;align-items:center;gap:4px;">
          <span style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:{label_color};">{v}</span>
          <div style="
            width:28px; height:{height}px;
            background:{color};
            border:{border};
            border-radius:4px 4px 0 0;
            transition: all 0.3s ease;
          "></div>
          <span style="font-family:'JetBrains Mono',monospace;font-size:0.6rem;color:#4a5568;">{i}</span>
        </div>"""

    return f'<div class="bar-container">{bars_html}</div>'


# ─────────────────────────────────────────────
#  Session state
# ─────────────────────────────────────────────
if "arr" not in st.session_state:
    st.session_state.arr = sorted(random.sample(range(10, 200), 18))
if "steps" not in st.session_state:
    st.session_state.steps = []
if "current_step" not in st.session_state:
    st.session_state.current_step = 0
if "result_idx" not in st.session_state:
    st.session_state.result_idx = -1
if "running" not in st.session_state:
    st.session_state.running = False


# ─────────────────────────────────────────────
#  UI Layout
# ─────────────────────────────────────────────
st.markdown("<h1>🔍 Binary Search Visualizer</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='color:#718096;margin-top:-12px;'>Divide and conquer — O(log n) searching on sorted arrays</p>",
    unsafe_allow_html=True,
)

col_ctrl, col_vis = st.columns([1, 2.5], gap="large")

with col_ctrl:
    st.markdown("### ⚙️ Controls")

    # Array controls
    arr_size = st.slider("Array size", 8, 30, 18, key="arr_size")
    arr_range = st.slider("Value range", 10, 500, (10, 200), key="arr_range")

    if st.button("🎲 Generate New Array", use_container_width=True):
        st.session_state.arr = sorted(random.sample(range(arr_range[0], arr_range[1]), arr_size))
        st.session_state.steps = []
        st.session_state.current_step = 0
        st.session_state.result_idx = -1

    st.divider()

    target = st.number_input(
        "🎯 Search Target",
        min_value=int(arr_range[0]),
        max_value=int(arr_range[1]),
        value=int(st.session_state.arr[len(st.session_state.arr)//2]),
        step=1,
    )

    speed = st.select_slider(
        "⚡ Animation Speed",
        options=["Slow (1s)", "Normal (0.5s)", "Fast (0.2s)", "Instant"],
        value="Normal (0.5s)",
    )
    speed_map = {"Slow (1s)": 1.0, "Normal (0.5s)": 0.5, "Fast (0.2s)": 0.2, "Instant": 0.0}
    delay = speed_map[speed]

    c1, c2 = st.columns(2)
    with c1:
        run_btn = st.button("▶ Run", use_container_width=True, type="primary")
    with c2:
        reset_btn = st.button("↺ Reset", use_container_width=True)

    if reset_btn:
        st.session_state.steps = []
        st.session_state.current_step = 0
        st.session_state.result_idx = -1

    # Step-by-step controls
    st.divider()
    st.markdown("**Step-by-Step Mode**")
    prev_btn, next_btn = st.columns(2)
    with prev_btn:
        if st.button("◀ Prev", use_container_width=True):
            if st.session_state.current_step > 0:
                st.session_state.current_step -= 1
    with next_btn:
        if st.button("Next ▶", use_container_width=True):
            if not st.session_state.steps:
                steps, idx = binary_search_steps(st.session_state.arr, int(target))
                st.session_state.steps = steps
                st.session_state.result_idx = idx
            if st.session_state.current_step < len(st.session_state.steps) - 1:
                st.session_state.current_step += 1

    # Legend
    st.divider()
    st.markdown("""
    <div style='font-size:0.8rem;color:#a0aec0;'>
      <div><span class='legend-dot' style='background:#7b61ff'></span>Active search range</div>
      <div style='margin-top:4px'><span class='legend-dot' style='background:#f6e05e'></span>Mid pointer (checked)</div>
      <div style='margin-top:4px'><span class='legend-dot' style='background:#48bb78'></span>Target found!</div>
      <div style='margin-top:4px'><span class='legend-dot' style='background:#2d3561'></span>Eliminated</div>
    </div>""", unsafe_allow_html=True)


with col_vis:
    # Metrics row
    arr = st.session_state.arr
    m1, m2, m3, m4 = st.columns(4)
    import math
    max_steps = math.ceil(math.log2(len(arr))) if arr else 0

    m1.markdown(f"""<div class="metric-card">
      <div class="metric-val">{len(arr)}</div>
      <div class="metric-label">Array Size</div></div>""", unsafe_allow_html=True)
    m2.markdown(f"""<div class="metric-card">
      <div class="metric-val">{max_steps}</div>
      <div class="metric-label">Max Steps (log₂n)</div></div>""", unsafe_allow_html=True)

    steps_done = st.session_state.current_step if st.session_state.steps else 0
    m3.markdown(f"""<div class="metric-card">
      <div class="metric-val">{steps_done}</div>
      <div class="metric-label">Steps Taken</div></div>""", unsafe_allow_html=True)

    status_txt = "—"
    status_color = "#a0aec0"
    if st.session_state.steps:
        last = st.session_state.steps[st.session_state.current_step]
        if last["status"] == "found":
            status_txt = "FOUND ✓"
            status_color = "#48bb78"
        elif last["status"] == "notfound":
            status_txt = "NOT FOUND"
            status_color = "#fc8181"
        else:
            status_txt = "Searching…"
            status_color = "#f6e05e"

    m4.markdown(f"""<div class="metric-card">
      <div class="metric-val" style="color:{status_color};font-size:1.2rem;">{status_txt}</div>
      <div class="metric-label">Status</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Bar chart placeholder
    bar_placeholder = st.empty()

    # Draw initial bars
    def draw_current():
        steps = st.session_state.steps
        idx = st.session_state.current_step
        if not steps:
            html = render_bars(arr, 0, len(arr)-1, -1)
        else:
            s = steps[idx]
            found = s["mid"] if s["status"] == "found" else -1
            html = render_bars(arr, s["lo"], s["hi"], s["mid"], found_idx=found)
        bar_placeholder.markdown(html, unsafe_allow_html=True)

    draw_current()

    # Step log
    st.markdown("#### 📋 Step Log")
    log_placeholder = st.empty()

    def render_log():
        steps = st.session_state.steps
        if not steps:
            log_placeholder.markdown(
                '<div class="step-box">Run the search to see step-by-step log...</div>',
                unsafe_allow_html=True,
            )
            return
        lines = ""
        for i, s in enumerate(steps[:st.session_state.current_step + 1]):
            iter_badge = f"<span style='color:#7b61ff'>Iter {s['iteration']}</span>"
            if s["status"] == "found":
                lines += f"<div class='found'>✓ {iter_badge} → Found {s['val']} at index {s['mid']}</div>"
            elif s["status"] == "notfound":
                lines += f"<div class='notfound'>✗ Target not found in array.</div>"
            else:
                lines += (
                    f"<div>• {iter_badge} "
                    f"lo=<span class='highlight'>{s['lo']}</span> "
                    f"hi=<span class='highlight'>{s['hi']}</span> "
                    f"mid=<span class='highlight'>{s['mid']}</span> "
                    f"→ arr[{s['mid']}]={s['val']}</div>"
                )
        log_placeholder.markdown(f'<div class="step-box">{lines}</div>', unsafe_allow_html=True)

    render_log()


# ─────────────────────────────────────────────
#  Run animation
# ─────────────────────────────────────────────
if run_btn:
    steps, idx = binary_search_steps(arr, int(target))
    st.session_state.steps = steps
    st.session_state.result_idx = idx
    st.session_state.current_step = 0

    for i, s in enumerate(steps):
        st.session_state.current_step = i
        found = s["mid"] if s["status"] == "found" else -1
        bar_placeholder.markdown(
            render_bars(arr, s["lo"], s["hi"], s["mid"], found_idx=found),
            unsafe_allow_html=True,
        )
        render_log()
        if delay > 0:
            time.sleep(delay)

    st.rerun()


# ─────────────────────────────────────────────
#  Complexity info
# ─────────────────────────────────────────────
st.divider()
st.markdown("### 📘 About Binary Search")
i1, i2, i3 = st.columns(3)
i1.info("**Time Complexity**\n\nBest: O(1)\n\nAverage: O(log n)\n\nWorst: O(log n)")
i2.info("**Space Complexity**\n\nIterative: O(1)\n\nRecursive: O(log n) stack")
i3.info("**Requirement**\n\nArray must be **sorted**.\n\nWorks by halving the search space each iteration.")

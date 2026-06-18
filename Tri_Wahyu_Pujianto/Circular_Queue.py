import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="Circular Queue Visualizer", page_icon="", layout="centered")

st.title("Visualisasi Circular Queue")
st.markdown("Simulasi **Circular Queue** dengan konsep *wrap-around* (melingkar)")

# ── Session state ─────────────────────────────────────────────────────────────
MAX_SIZE = 8

def init_state():
    if "queue" not in st.session_state:
        st.session_state.queue = [None] * MAX_SIZE
    if "front" not in st.session_state:
        st.session_state.front = -1
    if "rear" not in st.session_state:
        st.session_state.rear = -1
    if "count" not in st.session_state:
        st.session_state.count = 0
    if "log" not in st.session_state:
        st.session_state.log = []

init_state()

q     = st.session_state.queue
front = st.session_state.front
rear  = st.session_state.rear
count = st.session_state.count

# ── Circular Queue helpers ────────────────────────────────────────────────────
def is_empty():
    return st.session_state.count == 0

def is_full():
    return st.session_state.count == MAX_SIZE

def enqueue(value):
    if is_full():
        st.session_state.log.append(f"❌ Enqueue({value}) gagal — Queue PENUH!")
        return
    if st.session_state.front == -1:
        st.session_state.front = 0
    st.session_state.rear = (st.session_state.rear + 1) % MAX_SIZE
    st.session_state.queue[st.session_state.rear] = value
    st.session_state.count += 1
    st.session_state.log.append(f"✅ Enqueue({value}) → rear={st.session_state.rear}")

def dequeue():
    if is_empty():
        st.session_state.log.append("❌ Dequeue gagal — Queue KOSONG!")
        return
    removed = st.session_state.queue[st.session_state.front]
    st.session_state.queue[st.session_state.front] = None
    if st.session_state.count == 1:
        st.session_state.front = -1
        st.session_state.rear  = -1
    else:
        st.session_state.front = (st.session_state.front + 1) % MAX_SIZE
    st.session_state.count -= 1
    st.session_state.log.append(f"🗑️  Dequeue() → hapus [{removed}], front={st.session_state.front}")

# Draw circular visualization
def draw_circle():
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-1.6, 1.6)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor("#0e1117")
    ax.set_facecolor("#0e1117")

    n = MAX_SIZE
    radius_outer = 1.3
    radius_inner = 0.75
    radius_label = 1.55
    radius_text  = 1.02

    for i in range(n):
        angle_start = 90 - i * (360 / n)
        angle_end   = angle_start - (360 / n)

        # Determine slot color
        if is_empty():
            color = "#2c2f3a"
        elif count == MAX_SIZE:
            color = "#1f6feb"   # full → all blue
        else:
            # fill slots from front to rear (wrap-aware)
            filled = False
            if front <= rear:
                filled = front <= i <= rear
            else:
                filled = i >= front or i <= rear
            color = "#1f6feb" if filled else "#2c2f3a"

        # Highlight front / rear
        if not is_empty():
            if i == st.session_state.front and i == st.session_state.rear:
                color = "#f0b429"   # both → gold
            elif i == st.session_state.front:
                color = "#38d9a9"   # front → teal
            elif i == st.session_state.rear:
                color = "#e8590c"   # rear  → orange

        wedge = mpatches.Wedge(
            center=(0, 0),
            r=radius_outer,
            theta1=angle_end,
            theta2=angle_start,
            width=radius_outer - radius_inner,
            facecolor=color,
            edgecolor="#0e1117",
            linewidth=2,
        )
        ax.add_patch(wedge)

        # Slot index label (outside ring)
        mid_angle = np.radians((angle_start + angle_end) / 2)
        lx = radius_label * np.cos(mid_angle)
        ly = radius_label * np.sin(mid_angle)
        ax.text(lx, ly, str(i), ha="center", va="center",
                fontsize=9, color="#adb5bd", fontweight="bold")

        # Value inside ring
        tx = radius_text * np.cos(mid_angle)
        ty = radius_text * np.sin(mid_angle)
        val = st.session_state.queue[i]
        ax.text(tx, ty, str(val) if val is not None else "",
                ha="center", va="center", fontsize=11,
                color="white", fontweight="bold")

    # Centre info
    ax.text(0,  0.18, f"Size: {count}/{MAX_SIZE}",
            ha="center", va="center", fontsize=11, color="white", fontweight="bold")
    ax.text(0, -0.18, "Circular Queue",
            ha="center", va="center", fontsize=9, color="#6c757d")

    # Legend
    legend_items = [
        mpatches.Patch(color="#38d9a9", label=f"Front [{st.session_state.front}]"),
        mpatches.Patch(color="#e8590c", label=f"Rear  [{st.session_state.rear}]"),
        mpatches.Patch(color="#f0b429", label="Front & Rear"),
        mpatches.Patch(color="#1f6feb", label="Berisi data"),
        mpatches.Patch(color="#2c2f3a", label="Kosong"),
    ]
    ax.legend(handles=legend_items, loc="lower center",
              bbox_to_anchor=(0.5, -0.08), ncol=3,
              fontsize=7.5, facecolor="#1c1e26",
              edgecolor="#444", labelcolor="white")

    plt.tight_layout()
    return fig

# ── UI Layout ─────────────────────────────────────────────────────────────────
col_vis, col_ctrl = st.columns([1.2, 1])

with col_vis:
    st.subheader("Visualisasi")
    st.pyplot(draw_circle(), use_container_width=True)

with col_ctrl:
    st.subheader("Kontrol")

    # Status badges
    status_color = "#e03131" if is_full() else ("#2f9e44" if not is_empty() else "#868e96")
    status_text  = "PENUH 🔴" if is_full() else ("AKTIF 🟢" if not is_empty() else "KOSONG ⚪")
    st.markdown(f"**Status:** `{status_text}`")
    st.markdown(f"**Front:** `{st.session_state.front}` &nbsp;|&nbsp; **Rear:** `{st.session_state.rear}`")
    st.markdown(f"**Elemen:** `{count}/{MAX_SIZE}`")

    st.divider()

    # Enqueue
    st.markdown("**➕ Enqueue**")
    enq_val = st.text_input("Nilai", placeholder="Contoh: A, 42, ...", key="enq_input", label_visibility="collapsed")
    if st.button("Enqueue", use_container_width=True, type="primary"):
        if enq_val.strip():
            enqueue(enq_val.strip())
            st.rerun()
        else:
            st.warning("Masukkan nilai terlebih dahulu!")

    st.divider()

    # Dequeue
    st.markdown("**➖ Dequeue**")
    if st.button("Dequeue", use_container_width=True):
        dequeue()
        st.rerun()

    st.divider()

    # Reset
    if st.button("🔁 Reset Queue", use_container_width=True):
        for key in ["queue", "front", "rear", "count", "log"]:
            del st.session_state[key]
        st.rerun()

# ── Queue array display ───────────────────────────────────────────────────────
st.subheader("Isi Array Queue")
cols = st.columns(MAX_SIZE)
for i, col in enumerate(cols):
    val = st.session_state.queue[i]
    label = str(val) if val is not None else "—"
    is_f  = (i == st.session_state.front and not is_empty())
    is_r  = (i == st.session_state.rear  and not is_empty())
    badge = ""
    if is_f and is_r: badge = "F/R"
    elif is_f:        badge = "F"
    elif is_r:        badge = "R"
    col.metric(label=f"[{i}] {badge}", value=label)

# ── Log ───────────────────────────────────────────────────────────────────────
st.subheader("Log Operasi")
if st.session_state.log:
    for entry in reversed(st.session_state.log[-10:]):
        st.text(entry)
else:
    st.caption("Belum ada operasi.")

# ── Penjelasan konsep ──────────────────────────────────────────────────────────
with st.expander("Penjelasan Circular Queue"):
    st.markdown("""
**Circular Queue** adalah struktur data antrian di mana:
- 🔁 Elemen terakhir (index `MAX-1`) terhubung kembali ke elemen pertama (index `0`)
- 📐 Menggunakan konsep **wrap-around**: `rear = (rear + 1) % MAX_SIZE`

**Operasi utama:**
| Operasi | Kondisi | Keterangan |
|---------|---------|------------|
| `Enqueue(x)` | Queue tidak penuh | Tambah elemen di `rear` |
| `Dequeue()` | Queue tidak kosong | Hapus elemen di `front` |
| `isFull()` | `count == MAX_SIZE` | Queue penuh |
| `isEmpty()` | `count == 0` | Queue kosong |

**Rumus wrap-around:**
```python
rear  = (rear  + 1) % MAX_SIZE   # saat Enqueue
front = (front + 1) % MAX_SIZE   # saat Dequeue
```
    """)

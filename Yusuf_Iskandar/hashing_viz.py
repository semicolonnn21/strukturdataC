import streamlit as st
import random
import string
import hashlib

# ─────────────────────────────────────────────
#  Page config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Hashing Visualizer",
    page_icon="#️⃣",
    layout="wide",
)

# ─────────────────────────────────────────────
#  Custom CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Syne:wght@400;700;800&display=swap');

  html, body, [class*="css"] { font-family: 'Syne', sans-serif; }
  .main { background: #0e1117; }

  h1 {
    font-size: 2.6rem !important;
    font-weight: 800 !important;
    background: linear-gradient(135deg, #f6ad55, #ed64a6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -1px;
  }

  .bucket-wrap {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin: 8px 0;
  }

  .bucket {
    background: #1a1d2e;
    border: 1px solid #2d3561;
    border-radius: 10px;
    padding: 8px 10px;
    min-width: 120px;
    flex: 1;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
  }

  .bucket-label {
    color: #f6ad55;
    font-weight: 700;
    font-size: 0.7rem;
    margin-bottom: 6px;
    border-bottom: 1px solid #2d3561;
    padding-bottom: 4px;
  }

  .bucket-item {
    color: #e2e8f0;
    padding: 3px 0;
    border-bottom: 1px dashed #2d3561;
  }

  .bucket-item:last-child { border-bottom: none; }

  .collision-item { color: #fc8181 !important; }
  .new-item       { color: #68d391 !important; }

  .kv-row {
    display: flex;
    gap: 6px;
    margin-bottom: 4px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
  }
  .kv-key   { background:#2d3748; color:#f6ad55; padding:2px 8px; border-radius:4px; }
  .kv-arrow { color:#718096; }
  .kv-val   { background:#1a202c; color:#68d391; padding:2px 8px; border-radius:4px; flex:1; }
  .kv-hash  { color:#9f7aea; font-size:0.65rem; }

  .metric-card {
    background: #1a1d2e;
    border: 1px solid #2d3561;
    border-radius: 12px;
    padding: 16px;
    text-align: center;
  }
  .metric-val   { font-size: 1.9rem; font-weight: 800; color: #f6ad55; }
  .metric-label { font-size: 0.72rem; color: #718096; text-transform: uppercase; letter-spacing: 1px; }

  .log-box {
    background: #1a1d2e;
    border: 1px solid #2d3561;
    border-radius: 10px;
    padding: 14px 16px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    color: #a0aec0;
    max-height: 260px;
    overflow-y: auto;
  }

  .tab-content { margin-top: 12px; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  Hash Table Implementation
# ─────────────────────────────────────────────
class HashTable:
    """Chaining-based hash table."""

    def __init__(self, size=8):
        self.size = size
        self.buckets: list[list] = [[] for _ in range(size)]
        self.count = 0
        self.collision_count = 0
        self.ops_log: list[str] = []

    # ----- hash functions -----
    def _hash_division(self, key: str) -> int:
        return sum(ord(c) for c in str(key)) % self.size

    def _hash_polynomial(self, key: str) -> int:
        h, p = 0, 31
        for c in str(key):
            h = (h * p + ord(c)) % self.size
        return h

    def _hash_fnv1a(self, key: str) -> int:
        h = 2166136261
        for c in str(key):
            h ^= ord(c)
            h = (h * 16777619) & 0xFFFFFFFF
        return h % self.size

    def hash_key(self, key: str, method: str) -> int:
        if method == "Division":
            return self._hash_division(key)
        elif method == "Polynomial Rolling":
            return self._hash_polynomial(key)
        else:
            return self._hash_fnv1a(key)

    # ----- operations -----
    def insert(self, key: str, value, method: str):
        idx = self.hash_key(key, method)
        # check existing
        for i, (k, v) in enumerate(self.buckets[idx]):
            if k == key:
                self.buckets[idx][i] = (key, value)
                self.ops_log.append(f"UPDATE  bucket[{idx}] key='{key}' val='{value}'")
                return idx, False  # updated, no collision
        if len(self.buckets[idx]) > 0:
            self.collision_count += 1
            self.buckets[idx].append((key, value))
            self.ops_log.append(f"COLLIDE bucket[{idx}] key='{key}' → chained (collision #{self.collision_count})")
        else:
            self.buckets[idx].append((key, value))
            self.ops_log.append(f"INSERT  bucket[{idx}] key='{key}' val='{value}'")
        self.count += 1
        return idx, len(self.buckets[idx]) > 1

    def search(self, key: str, method: str):
        idx = self.hash_key(key, method)
        for k, v in self.buckets[idx]:
            if k == key:
                self.ops_log.append(f"SEARCH  bucket[{idx}] key='{key}' → FOUND '{v}'")
                return idx, v
        self.ops_log.append(f"SEARCH  bucket[{idx}] key='{key}' → NOT FOUND")
        return idx, None

    def delete(self, key: str, method: str):
        idx = self.hash_key(key, method)
        for i, (k, v) in enumerate(self.buckets[idx]):
            if k == key:
                self.buckets[idx].pop(i)
                self.count -= 1
                self.ops_log.append(f"DELETE  bucket[{idx}] key='{key}' → removed")
                return idx, True
        self.ops_log.append(f"DELETE  bucket[{idx}] key='{key}' → NOT FOUND")
        return idx, False

    @property
    def load_factor(self):
        return self.count / self.size if self.size else 0


# ─────────────────────────────────────────────
#  Session State
# ─────────────────────────────────────────────
def init_state():
    if "ht" not in st.session_state:
        st.session_state.ht = HashTable(size=8)
    if "last_bucket" not in st.session_state:
        st.session_state.last_bucket = -1
    if "last_op" not in st.session_state:
        st.session_state.last_op = ""

init_state()
ht: HashTable = st.session_state.ht


# ─────────────────────────────────────────────
#  UI
# ─────────────────────────────────────────────
st.markdown("<h1>#️⃣ Hashing Visualizer</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='color:#718096;margin-top:-12px;'>Explore hash tables: insert, search, delete & collision chaining — O(1) average</p>",
    unsafe_allow_html=True,
)

col_ctrl, col_vis = st.columns([1, 2.5], gap="large")

# ─── Controls ─────────────────────────────────
with col_ctrl:
    st.markdown("### ⚙️ Configuration")

    hash_method = st.selectbox(
        "Hash Function",
        ["Division", "Polynomial Rolling", "FNV-1a"],
        help="Division: sum of ASCII % size | Polynomial: p=31 rolling | FNV-1a: Fowler–Noll–Vo"
    )

    table_size = st.slider("Table Size (buckets)", 4, 20, ht.size, key="tbl_size")
    if st.button("🔄 Resize / Reset Table", use_container_width=True):
        st.session_state.ht = HashTable(size=table_size)
        st.session_state.last_bucket = -1
        st.session_state.last_op = ""
        ht = st.session_state.ht
        st.rerun()

    st.divider()

    op = st.radio("Operation", ["Insert", "Search", "Delete"], horizontal=True)

    key_input = st.text_input("Key", placeholder="e.g. 'apple', '42', 'hello'")
    val_input = ""
    if op == "Insert":
        val_input = st.text_input("Value", placeholder="e.g. 'red', '100', 'world'")

    do_btn = st.button(f"▶ {op}", use_container_width=True, type="primary")

    st.divider()
    st.markdown("**Demo Data**")
    demo_words = ["apple", "banana", "mango", "grape", "kiwi",
                  "lemon", "melon", "plum", "peach", "lime"]
    if st.button("🍎 Load Fruit Demo", use_container_width=True):
        st.session_state.ht = HashTable(size=table_size)
        ht = st.session_state.ht
        for w in demo_words:
            ht.insert(w, random.randint(1, 100), hash_method)
        st.session_state.last_bucket = -1
        st.session_state.last_op = "Loaded demo data"
        st.rerun()

    if st.button("🎲 Random Strings", use_container_width=True):
        st.session_state.ht = HashTable(size=table_size)
        ht = st.session_state.ht
        for _ in range(10):
            k = "".join(random.choices(string.ascii_lowercase, k=4))
            v = random.randint(1, 999)
            ht.insert(k, v, hash_method)
        st.session_state.last_bucket = -1
        st.session_state.last_op = "Loaded random data"
        st.rerun()


# ─── Operation Handler ────────────────────────
if do_btn and key_input.strip():
    k = key_input.strip()
    if op == "Insert":
        v = val_input.strip() or "null"
        idx, collision = ht.insert(k, v, hash_method)
        st.session_state.last_bucket = idx
        st.session_state.last_op = f"Inserted '{k}' → bucket[{idx}]" + (" (COLLISION)" if collision else "")
    elif op == "Search":
        idx, result = ht.search(k, hash_method)
        st.session_state.last_bucket = idx
        st.session_state.last_op = f"Searched '{k}' → " + (f"Found '{result}' in bucket[{idx}]" if result is not None else "NOT FOUND")
    else:
        idx, success = ht.delete(k, hash_method)
        st.session_state.last_bucket = idx
        st.session_state.last_op = f"Deleted '{k}' → " + ("OK" if success else "KEY NOT FOUND")


# ─── Visual Area ──────────────────────────────
with col_vis:
    # Metrics
    m1, m2, m3, m4 = st.columns(4)
    lf = ht.load_factor
    lf_color = "#48bb78" if lf < 0.7 else "#f6ad55" if lf < 1.0 else "#fc8181"

    m1.markdown(f"""<div class="metric-card">
      <div class="metric-val">{ht.count}</div>
      <div class="metric-label">Items</div></div>""", unsafe_allow_html=True)
    m2.markdown(f"""<div class="metric-card">
      <div class="metric-val">{ht.size}</div>
      <div class="metric-label">Buckets</div></div>""", unsafe_allow_html=True)
    m3.markdown(f"""<div class="metric-card">
      <div class="metric-val" style="color:{lf_color}">{lf:.2f}</div>
      <div class="metric-label">Load Factor</div></div>""", unsafe_allow_html=True)
    m4.markdown(f"""<div class="metric-card">
      <div class="metric-val" style="color:#fc8181">{ht.collision_count}</div>
      <div class="metric-label">Collisions</div></div>""", unsafe_allow_html=True)

    if st.session_state.last_op:
        color = "#48bb78" if "Found" in st.session_state.last_op or "Inserted" in st.session_state.last_op else \
                "#fc8181" if "NOT FOUND" in st.session_state.last_op else "#f6ad55"
        st.markdown(
            f"<div style='background:#1a1d2e;border:1px solid #2d3561;border-radius:8px;padding:10px 14px;"
            f"font-family:JetBrains Mono,monospace;font-size:0.8rem;color:{color};margin:8px 0'>"
            f"→ {st.session_state.last_op}</div>",
            unsafe_allow_html=True
        )

    # Tabs
    tab1, tab2, tab3 = st.tabs(["🪣 Hash Table", "🔑 Key-Value Map", "📋 Operation Log"])

    with tab1:
        st.markdown("<div class='tab-content'>", unsafe_allow_html=True)
        st.markdown("**Bucket view** — each row is a chain (linked list for collisions)")

        last_b = st.session_state.last_bucket
        buckets_html = '<div class="bucket-wrap">'
        cols_per_row = 4
        bucket_rows = [ht.buckets[i:i+cols_per_row] for i in range(0, ht.size, cols_per_row)]

        for row_buckets in bucket_rows:
            row_html = '<div style="display:flex;gap:10px;width:100%;margin-bottom:10px;">'
            start_idx = bucket_rows.index(row_buckets) * cols_per_row
            for j, bucket in enumerate(row_buckets):
                idx = start_idx + j
                highlight = "border:1px solid #f6ad55 !important;" if idx == last_b else ""
                items_html = ""
                for ci, (k, v) in enumerate(bucket):
                    cls = "new-item" if idx == last_b and ci == len(bucket)-1 else \
                          "collision-item" if ci > 0 else ""
                    chain = "→ " if ci > 0 else ""
                    items_html += f"<div class='bucket-item {cls}'>{chain}{k}: {v}</div>"
                if not items_html:
                    items_html = "<div style='color:#4a5568;font-size:0.65rem;'>empty</div>"
                row_html += f"""
                <div class='bucket' style='flex:1;{highlight}'>
                  <div class='bucket-label'>Bucket [{idx}]</div>
                  {items_html}
                </div>"""
            row_html += "</div>"
            st.markdown(row_html, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("<div class='tab-content'>", unsafe_allow_html=True)
        st.markdown("**All stored key-value pairs** with their bucket index")
        all_items = []
        for idx, bucket in enumerate(ht.buckets):
            for k, v in bucket:
                h = ht.hash_key(k, hash_method)
                all_items.append((k, v, h))

        if all_items:
            for k, v, h in sorted(all_items, key=lambda x: x[2]):
                st.markdown(
                    f"<div class='kv-row'>"
                    f"<span class='kv-key'>{k}</span>"
                    f"<span class='kv-arrow'>→</span>"
                    f"<span class='kv-val'>{v}</span>"
                    f"<span class='kv-hash'>bucket[{h}]</span>"
                    f"</div>",
                    unsafe_allow_html=True,
                )
        else:
            st.markdown("<p style='color:#4a5568;font-size:0.85rem;'>Table is empty.</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with tab3:
        st.markdown("<div class='tab-content'>", unsafe_allow_html=True)
        if ht.ops_log:
            log_entries = ""
            for entry in reversed(ht.ops_log[-40:]):
                if "FOUND" in entry and "NOT" not in entry:
                    c = "#68d391"
                elif "NOT FOUND" in entry or "COLLIDE" in entry:
                    c = "#fc8181"
                elif "DELETE" in entry:
                    c = "#fc8181"
                elif "UPDATE" in entry:
                    c = "#f6ad55"
                else:
                    c = "#a0aec0"
                log_entries += f"<div style='color:{c};padding:2px 0;border-bottom:1px solid #1a1d2e;'>{entry}</div>"
            st.markdown(f'<div class="log-box">{log_entries}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="log-box">No operations yet...</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  Hash Function Demo Panel
# ─────────────────────────────────────────────
st.divider()
st.markdown("### 🔬 Hash Function Calculator")
hc1, hc2, hc3 = st.columns([1.5, 1, 1])

with hc1:
    demo_key = st.text_input("Try any key:", value="hello", key="demo_key_input")
    demo_size = st.slider("Table size for demo", 4, 20, 8, key="demo_size")

with hc2:
    if demo_key:
        st.markdown("**Results across all methods:**")
        ht_demo = HashTable(size=demo_size)
        for method in ["Division", "Polynomial Rolling", "FNV-1a"]:
            idx = ht_demo.hash_key(demo_key, method)
            st.markdown(
                f"<div style='background:#1a1d2e;border-radius:6px;padding:8px 12px;margin:4px 0;"
                f"font-family:JetBrains Mono,monospace;font-size:0.78rem;'>"
                f"<span style='color:#f6ad55'>{method}</span>"
                f"<span style='color:#718096'> → bucket </span>"
                f"<span style='color:#00f5c4'>[{idx}]</span></div>",
                unsafe_allow_html=True,
            )

with hc3:
    if demo_key:
        st.markdown("**SHA-256 (standard lib)**")
        sha = hashlib.sha256(demo_key.encode()).hexdigest()
        st.markdown(
            f"<div style='background:#1a1d2e;border-radius:6px;padding:8px 12px;"
            f"font-family:JetBrains Mono,monospace;font-size:0.62rem;color:#9f7aea;word-break:break-all;'>"
            f"{sha}</div>",
            unsafe_allow_html=True,
        )
        st.caption("SHA-256 is a cryptographic hash — not used for hash tables but shown for comparison.")


# ─────────────────────────────────────────────
#  Info section
# ─────────────────────────────────────────────
st.divider()
st.markdown("### 📘 About Hash Tables")
i1, i2, i3 = st.columns(3)
i1.info("**Time Complexity**\n\nInsert: O(1) avg, O(n) worst\n\nSearch: O(1) avg, O(n) worst\n\nDelete: O(1) avg, O(n) worst")
i2.info("**Collision Resolution**\n\nThis demo uses **Separate Chaining** — each bucket holds a linked list. Alternatives: Open Addressing (Linear Probing, Quadratic, Double Hashing)")
i3.info("**Load Factor**\n\nλ = n / m (items / buckets)\n\nKeep λ < 0.75 for good performance.\n\nRehash (resize) when λ exceeds threshold.")

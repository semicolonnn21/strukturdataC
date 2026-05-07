import streamlit as st

st.set_page_config(page_title="Hash Table Visualizer", page_icon="#️⃣", layout="wide")

# ── Hash Table: Separate Chaining ────────────────────────────────────────────
class HashTableChaining:
    def __init__(self, size=8):
        self.size = size
        self.table = [[] for _ in range(size)]

    def _hash(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        idx = self._hash(key)
        for pair in self.table[idx]:
            if pair[0] == key:
                pair[1] = value
                return idx, "updated"
        self.table[idx].append([key, value])
        return idx, "inserted"

    def search(self, key):
        idx = self._hash(key)
        for pair in self.table[idx]:
            if pair[0] == key:
                return idx, pair[1]
        return idx, None

    def delete(self, key):
        idx = self._hash(key)
        before = len(self.table[idx])
        self.table[idx] = [p for p in self.table[idx] if p[0] != key]
        return idx, len(self.table[idx]) < before

    def item_count(self):
        return sum(len(b) for b in self.table)

    def load_factor(self):
        return self.item_count() / self.size


# ── Hash Table: Linear Probing ────────────────────────────────────────────────
class HashTableLinearProbing:
    DELETED = "__DELETED__"

    def __init__(self, size=8):
        self.size = size
        self.table = [None] * size

    def _hash(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        if self.item_count() >= self.size:
            return None, [], "full"
        idx = self._hash(key)
        probes = []
        for _ in range(self.size):
            probes.append(idx)
            if self.table[idx] is None or self.table[idx] == self.DELETED:
                self.table[idx] = (key, value)
                return idx, probes, "inserted"
            if self.table[idx][0] == key:
                self.table[idx] = (key, value)
                return idx, probes, "updated"
            idx = (idx + 1) % self.size
        return None, probes, "full"

    def search(self, key):
        idx = self._hash(key)
        probes = []
        for _ in range(self.size):
            probes.append(idx)
            if self.table[idx] is None:
                return None, probes, None
            if self.table[idx] != self.DELETED and self.table[idx][0] == key:
                return idx, probes, self.table[idx][1]
            idx = (idx + 1) % self.size
        return None, probes, None

    def delete(self, key):
        idx = self._hash(key)
        probes = []
        for _ in range(self.size):
            probes.append(idx)
            if self.table[idx] is None:
                return None, probes, False
            if self.table[idx] != self.DELETED and self.table[idx][0] == key:
                self.table[idx] = self.DELETED
                return idx, probes, True
            idx = (idx + 1) % self.size
        return None, probes, False

    def item_count(self):
        return sum(1 for s in self.table if s is not None and s != self.DELETED)

    def load_factor(self):
        return self.item_count() / self.size


# ── Session State ─────────────────────────────────────────────────────────────
if "ht_chain" not in st.session_state:
    st.session_state.ht_chain = HashTableChaining(size=8)
if "ht_probe" not in st.session_state:
    st.session_state.ht_probe = HashTableLinearProbing(size=8)
if "logs" not in st.session_state:
    st.session_state.logs = []
if "hl_chain" not in st.session_state:
    st.session_state.hl_chain = {}
if "hl_probe" not in st.session_state:
    st.session_state.hl_probe = {}


def add_log(msg):
    st.session_state.logs.insert(0, msg)
    if len(st.session_state.logs) > 20:
        st.session_state.logs.pop()


# ── Render Helpers ────────────────────────────────────────────────────────────
# Warna pakai emoji saja — tidak ada komponen alert di dalam columns
COLOR = {
    "insert":  "🟢",
    "found":   "🔵",
    "deleted": "🔴",
    "probe":   "🟡",
    "":        "⬜",
}

def render_chain_table(ht, highlights):
    # Header
    h1, h2, h3 = st.columns([1, 3, 5])
    h1.write("**Idx**")
    h2.write("**Status**")
    h3.write("**Isi Bucket**")
    st.divider()

    for i, bucket in enumerate(ht.table):
        h = highlights.get(i, "")
        col_idx, col_status, col_isi = st.columns([1, 3, 5])

        col_idx.write(f"**{i}**")

        label = {
            "insert":  "🟢 Insert",
            "found":   "🔵 Found",
            "deleted": "🔴 Deleted",
        }.get(h, "—")
        col_status.write(label)

        if not bucket:
            col_isi.write("*kosong*")
        else:
            items = "  ·  ".join(f"**{p[0]}** → {p[1]}" for p in bucket)
            col_isi.write(items)


def render_probe_table(ht, highlights):
    DELETED = HashTableLinearProbing.DELETED

    # Header
    h1, h2, h3 = st.columns([1, 3, 5])
    h1.write("**Idx**")
    h2.write("**Status**")
    h3.write("**Isi Slot**")
    st.divider()

    for i, slot in enumerate(ht.table):
        h = highlights.get(i, "")
        col_idx, col_status, col_isi = st.columns([1, 3, 5])

        col_idx.write(f"**{i}**")

        label = {
            "insert":  "🟢 Insert",
            "found":   "🔵 Found",
            "deleted": "🔴 Deleted",
            "probe":   "🟡 Probe",
        }.get(h, "—")
        col_status.write(label)

        if slot is None:
            col_isi.write("*kosong*")
        elif slot == DELETED:
            col_isi.write("~~dihapus~~")
        else:
            col_isi.write(f"**{slot[0]}** → {slot[1]}")


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Pengaturan")
    tbl_size = st.slider("Ukuran Tabel", min_value=4, max_value=12, value=8)

    if tbl_size != st.session_state.ht_chain.size:
        st.session_state.ht_chain = HashTableChaining(size=tbl_size)
        st.session_state.ht_probe = HashTableLinearProbing(size=tbl_size)
        st.session_state.logs     = []
        st.session_state.hl_chain = {}
        st.session_state.hl_probe = {}
        st.rerun()

    st.divider()
    st.header("🎮 Operasi")
    op      = st.radio("Pilih Operasi", ["Insert", "Search", "Delete"])
    key_in  = st.text_input("Key",   placeholder="contoh: alice")
    val_in  = st.text_input("Value", placeholder="contoh: 90", disabled=(op != "Insert"))
    run     = st.button(f"▶ Jalankan {op}", use_container_width=True)

    st.divider()
    if st.button("🗑 Reset Semua", use_container_width=True):
        sz = st.session_state.ht_chain.size
        st.session_state.ht_chain = HashTableChaining(size=sz)
        st.session_state.ht_probe = HashTableLinearProbing(size=sz)
        st.session_state.logs     = []
        st.session_state.hl_chain = {}
        st.session_state.hl_probe = {}
        st.rerun()

    st.divider()
    st.markdown("""
    **Legenda**
    - 🟢 Insert
    - 🔵 Search / Found
    - 🔴 Deleted
    - 🟡 Probe (Linear)
    """)


# ── Proses Operasi ────────────────────────────────────────────────────────────
if run:
    if not key_in.strip():
        st.sidebar.error("Key tidak boleh kosong!")
    else:
        key = key_in.strip()
        val = val_in.strip()
        hc  = st.session_state.ht_chain
        hp  = st.session_state.ht_probe

        # Chaining
        if op == "Insert":
            idx, status = hc.insert(key, val)
            st.session_state.hl_chain = {idx: "insert"}
            add_log(f"✅ [Chaining] INSERT '{key}'='{val}' → bucket[{idx}] {status}")
        elif op == "Search":
            idx, found = hc.search(key)
            st.session_state.hl_chain = {idx: "found"}
            if found is not None:
                add_log(f"🔍 [Chaining] SEARCH '{key}' → bucket[{idx}] ✓ value='{found}'")
            else:
                add_log(f"⚠️ [Chaining] SEARCH '{key}' → bucket[{idx}] ✗ tidak ditemukan")
        elif op == "Delete":
            idx, deleted = hc.delete(key)
            if deleted:
                st.session_state.hl_chain = {idx: "deleted"}
                add_log(f"🗑️ [Chaining] DELETE '{key}' → bucket[{idx}] ✓ dihapus")
            else:
                st.session_state.hl_chain = {idx: "found"}
                add_log(f"⚠️ [Chaining] DELETE '{key}' → tidak ditemukan")

        # Linear Probing
        if op == "Insert":
            idx, probes, status = hp.insert(key, val)
            if status == "full":
                add_log("❌ [Probing] INSERT gagal — tabel penuh!")
                st.session_state.hl_probe = {}
            else:
                hl = {p: "probe" for p in probes[:-1]}
                if idx is not None:
                    hl[idx] = "insert"
                st.session_state.hl_probe = hl
                add_log(f"✅ [Probing] INSERT '{key}'='{val}' → slot[{idx}] {status} ({len(probes)} probe)")
        elif op == "Search":
            idx, probes, found = hp.search(key)
            hl = {p: "probe" for p in probes[:-1]}
            if found is not None and idx is not None:
                hl[idx] = "found"
                add_log(f"🔍 [Probing] SEARCH '{key}' → slot[{idx}] ✓ value='{found}' ({len(probes)} probe)")
            else:
                add_log(f"⚠️ [Probing] SEARCH '{key}' ✗ tidak ditemukan ({len(probes)} probe)")
            st.session_state.hl_probe = hl
        elif op == "Delete":
            idx, probes, deleted = hp.delete(key)
            hl = {p: "probe" for p in probes[:-1]}
            if deleted and idx is not None:
                hl[idx] = "deleted"
                add_log(f"🗑️ [Probing] DELETE '{key}' → slot[{idx}] ✓ dihapus ({len(probes)} probe)")
            else:
                add_log(f"⚠️ [Probing] DELETE '{key}' ✗ tidak ditemukan ({len(probes)} probe)")
            st.session_state.hl_probe = hl


# ── Main UI ───────────────────────────────────────────────────────────────────
st.title("#️⃣ Hash Table Visualizer")
st.caption("Visualisasi interaktif Separate Chaining & Linear Probing")
st.divider()

tab1, tab2, tab3 = st.tabs(["⛓ Separate Chaining", "🔍 Linear Probing", "📋 Log Operasi"])

with tab1:
    ht = st.session_state.ht_chain
    st.subheader("Separate Chaining")
    st.caption("Collision diselesaikan dengan menumpuk data di bucket yang sama (list).")

    if key_in.strip():
        h = hash(key_in.strip()) % ht.size
        st.info(f"🔢 hash(**\"{key_in.strip()}\"**) % {ht.size} = **{h}**")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Items",       ht.item_count())
    c2.metric("Kapasitas",   ht.size)
    c3.metric("Load Factor", f"{ht.load_factor():.0%}")
    c4.metric("Max Chain",   max((len(b) for b in ht.table), default=0))

    st.divider()
    render_chain_table(ht, st.session_state.hl_chain)

with tab2:
    ht2 = st.session_state.ht_probe
    st.subheader("Linear Probing")
    st.caption("Collision diselesaikan dengan geser ke slot berikutnya: (h+1) % size.")

    if key_in.strip():
        h2 = hash(key_in.strip()) % ht2.size
        st.info(f"🔢 hash(**\"{key_in.strip()}\"**) % {ht2.size} = **{h2}** → probe: h, h+1, h+2 …")

    deleted_count = sum(1 for s in ht2.table if s == HashTableLinearProbing.DELETED)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Items",         ht2.item_count())
    c2.metric("Kapasitas",     ht2.size)
    c3.metric("Load Factor",   f"{ht2.load_factor():.0%}")
    c4.metric("Deleted Slots", deleted_count)

    st.divider()
    render_probe_table(ht2, st.session_state.hl_probe)

with tab3:
    st.subheader("📋 Log Operasi")
    if not st.session_state.logs:
        st.caption("Belum ada operasi yang dilakukan.")
    else:
        for entry in st.session_state.logs:
            st.write(entry)
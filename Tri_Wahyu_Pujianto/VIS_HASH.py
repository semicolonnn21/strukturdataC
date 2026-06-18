import streamlit as st
import time

st.set_page_config(page_title="Room Tri", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;800&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');

:root {
    --bg:#0b0f1a; --bg2:#111827; --bg3:#1a2235;
    --accent:#00f5c4; --warn:#ffb347; --danger:#ff4f6d;
    --text:#e2e8f0; --muted:#64748b; --border:rgba(0,245,196,0.15);
    --glow:0 0 18px rgba(0,245,196,0.35);
}
html, body, [data-testid="stAppViewContainer"] {
    background:var(--bg) !important; color:var(--text) !important;
    font-family:'Syne',sans-serif !important;
}
[data-testid="stAppViewContainer"]::before {
    content:""; position:fixed; inset:0; pointer-events:none; z-index:0;
    background-image: linear-gradient(rgba(0,245,196,0.04) 1px,transparent 1px),
                      linear-gradient(90deg,rgba(0,245,196,0.04) 1px,transparent 1px);
    background-size:40px 40px;
}
[data-testid="stMain"] > div { position:relative; z-index:1; }
[data-testid="stSidebar"] {
    background:var(--bg2) !important; border-right:1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color:var(--text) !important; }
.material-symbols-rounded,
[data-testid="stSidebarCollapsedControl"] span,
[data-testid="stSidebarCollapseButton"] span {
    font-family:'Material Symbols Rounded' !important;
}
h4,h3,h2,h1 { font-family:'Syne',sans-serif !important; font-weight:800 !important; }
h4 { color:var(--accent) !important; font-size:1.4rem !important; }
[data-testid="stHeading"] h3 {
    color:var(--text) !important; font-size:1.1rem !important;
    padding-left:12px; border-left:3px solid var(--accent); margin-bottom:1.2rem !important;
}
[data-testid="stTextInput"] input, [data-testid="stNumberInput"] input {
    background:var(--bg3) !important; border:1px solid var(--border) !important;
    border-radius:8px !important; color:var(--text) !important;
    font-family:'Space Mono',monospace !important; caret-color:var(--accent);
    transition:border-color .2s,box-shadow .2s;
}
[data-testid="stTextInput"] input:focus, [data-testid="stNumberInput"] input:focus {
    border-color:var(--accent) !important; box-shadow:var(--glow) !important;
}
[data-testid="stTextInput"] label, [data-testid="stNumberInput"] label,
[data-testid="stSelectbox"] label {
    color:var(--muted) !important; font-size:0.75rem !important;
    letter-spacing:0.08em; text-transform:uppercase;
}
[data-testid="stBaseButton-secondary"], [data-testid="stBaseButton-primary"] {
    background:transparent !important; border:1px solid var(--accent) !important;
    color:var(--accent) !important; font-family:'Space Mono',monospace !important;
    font-size:0.8rem !important; letter-spacing:0.1em; text-transform:uppercase;
    border-radius:6px !important; transition:all .2s ease !important;
}
[data-testid="stBaseButton-secondary"]:hover, [data-testid="stBaseButton-primary"]:hover {
    background:rgba(0,245,196,0.1) !important; box-shadow:var(--glow) !important;
    transform:translateY(-1px);
}
[data-testid="stTable"] table {
    background:var(--bg2) !important; border:1px solid var(--border) !important;
    border-radius:10px !important; font-family:'Space Mono',monospace !important; font-size:0.82rem !important;
}
[data-testid="stTable"] thead th {
    background:var(--bg3) !important; color:var(--accent) !important;
    letter-spacing:0.1em; font-size:0.7rem !important; text-transform:uppercase;
    border-bottom:1px solid var(--border) !important; padding:10px 16px !important;
}
[data-testid="stTable"] tbody tr:hover { background:rgba(0,245,196,0.04) !important; }
[data-testid="stTable"] tbody td {
    color:var(--text) !important; border-color:var(--border) !important; padding:8px 16px !important;
}
[data-testid="stSelectbox"] > div > div {
    background:var(--bg3) !important; border:1px solid var(--border) !important;
    border-radius:8px !important; color:var(--text) !important;
}
hr { border:none !important; border-top:1px solid var(--border) !important; margin:1rem 0 !important; }
p, li { font-family:'Syne',sans-serif !important; color:var(--text); }
::-webkit-scrollbar { width:6px; }
::-webkit-scrollbar-track { background:var(--bg2); }
::-webkit-scrollbar-thumb { background:var(--border); border-radius:4px; }
::-webkit-scrollbar-thumb:hover { background:var(--accent); }
</style>
""", unsafe_allow_html=True)


def main():
    st.markdown("#### ⟨ Search Visual and Hashing: TRI WAHYU ⟩")
    menu = st.sidebar.selectbox("Pilih Menu:", ["Searching Visualization", "Hashing"])

    if menu == "Searching Visualization":
        st.write("---")
        st.subheader("Visualisasi Linear Search")
        data_input = st.text_input("Masukkan angka (kasih tanda koma):", "15, 92, 78, 80, 86, 20, 90")
        target = st.number_input("Cari angka:", value=10000)

        arr = None
        try:
            arr = [int(x.strip()) for x in data_input.split(",")]
        except ValueError:
            st.error("Masukkan angka aja Bre!")

        if arr and st.button("Mulai Cari"):
            cols = st.columns(len(arr))
            found = False
            placeholder = st.empty()
            for i in range(len(arr)):
                with cols[i]:
                    if arr[i] == target:
                        st.success(f"[{arr[i]}]")
                        st.write(f"Index {i}")
                        found = True
                        break
                    else:
                        st.warning(f"{arr[i]}")
                        st.write(f"Index {i}")
                        time.sleep(0.3)
            if found:
                placeholder.success(f"Angka {target} ditemukan pada indeks ke-{i}!")
            else:
                placeholder.error(f"Tidak ada angka {target} , cari yang ada bro, gua tahu lu bisa lihat.")


    elif menu == "Hashing":
        st.write("---")
        st.subheader("Implementasi Hashing — Linear Probing")
        if 'hash_table' not in st.session_state:
            st.session_state.hash_table = [None] * 10

        col1, col2 = st.columns([1, 2])
        with col1:
            key_to_insert = st.number_input("Masukkan angka ke Hash Table:", value=99)
            if st.button("Enter"):
                size = 10
                index = key_to_insert % size
                placed = False
                for i in range(size):
                    curr_idx = (index + i) % size
                    if st.session_state.hash_table[curr_idx] is None:
                        st.session_state.hash_table[curr_idx] = key_to_insert
                        st.success(f" Masuk di index {curr_idx}")
                        placed = True
                        break
                    else:
                        st.write(f" Tabrakan di index {curr_idx}...")
                if not placed:
                    st.error(" Hash table penuh Rek!")
            if st.button("Reset Table"):
                st.session_state.hash_table = [None] * 10
                st.rerun()
        with col2:
            table_data = [
                {"Index": i, "Value": val if val is not None else "—"}
                for i, val in enumerate(st.session_state.hash_table)
            ]
            st.table(table_data)


if __name__ == "__main__":
    main()
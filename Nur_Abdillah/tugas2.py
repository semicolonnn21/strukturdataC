import streamlit as st

st.title("Circular Queue Simple")

# Inisialisasi variabel (Kapasitas 8)
if 'q' not in st.session_state:
    st.session_state.q = [None] * 8
    st.session_state.h = -1
    st.session_state.t = -1

size = 8

# Tombol Tambah (Enqueue)
item = st.text_input("Data baru:")
if st.button("Tambah"):
    if ((st.session_state.t + 1) % size) == st.session_state.h:
        st.error("Penuh!")
    else:
        if st.session_state.h == -1: st.session_state.h = 0
        st.session_state.t = (st.session_state.t + 1) % size
        st.session_state.q[st.session_state.t] = item

# Tombol Hapus (Dequeue)
if st.button("Hapus"):
    if st.session_state.h == -1:
        st.error("Kosong!")
    else:
        st.session_state.q[st.session_state.h] = None
        if st.session_state.h == st.session_state.t:
            st.session_state.h = st.session_state.t = -1
        else:
            st.session_state.h = (st.session_state.h + 1) % size

# Tampilan Tabel Horizontal
st.write("Isi Antrean:")
st.table([st.session_state.q])

st.write(f"Indeks Head: **{st.session_state.h}** | Indeks Tail: **{st.session_state.t}**")
import streamlit as st

st.title("Circular Queue Sederhana")

# Inisialisasi
if 'max_size' not in st.session_state:
    st.session_state.max_size = 5
if 'queue' not in st.session_state:
    st.session_state.queue = ["-"] * 5
if 'head' not in st.session_state:
    st.session_state.head = -1
if 'tail' not in st.session_state:
    st.session_state.tail = -1

# Input
item = st.text_input("Masukkan Data")

col1, col2 = st.columns(2)

tambah = col1.button("Enqueue")
hapus = col2.button("Dequeue")

# Enqueue
if tambah:
    if (st.session_state.tail + 1) % st.session_state.max_size == st.session_state.head:
        st.warning("Queue penuh")
    elif item:
        if st.session_state.head == -1:
            st.session_state.head = 0
        
        st.session_state.tail = (st.session_state.tail + 1) % st.session_state.max_size
        st.session_state.queue[st.session_state.tail] = item

# Dequeue
if hapus:
    if st.session_state.head == -1:
        st.warning("Queue kosong")
    else:
        st.session_state.queue[st.session_state.head] = "-"
        
        if st.session_state.head == st.session_state.tail:
            st.session_state.head = -1
            st.session_state.tail = -1
        else:
            st.session_state.head = (st.session_state.head + 1) % st.session_state.max_size

# Tampilan sederhana
st.subheader("Isi Queue:")
st.write(st.session_state.queue)

st.write("HEAD:", st.session_state.head)
st.write("TAIL:", st.session_state.tail)
import streamlit as st

# Inisialisasi
if 'queue' not in st.session_state:
    st.session_state.queue = []
    st.session_state.size = 5
    st.session_state.front = -1
    st.session_state.rear = -1

st.title("Circular Queue Visualization")

# Input
value = st.text_input("Masukkan nilai")

# Fungsi enqueue
def enqueue(val):
    if (st.session_state.rear + 1) % st.session_state.size == st.session_state.front:
        st.warning("Queue penuh!")
        return
    
    if st.session_state.front == -1:
        st.session_state.front = 0
        st.session_state.rear = 0
        st.session_state.queue = [None] * st.session_state.size
        st.session_state.queue[st.session_state.rear] = val
    else:
        st.session_state.rear = (st.session_state.rear + 1) % st.session_state.size
        st.session_state.queue[st.session_state.rear] = val

# Fungsi dequeue
def dequeue():
    if st.session_state.front == -1:
        st.warning("Queue kosong!")
        return
    
    st.session_state.queue[st.session_state.front] = None
    
    if st.session_state.front == st.session_state.rear:
        st.session_state.front = -1
        st.session_state.rear = -1
    else:
        st.session_state.front = (st.session_state.front + 1) % st.session_state.size

# Tombol
col1, col2 = st.columns(2)

with col1:
    if st.button("Enqueue"):
        enqueue(value)

with col2:
    if st.button("Dequeue"):
        dequeue()

# Visualisasi
st.subheader("Queue State")
st.write(st.session_state.queue)

st.write(f"Front: {st.session_state.front}")
st.write(f"Rear: {st.session_state.rear}")
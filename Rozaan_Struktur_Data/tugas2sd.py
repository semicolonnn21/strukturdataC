import streamlit as st

st.title("Circular Queue (Ukuran 8)")

# Ukuran queue
size = 8

# Inisialisasi
if "queue" not in st.session_state:
    st.session_state.queue = [None]*size
    st.session_state.front = -1
    st.session_state.rear = -1

# Enqueue
def enqueue(x):
    if (st.session_state.rear + 1) % size == st.session_state.front:
        st.write("Queue penuh!")
    else:
        if st.session_state.front == -1:
            st.session_state.front = 0
            st.session_state.rear = 0
        else:
            st.session_state.rear = (st.session_state.rear + 1) % size
        
        st.session_state.queue[st.session_state.rear] = x

# Dequeue
def dequeue():
    if st.session_state.front == -1:
        st.write("Queue kosong!")
    else:
        st.session_state.queue[st.session_state.front] = None
        
        if st.session_state.front == st.session_state.rear:
            st.session_state.front = -1
            st.session_state.rear = -1
        else:
            st.session_state.front = (st.session_state.front + 1) % size

# Input
angka = st.number_input("Masukkan angka")

if st.button("Enqueue"):
    enqueue(angka)

if st.button("Dequeue"):
    dequeue()

# Tampilkan isi queue
st.write("Isi Queue:")
st.write(st.session_state.queue)

st.write("Front:", st.session_state.front)
st.write("Rear:", st.session_state.rear)
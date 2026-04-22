import streamlit as st

# Inisialisasi
if "queue" not in st.session_state:
    st.session_state.queue = [None] * 5
    st.session_state.front = -1
    st.session_state.rear = -1
    st.session_state.size = 5
    st.session_state.counter = 1  # nomor pasien

queue = st.session_state.queue
front = st.session_state.front
rear = st.session_state.rear
size = st.session_state.size
counter = st.session_state.counter

st.title("Sistem Antrian Pasien (Circular Queue)")

# Fungsi enqueue
def enqueue():
    global front, rear, counter

    if (rear + 1) % size == front:
        st.error("Antrian PENUH!")
        return

    data = f"Pasien {counter}"

    if front == -1:
        front = rear = 0
    else:
        rear = (rear + 1) % size

    queue[rear] = data
    counter += 1

# Fungsi dequeue
def dequeue():
    global front, rear

    if front == -1:
        st.error("Antrian KOSONG!")
        return None

    data = queue[front]
    queue[front] = None

    if front == rear:
        front = rear = -1
    else:
        front = (front + 1) % size

    return data

# Tombol
col1, col2 = st.columns(2)

if col1.button("Tambah Pasien (Enqueue)"):
    enqueue()

if col2.button("Layani Pasien (Dequeue)"):
    hasil = dequeue()
    if hasil:
        st.success(f"Melayani: {hasil}")

# Simpan state
st.session_state.front = front
st.session_state.rear = rear
st.session_state.counter = counter

# Tampilkan queue
st.subheader("Isi Antrian:")
st.write(queue)

# Info posisi
st.write(f"Front: {front}")
st.write(f"Rear: {rear}")

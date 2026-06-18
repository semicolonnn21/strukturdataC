import streamlit as st

st.set_page_config(page_title="Circular Queue Visualization", layout="centered")

st.title("🔄 Circular Queue Visualization")
st.write("Simulasi antrian menggunakan konsep Circular Queue (wrap-around)")

if "queue" not in st.session_state:
    st.session_state.queue = [None] * 5
    st.session_state.front = -1
    st.session_state.rear = -1
    st.session_state.size = 5


def enqueue(value):
    if (st.session_state.rear + 1) % st.session_state.size == st.session_state.front:
        st.warning("Queue penuh (Overflow)")
        return

    if st.session_state.front == -1:
        st.session_state.front = 0
        st.session_state.rear = 0
    else:
        st.session_state.rear = (st.session_state.rear + 1) % st.session_state.size

    st.session_state.queue[st.session_state.rear] = value


def dequeue():
    if st.session_state.front == -1:
        st.warning("Queue kosong (Underflow)")
        return

    st.session_state.queue[st.session_state.front] = None

    if st.session_state.front == st.session_state.rear:
        st.session_state.front = -1
        st.session_state.rear = -1
    else:
        st.session_state.front = (st.session_state.front + 1) % st.session_state.size


value = st.text_input("Masukkan nilai")

col1, col2 = st.columns(2)

with col1:
    if st.button("Enqueue"):
        if value:
            enqueue(value)
        else:
            st.warning("Masukkan nilai terlebih dahulu")

with col2:
    if st.button("Dequeue"):
        dequeue()

st.subheader("Visualisasi Queue")

cols = st.columns(st.session_state.size)

for i in range(st.session_state.size):
    box_value = st.session_state.queue[i]

    label = f"{box_value}" if box_value is not None else "-"

    if i == st.session_state.front and i == st.session_state.rear and i != -1:
        cols[i].markdown(f"**F/R**\n\n[{label}]")
    elif i == st.session_state.front:
        cols[i].markdown(f"**F**\n\n[{label}]")
    elif i == st.session_state.rear:
        cols[i].markdown(f"**R**\n\n[{label}]")
    else:
        cols[i].markdown(f"\n\n[{label}]")

st.write("---")
st.write(f"Front: {st.session_state.front}")
st.write(f"Rear: {st.session_state.rear}")

st.info("Gunakan enqueue untuk menambah data dan dequeue untuk menghapus data. Circular queue akan kembali ke awal saat mencapai ujung array.")
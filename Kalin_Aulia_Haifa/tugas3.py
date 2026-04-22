import streamlit as st

st.title("Circular Queue")

SIZE = 5

if "q" not in st.session_state:
    st.session_state.q = [None] * SIZE
    st.session_state.head = 0
    st.session_state.tail = 0
    st.session_state.count = 0

val = st.text_input("Masukkan nilai")

if st.button("Enqueue"):
    if st.session_state.count < SIZE:
        st.session_state.q[st.session_state.tail] = val
        st.session_state.tail = (st.session_state.tail + 1) % SIZE 
        st.session_state.count += 1
    else:
        st.error("Queue penuh!")

if st.button("Dequeue"):
    if st.session_state.count > 0:
        st.session_state.q[st.session_state.head] = None
        st.session_state.head = (st.session_state.head + 1) % SIZE  
        st.session_state.count -= 1
    else:
        st.error("Queue kosong!")

st.write("### Antrian:")
cols = st.columns(SIZE)
for i in range(SIZE):
    with cols[i]:
        isi = st.session_state.q[i] if st.session_state.q[i] else "-"
        label = ""
        if i == st.session_state.head and st.session_state.count > 0:
            label = "HEAD"
        if i == (st.session_state.tail - 1) % SIZE and st.session_state.count > 0:
            label = "TAIL"
        st.metric(label=f"[{i}] {label}", value=isi)

st.caption(f"Head: {st.session_state.head} | Tail: {st.session_state.tail} | Isi: {st.session_state.count}/{SIZE}")
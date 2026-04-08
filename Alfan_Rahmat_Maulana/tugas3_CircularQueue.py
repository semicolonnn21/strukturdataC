import streamlit as st

SIZE = 8

# Init
if "queue" not in st.session_state:
    st.session_state.queue = [None] * SIZE
    st.session_state.front = -1
    st.session_state.rear = -1

queue = st.session_state.queue

st.set_page_config(page_title="Circular Queue", layout="centered")

st.title("Circular Queue Visual")
st.caption("Simulasi antrian")

# ======================
# FUNCTION
# ======================
def enqueue(data):
    if (st.session_state.rear + 1) % SIZE == st.session_state.front:
        st.error("Queue penuh!")
        return

    if st.session_state.front == -1:
        st.session_state.front = 0
        st.session_state.rear = 0
    else:
        st.session_state.rear = (st.session_state.rear + 1) % SIZE

    queue[st.session_state.rear] = data


def dequeue():
    if st.session_state.front == -1:
        st.warning("Queue kosong!")
        return

    queue[st.session_state.front] = None

    if st.session_state.front == st.session_state.rear:
        st.session_state.front = -1
        st.session_state.rear = -1
    else:
        st.session_state.front = (st.session_state.front + 1) % SIZE


# ======================
# INPUT UI
# ======================
st.subheader("Input Data")

col1, col2 = st.columns([2,1])

with col1:
    data = st.number_input("Masukkan angka", step=1)

with col2:
    st.write("")
    if st.button("➕ Enqueue"):
        enqueue(data)
    if st.button("➖ Dequeue"):
        dequeue()

# ======================
# VISUAL BOX
# ======================
st.subheader("Visual Queue")

cols = st.columns(SIZE)

for i in range(SIZE):
    val = queue[i] if queue[i] is not None else ""

    color = "#2E86C1"  # default

    if i == st.session_state.front:
        color = "#28B463"  # hijau
    elif i == st.session_state.rear:
        color = "#E74C3C"  # merah

    with cols[i]:
        st.markdown(
            f"""
            <div style="
                background-color:{color};
                padding:20px;
                border-radius:10px;
                text-align:center;
                color:white;
                font-weight:bold;
            ">
                {val}
            </div>
            <p style='text-align:center;'>Index {i}</p>
            """,
            unsafe_allow_html=True
        )

# ======================
# INFO
# ======================
st.subheader("Status")
col1, col2 = st.columns(2)

col1.metric("Front", st.session_state.front)
col2.metric("Rear", st.session_state.rear)
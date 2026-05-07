import streamlit as st

# Kapasitas queue
MAX = 7

if "queue" not in st.session_state:
    st.session_state.queue = [None] * MAX
    st.session_state.front = -1
    st.session_state.rear = -1
    st.session_state.document = 1  # nomor job otomatis

st.title("🖨️ Antrian Printer Kang Fotocopy")

def generate_document_name():
    job = f"Doc-{st.session_state.document:02d}"
    st.session_state.document += 1
    return job

# Enqueue (tambah dokumen)
def tambah_dokumen():
    if (st.session_state.rear + 1) % MAX == st.session_state.front:
        st.error("Antrian Printer Penuh!")
    else:
        job = generate_document_name()

        if st.session_state.front == -1:
            st.session_state.front = 0
            st.session_state.rear = 0
        else:
            st.session_state.rear = (st.session_state.rear + 1) % MAX

        st.session_state.queue[st.session_state.rear] = job
        st.success(f"Dokumen masuk: {job}")

# Dequeue (cetak dokumen)
def cetak_dokumen():
    if st.session_state.front == -1:
        st.warning("Tidak ada dokumen untuk dicetak!")
    else:
        job = st.session_state.queue[st.session_state.front]
        st.success(f"Sedang mencetak: {job}")
        st.session_state.queue[st.session_state.front] = None

        if st.session_state.front == st.session_state.rear:
            st.session_state.front = -1
            st.session_state.rear = -1
        else:
            st.session_state.front = (st.session_state.front + 1) % MAX

# Tombol
col1, col2 = st.columns(2)

with col1:
    if st.button("Tambah Dokumen"):
        tambah_dokumen()

with col2:
    if st.button("Cetak Dokumen"):
        cetak_dokumen()

# Visualisasi queue
st.subheader("📄 Daftar Antrian Printer")

cols = st.columns(MAX)

for i in range(MAX):
    isi = st.session_state.queue[i]

    if isi is None:
        text = f"[{i}] \n Kosong"
    else:
        text = f"[{i}] \n {isi}"

        if i == st.session_state.front:
            text += "\n (Sedang dicetak)"
        if i == st.session_state.rear:
            text += "\n (Terakhir)"

    cols[i].write(text)
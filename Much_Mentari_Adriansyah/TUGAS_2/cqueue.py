import streamlit as st

st.set_page_config(page_title="Antrian Pasien (Circular Queue)", layout="centered")
st.title("🏥 Antrian Pasien (Circular Queue)")
st.caption("FIFO + wrap-around (melingkar)")

# === KAPASITAS ===
capacity = st.slider("Kapasitas", 3, 11, 5)

# === INISIALISASI STATE ===
if 'queue' not in st.session_state:
    st.session_state.queue = [None] * capacity
    st.session_state.front = -1
    st.session_state.rear = -1
    st.session_state.capacity = capacity

# Reset jika kapasitas berubah
if st.session_state.capacity != capacity:
    # Ambil data lama berurutan dari front ke rear
    old_items = []
    if st.session_state.front != -1:
        f = st.session_state.front
        r = st.session_state.rear
        cap_old = st.session_state.capacity
        i = f
        while True:
            if st.session_state.queue[i] is not None:
                old_items.append(st.session_state.queue[i])
            if i == r:
                break
            i = (i + 1) % cap_old
    
    # Reset dengan kapasitas baru
    st.session_state.queue = [None] * capacity
    st.session_state.front = -1
    st.session_state.rear = -1
    st.session_state.capacity = capacity
    
    # Masukkan ulang data (sebatas kapasitas baru)
    for item in old_items[:capacity]:
        if st.session_state.front == -1:
            st.session_state.front = 0
            st.session_state.rear = 0
            st.session_state.queue[0] = item
        else:
            next_rear = (st.session_state.rear + 1) % capacity
            if next_rear != st.session_state.front:
                st.session_state.rear = next_rear
                st.session_state.queue[st.session_state.rear] = item

# === FUNGSI CIRCULAR QUEUE ===
def enqueue(data):
    queue = st.session_state.queue
    front = st.session_state.front
    rear = st.session_state.rear
    cap = st.session_state.capacity
    
    if (rear + 1) % cap == front:
        return False, "Antrian PENUH!"
    
    if front == -1:
        st.session_state.front = 0
        st.session_state.rear = 0
        queue[0] = data
    else:
        next_rear = (rear + 1) % cap
        st.session_state.rear = next_rear
        queue[next_rear] = data
    return True, f"✅ {data} masuk antrian"

def dequeue():
    queue = st.session_state.queue
    front = st.session_state.front
    rear = st.session_state.rear
    cap = st.session_state.capacity
    
    if front == -1:
        return False, "Antrian KOSONG!"
    
    removed = queue[front]
    queue[front] = None
    
    if front == rear:
        st.session_state.front = -1
        st.session_state.rear = -1
    else:
        st.session_state.front = (front + 1) % cap
    return True, f"👨‍⚕️ {removed} sudah dilayani"

def reset():
    st.session_state.queue = [None] * st.session_state.capacity
    st.session_state.front = -1
    st.session_state.rear = -1

# === SIDEBAR KONTROL ===
st.sidebar.header("Kontrol")

nama = st.sidebar.text_input("Nama Pasien")

col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("➕ Tambah"):
        if nama:
            ok, msg = enqueue(nama)
            if ok:
                st.sidebar.success(msg)
            else:
                st.sidebar.error(msg)
            st.rerun()
        else:
            st.sidebar.warning("Isi nama dulu!")

with col2:
    if st.button("👨‍⚕️ Layani"):
        ok, msg = dequeue()
        if ok:
            st.sidebar.success(msg)
        else:
            st.sidebar.warning(msg)
        st.rerun()

if st.sidebar.button("🔄 Reset"):
    reset()
    st.rerun()

# === VISUALISASI SEDERHANA ===
st.subheader("📊 Keadaan Antrian")

# Hitung jumlah pasien
jumlah = sum(1 for x in st.session_state.queue if x is not None)

# Tampilkan status
col_a, col_b, col_c = st.columns(3)
with col_a:
    st.metric("Front Index", st.session_state.front if st.session_state.front != -1 else "-")
with col_b:
    st.metric("Rear Index", st.session_state.rear if st.session_state.rear != -1 else "-")
with col_c:
    st.metric("Terisi", f"{jumlah}/{capacity}")

# Tampilkan antrian dalam bentuk tabel
st.write("**Slot Memori:**")
for i in range(capacity):
    val = st.session_state.queue[i]
    tanda = ""
    if i == st.session_state.front and i == st.session_state.rear:
        tanda = " 🔄 DEPAN & BELAKANG"
    elif i == st.session_state.front:
        tanda = " 🔴 DEPAN"
    elif i == st.session_state.rear:
        tanda = " 🔵 BELAKANG"
    
    if val is None:
        st.text(f"[{i}] : (kosong){tanda}")
    else:
        st.text(f"[{i}] : {val}{tanda}")

# Tampilkan urutan antrian dari depan ke belakang
if st.session_state.front != -1:
    st.write("**Urutan antrian (dari depan):**")
    urutan = []
    i = st.session_state.front
    while True:
        if st.session_state.queue[i] is not None:
            urutan.append(st.session_state.queue[i])
        if i == st.session_state.rear:
            break
        i = (i + 1) % capacity
    st.write(" → ".join(urutan))
else:
    st.info("Antrian kosong")

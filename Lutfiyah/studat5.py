import streamlit as st

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Aplikasi Algoritma & Struktur Data", layout="centered")

# ==========================================
# LOGIKA & FUNGSI BINARY SEARCH
# ==========================================
def binarySearch(arr, x):
    low = 0
    high = len(arr) - 1
    history = []
    while low <= high:
        mid = low + (high - low) // 2
        history.append({"low": low, "mid": mid, "high": high})
        if arr[mid] == x:
            return mid, history
        elif arr[mid] < x:
            low = mid + 1
        else:
            high = mid - 1
    return -1, history

def tampilkan_binary_search():
    st.title("🔍 Visualisasi Binary Search")
    st.write("Cari indeks angka dalam list yang sudah terurut.")

    # Input User
    input_data = st.text_input("Masukkan angka (pisahkan dengan koma):", "15, 25, 35, 45, 55, 65, 75, 85, 95")
    target = st.number_input("Angka yang ingin dicari:", value=35)

    if st.button("Cari Sekarang"):
        try:
            # Olah data
            arr = sorted([int(i.strip()) for i in input_data.split(",")])
            st.info(f"Array Terurut: {arr}")
            
            result, steps = binarySearch(arr, target)

            if result != -1:
                st.success(f"**Elemen ditemukan!** Angka {target} berada di **indeks {result}**.")
            else:
                st.error(f"**Elemen tidak ditemukan.** Angka {target} tidak ada dalam list.")

            with st.expander("Lihat Langkah Pencarian"):
                for i, step in enumerate(steps):
                    st.write(f"Langkah {i+1}: Indeks tengah {step['mid']} (Nilai: {arr[step['mid']]})")
        except ValueError:
            st.warning("Format salah! Gunakan angka dipisah koma (Contoh: 10, 20, 30)")

# ==========================================
# LOGIKA & KELAS HASHING
# ==========================================
class Hash:
    def __init__(self, bucket):
        self.__bucket = bucket
        self.__table = [[] for _ in range(bucket)]

    def hashFunction(self, key):
        return (key % self.__bucket)

    def insertItem(self, key):
        index = self.hashFunction(key)
        self.__table[index].append(key)

    def deleteItem(self, key):
        index = self.hashFunction(key)
        if key in self.__table[index]:
            self.__table[index].remove(key)
            return True
        return False

    def get_table(self):
        return self.__table

def tampilkan_hashing():
    st.title("🗄️ Visualisasi Hashing (Chaining)")
    st.write("Simulasi tabel hash dengan ukuran bucket tetap (7).")

    # Inisialisasi State agar data tidak hilang saat menu berpindah
    if 'hash_table' not in st.session_state:
        st.session_state.hash_table = Hash(7)

    # Kontrol di Sidebar (Khusus menu Hashing)
    st.sidebar.divider()
    st.sidebar.subheader("⚙️ Kontrol Hashing")
    angka_hash = st.sidebar.number_input("Input Angka Hash:", value=10, step=1)
    
    c1, c2 = st.sidebar.columns(2)
    if c1.button("Tambah"):
        st.session_state.hash_table.insertItem(angka_hash)
        st.toast(f"Ditambah: {angka_hash}")

    if c2.button("Hapus"):
        if st.session_state.hash_table.deleteItem(angka_hash):
            st.toast(f"Dihapus: {angka_hash}")
        else:
            st.sidebar.error("Data tak ada")

    if st.sidebar.button("🗑️ Reset Tabel"):
        st.session_state.hash_table = Hash(7)
        st.rerun()

    # Tampilan Utama Hashing
    st.subheader("Struktur Tabel Hash (MOD 7):")
    tabel = st.session_state.hash_table.get_table()
    for i, isi in enumerate(tabel):
        row = f"**[{i}]** : "
        if not isi:
            row += "*(Kosong)*"
        else:
            row += " → ".join([f"`{str(x)}`" for x in isi])
        st.markdown(row)

# ==========================================
# MENU NAVIGASI (SIDEBAR)
# ==========================================
st.sidebar.title("📌 Menu Utama")
pilihan = st.sidebar.selectbox(
    "Pilih Visualisasi Algoritma:",
    ["Binary Search", "Hashing"]
)

# Menjalankan fungsi sesuai pilihan menu
if pilihan == "Binary Search":
    tampilkan_binary_search()
else:
    tampilkan_hashing()

# Footer
st.sidebar.divider()
st.sidebar.caption("Tugas Struktur Data | Python & Streamlit")
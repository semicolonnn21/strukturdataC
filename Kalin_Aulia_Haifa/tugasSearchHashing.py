import streamlit as st

st.sidebar.title("Menu Tugas")
pilihan = st.sidebar.radio("Pilih Visualisasi:", ["Binary Search", "Hashing"])

if pilihan == "Binary Search":
    st.title("🔍 Visualisasi Binary Search")
    st.write("Algoritma ini mencari angka dengan membelah data menjadi dua bagian terus-menerus.")

    data_array = [20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
    st.info(f"**Data Terurut:** {data_array}")

    target = st.number_input("Cari angka berapa?", value=26)

    if st.button("Mulai Cari"):
        left, right = 0, len(data_array) - 1
        found = False
        step = 1
        
        while left <= right:
            mid = (left + right) // 2
            st.markdown(f"#### Langkah {step}")
            st.write(f"🔍 **Mencari di antara urutan:** `{left}` hingga `{right}`")
            
            visual = [f"**[{data_array[i]}]**" if i == mid else f"{data_array[i]}" for i in range(len(data_array))]
            st.write(" | ".join(visual))
            
            if data_array[mid] == target:
                st.success(f"🎉 Ketemu! {target} ada di indeks ke-{mid}")
                found = True
                break
            elif data_array[mid] < target:
                st.warning(f"{data_array[mid]} kekecilan, geser ke kanan.")
                left = mid + 1
            else:
                st.warning(f"{data_array[mid]} kegedean, geser ke kiri.")
                right = mid - 1
            step += 1
        if not found:
            st.error("Yah, angkanya nggak ketemu.")

elif pilihan == "Hashing":
    st.title("🗄️ Visualisasi Hashing")
    st.write("Menyimpan data langsung ke 'alamat' (indeks) tertentu menggunakan rumus Modulo.")

    SIZE = 10
    if 'hash_table' not in st.session_state:
        st.session_state.hash_table = [None] * SIZE

    input_data = st.number_input("Masukkan angka untuk disimpan:", value=0)
    
    if st.button("Simpan ke Tabel"):
        index = input_data % SIZE
        steps = 0
        found_spot = False
        
        while steps < SIZE:
            if st.session_state.hash_table[index] is None:
                st.session_state.hash_table[index] = input_data
                st.success(f"Angka {input_data} masuk ke loker nomor {index}")
                found_spot = True
                break
            else:
                st.warning(f"Loker {index} penuh! Cek loker bawahnya...")
                index = (index + 1) % SIZE
                steps += 1
        
        if not found_spot:
            st.error("Tabel sudah penuh banget!")

    st.write("### Isi Tabel Saat Ini:")
    cols = st.columns(SIZE)
    for i in range(SIZE):
        with cols[i]:
            st.code(f"[{i}]")
            val = st.session_state.hash_table[i]
            st.write(val if val is not None else "-")

    if st.button("Kosongkan Tabel"):
        st.session_state.hash_table = [None] * SIZE
        st.rerun()
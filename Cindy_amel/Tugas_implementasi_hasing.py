import streamlit as st
import time
import os

def main():
    # Judul simpel
    st.markdown("#### Tugas Implementasi Hasing: Cindy Amelia")
    
    menu = st.sidebar.selectbox("Pilih Menu:", ["Searching Visualization", "Hashing (Linear Probing)"])

    if menu == "Searching Visualization":
        st.write("---")
        st.subheader("Visualisasi Linear Search")
        
        data_input = st.text_input("Masukkan angka (pisahkan dengan koma):", "10, 25, 40, 55, 70, 85, 100")
        target = st.number_input("Cari angka:", value=99)
        
        try:
            arr = [int(x.strip()) for x in data_input.split(",")]
        except ValueError:
            st.error("Masukkan angka saja ya!")
            st.stop()

    if st.button("Mulai Cari"):
        cols = st.columns(len(arr))
        found = False
        placeholder = st.empty()
        
        for i in range(len(arr)):
            with cols[i]:
                if arr[i] == target:
                    st.success(f"[{arr[i]}]")
                    st.write(f"Index {i}")
                    found = True
                    break
                else:
                    st.warning(f"{arr[i]}")
                    st.write(f"Index {i}")
                    time.sleep(0.3)
        
        if found:
            placeholder.success(f"Angka {target} ditemukan pada indeks ke-{i}!")
        else:
            placeholder.error(f"Yah, angka {target} nggak ada...")
            
            nama_file_gambar = 'lucu.png'
            
            if os.path.exists(nama_file_gambar):
                # Teks caption dikosongkan sesuai permintaan
                st.image(nama_file_gambar, caption="", width=300)

    elif menu == "Hashing (Linear Probing)":
        st.write("---")
        st.subheader("Implementasi Hashing - Linear Probing")
        
        if 'hash_table' not in st.session_state:
            st.session_state.hash_table = [None] * 10
            
        col1, col2 = st.columns([1, 2])
        
        with col1:
            key_to_insert = st.number_input("Masukkan angka ke Hash Table:", value=207)
            if st.button("Insert"):
                size = 10
                index = key_to_insert % size
                placed = False
                for i in range(size):
                    curr_idx = (index + i) % size
                    if st.session_state.hash_table[curr_idx] is None:
                        st.session_state.hash_table[curr_idx] = key_to_insert
                        st.success(f"Masuk di index {curr_idx}")
                        placed = True
                        break
                    else:
                        st.write(f"Tabrakan di index {curr_idx}...")
                
                if not placed:
                    st.error("Penuh!")

            if st.button("Reset Table"):
                st.session_state.hash_table = [None] * 10
                st.rerun()

        with col2:
            table_data = []
            for i, val in enumerate(st.session_state.hash_table):
                table_data.append({"Index": i, "Value": val if val is not None else "-"})
            st.table(table_data)

if __name__ == "__main__":
    main()
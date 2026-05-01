import streamlit as st

# Mengatur tampilan halaman (page)
st.set_page_config(page_title="Word Count🤩😜", layout="wide")

st.title("📝 Word count")

# Garis batas
st.divider()

# Identitas (Bisa pakai kolom agar rapi)
col_nama, col_nim, col_mk, col_class = st.columns(4)
with col_nama:
    st.write("**Nama:** Hafidzar Ashyawal Sinatryas")
with col_nim:
    st.write("**NIM:** 2530801075")
with col_mk:
    st.write("**Mata kuliah:** Struktur Data")
with col_class:
    st.write("**Kelas:** 2/C")

st.divider()

# Input area untuk teks panjang
input_teks = st.text_area("Masukkan teks kamu di sini:", height=200)

if input_teks:
    # Menghitung kata dengan split()
    # split() tanpa argumen otomatis menangani spasi ganda dan baris baru
    words = input_teks.split()
    jumlah_kata = len(words)
    
    # Menghitung karakter (dengan dan tanpa spasi)
    char_total = len(input_teks)
    char_no_space = len(input_teks.replace(" ", ""))

    # Menampilkan hasil dalam kolom agar rapi
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Jumlah Kata", jumlah_kata)
    
    with col2:
        st.metric("Total Karakter", char_total)
        
    with col3:
        st.metric("Tanpa Spasi", char_no_space)

    # Fitur tambahan: Menampilkan 5 kata pertama sebagai preview
    if jumlah_kata > 0:
        st.info(f"Preview 5 kata pertama: {', '.join(words[:5])}...")
else:
    st.write("Silahkan ketik sesuatu untuk mulai menghitung.")

st.balloons
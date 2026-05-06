import streamlit as st

st.set_page_config(page_title="Operasi Set", layout="centered") # Mengatur tampilan halaman
st.title("🔢 Visualisasi Operasi Set") # Judul applikasi
st.write("Masukkan elemen set dipisahkan dengan koma (contoh: a,b,c)") # Petunjuk input

# Membuat 2 kolom untuk input
col1, col2 = st.columns(2)

with col1:
    input_A = st.text_input("Set A") # Input untuk Set A
with col2:
    input_B = st.text_input("Set B") # Input untuk Set B

# Jika kedua input sudah diisi 
if input_A and input_B:
    # Mengubah input string menjadi Set
    set_A = set([x.strip() for x in input_A.split(",")])
    set_B = set([x.strip() for x in input_B.split(",")])

    st.divider()
    st.subheader("📊 Hasil Operasi")

    # Tampilkan isi Set
    st.write("🔵 A =", set_A)
    st.write("🟢 B =", set_B)

    # Membuat 2 kolom untuk hasil
    col1, col2 = st.columns(2)

    with col1:
        st.success(f"Union\n{set_A | set_B}") # Gabungan/Union 2 Set
        st.info(f"Intersection\n{set_A & set_B}") # Irisan/Intersection 2 Set

    with col2:
        st.warning(f"A - B\n{set_A - set_B}") # Selisih A terhadap B
        st.error(f"Symmetric Diff\n{set_A ^ set_B}") # Elemen yang berbeda di A dan B

    st.divider() 
    st.caption("✨ Dibuat dengan Streamlit")
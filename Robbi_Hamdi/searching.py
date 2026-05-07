import streamlit as st

st.title("Searching dan Hashing Sederhana")

menu = st.selectbox("Pilih", ["Searching", "Hashing"])

# SEARCHING
if menu == "Searching":
    data = [10, 20, 30, 40, 50]
    cari = st.number_input("Cari angka", step=1)

    if st.button("Cari"):
        if cari in data:
            st.success(f"{cari} ditemukan")
        else:
            st.error(f"{cari} tidak ditemukan")

    st.write("Data:", data)

# HASHING
else:
    data = {
        "nama": "Brata",
        "kelas": "Informatika"
    }

    key = st.text_input("Masukkan key")

    if st.button("Cari Key"):
        if key in data:
            st.success(f"Value: {data[key]}")
        else:
            st.error("Key tidak ditemukan")

    st.write(data)
import streamlit as st

st.title("Visualisasi Operasi Set")

# Input dari user (misal angka dipisahkan koma)
input_a = st.text_input("Masukkan anggota Set A (pisahkan dengan koma)", "1, 2, 3, 4")
input_b = st.text_input("Masukkan anggota Set B (pisahkan dengan koma)", "3, 4, 5, 6")

# Ubah input string menjadi set
set_a = set([x.strip() for x in input_a.split(",")])
set_b = set([x.strip() for x in input_b.split(",")])

# Pilihan Operasi
operasi = st.selectbox("Pilih Operasi Set", ["Union", "Intersection", "Difference", "Symmetric Difference"])

if operasi == "Union":
    hasil = set_a.union(set_b)
elif operasi == "Intersection":
    hasil = set_a.intersection(set_b)
elif operasi == "Difference":
    hasil = set_a.difference(set_b)
else:
    hasil = set_a.symmetric_difference(set_b)

st.write(f"Hasil {operasi}:")
st.write(hasil)

st.title("Word Count Komentar")

# Input teks/komentar
teks = st.text_area("Masukkan komentar di sini:", "Belajar streamlit itu seru dan streamlit itu mudah")
if teks:
    # Proses menghitung kata
    kata_list = teks.lower().split()
    dictionary_hitung = {}
    
    for k in kata_list:
        dictionary_hitung[k] = dictionary_hitung.get(k, 0) + 1
    
    # Menampilkan hasil dalam bentuk tabel/bar chart agar lebih visual
    st.write("Frekuensi Kata:")
    st.bar_chart(dictionary_hitung)
    st.write(dictionary_hitung) # Menampilkan Key dan Value-nya
    
    

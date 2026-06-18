import streamlit as st

st.title("Visualisasi Operasi Set")

# Input anggota himpunan
input_a = st.text_input("Masukkan anggota Set A (Pisahkan setiap anggota dengan tanda koma)", "1, 2, 3, 4")
input_b = st.text_input("Masukkan anggota Set B (Pisahkan setiap anggota dengan tanda koma)", "3, 4, 5, 6")

# Ubah input string menjadi set
set_a = set([x.strip() for x in input_a.split(",")])
set_b = set([x.strip() for x in input_b.split(",")])

st.write("Set A:", set_a)
st.write("Set B:", set_b)

# Pilih Operasi Set
operasi = st.selectbox("Pilih Operasi Set yang ingin digunakan", ["Union", "Intersection", "Difference", "Symmetric Difference"])

if operasi == "Union":
    hasil = set_a.union(set_b)
elif operasi == "Intersection":
    hasil = set_a.intersection(set_b)
elif operasi == "Difference":
    hasil = set_a.difference(set_b)
else:
    hasil = set_a.symmetric_difference(set_b)

st.success(f"Hasil {operasi}: {hasil}")

#Untuk Garis Pemisah
st.divider()

st.title("Word Count")

# Input teks komentar
teks = st.text_area("Masukkan komentar di sini:", "Belajar streamlit itu menyenangkan, mudah dan itu seru")

if st.button("Hitung Frekuensi Kata"):
    if teks:
        # Kecilkan semua huruf dan pecah kalimat menjadi daftar kata
        kata_list = teks.lower().split()
        
        # wadah kosong (Dictionary) untuk menyimpan hasil
        dictionary_hitung = {}

        # Perulangan untuk mengecek satu per satu kata
        for k in kata_list:
            if k in dictionary_hitung:
                dictionary_hitung[k] += 1
            else:
                dictionary_hitung[k] = 1

        st.subheader("Hasil (Dictionary)")
        st.write(dictionary_hitung)

        # Visualisasi grafik 
        st.subheader("Visualisasi Frekuensi")
        st.bar_chart(dictionary_hitung)
        
        # Detail setiap kata
        for kata, jumlah in dictionary_hitung.items():
            st.text(f"{kata} : {jumlah}")
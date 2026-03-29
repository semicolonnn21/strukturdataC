import streamlit as st
import matplotlib.pyplot as plt
from matplotlib_venn import venn2
import pandas as pd

st.title("Tugas Struktur Data: Operasi Set dan Word Count Komentar Sosial Media")

# Navigation
with st.sidebar:
    pilih_menu = st.radio("Pilih Tugas", ["Operasi Set", "Word Count Komentar Sosial Media"])

if pilih_menu == "Operasi Set":
    st.subheader("Operasi Set")

    # Input Set A dan Set B
    setA_input = st.text_input("Masukkan elemen Set A (pisahkan dengan koma)", "2,3,5,7")
    setB_input = st.text_input("Masukkan elemen Set B (pisahkan dengan koma)", "3,4,5,6")

    # Konversi input menjadi set
    setA = set(setA_input.split(","))
    setB = set(setB_input.split(","))

    st.write("Set A:", setA)
    st.write("Set B:", setB)

    st.subheader("Pilih Operasi Set yang Ingin Dilihat")

    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        # Membuat checkbox
        union = st.checkbox("Union (Gabungan)")
        intersection = st.checkbox("Intersection (Irisan)")
        difference = st.checkbox("Difference (Selisih)")
        symmetric_difference = st.checkbox("Symmetric Difference (Selisih Simetris)")

    with col2:  
        # Fungsi buat gambar diagram
        def buat_venn(seta, setb, judul, warna_id=None):
            fig, ax = plt.subplots(figsize=(6, 4))
            v = venn2([seta, setb], set_labels=('Set A', 'Set B'), ax=ax)
            
            # Ganti label jumlah jadi isi angka
            if v.get_label_by_id('10'): v.get_label_by_id('10').set_text(str(seta-setb))
            if v.get_label_by_id('01'): v.get_label_by_id('01').set_text(str(setb-seta))
            if v.get_label_by_id('11'): v.get_label_by_id('11').set_text(str(seta&setb))
            
            # Atur warna bagian yang dipilih
            if warna_id:
                for id_area in warna_id:
                    if v.get_patch_by_id(id_area):
                        v.get_patch_by_id(id_area).set_alpha(0.8)
                        v.get_patch_by_id(id_area).set_color('yellow')
            
            st.write(f"{judul}")
            st.pyplot(fig)

        # Tampilkan hasil operasi set dan visualisasinya
        if union:
            st.success(f"Union (A ∪ B): {setA|setB}")
            buat_venn(setA, setB, "Venn Diagram Union", ['10', '01', '11'])

        if intersection:
            st.success(f"Intersection (A ∩ B): {setA&setB}")
            buat_venn(setA, setB, "Venn Diagram Intersection", ['11'])

        if difference:
            st.success(f"Difference (A - B): {setA-setB}")
            st.success(f"Difference (B - A): {setB-setA}")  
            buat_venn(setA, setB, "Venn Diagram Difference", ['10'])

        if symmetric_difference:
            st.success(f"Symmetric Difference (A △ B): {setA^setB}")
            buat_venn(setA, setB, "Venn Diagram Symmetric Difference", ['10', '01'])

elif pilih_menu == "Word Count Komentar Sosial Media":
    st.header("Word Count Komentar Sosial Media")
    
    # 1. Input Komentar
    teks = st.text_area("Masukkan komentar di sini:")

    if teks:
        # 2. Preprocessing (Lowercase + Split)
        list_kata = teks.lower().split()

        # 3. Hitung Frekuensi Kata
        counts = {}
        for kata in list_kata:
            # Bersihkan tanda baca di awal/akhir kata
            kata = kata.strip(".,!?:;\"'-()")
            if kata: 
                counts[kata] = counts.get(kata, 0) + 1

        # 4. Penyajian (Ubah ke DataFrame agar bisa jadi Tabel & Grafik)
        # Mengubah dictionary counts menjadi tabel
        df = pd.DataFrame(list(counts.items()), columns=['Kata', 'Frekuensi'])
        
        # Urutkan dari yang terbanyak
        df = df.sort_values(by='Frekuensi', ascending=False)

        # 5. Tampilkan ke Layar
        st.subheader("Hasil Frekuensi Kata")
        
        col_tabel, col_grafik = st.columns(2)
        with col_tabel:
            st.dataframe(df) # Menampilkan tabel interaktif
            
        with col_grafik:
            st.bar_chart(data=df, x='Kata', y='Frekuensi') # Menampilkan grafik batang
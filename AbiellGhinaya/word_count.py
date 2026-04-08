import streamlit as st

# 1. Mengatur tampilan halaman (page)
st.set_page_config(page_title="Project WordCount📒", layout="wide") # wide: kesamping

# 2. Judul project
st.title("Word Count \'NGAWI\'📝")
st.caption("***Tugas Project Mata kuliah \'Struktur Data\'*** 😌")

# 3. Garis batas
st.divider()

# 4. Identitas (Bisa pakai kolom agar rapi)
col_nama, col_nim, col_mk, col_class = st.columns(4)
with col_nama:
    st.write("**Nama:** Abil Ghinaya Azka")
with col_nim:
    st.write("**NIM:** 2530801056")
with col_mk:
    st.write("**Mata kuliah:** Struktur Data")
with col_class:
    st.write("**Kelas:** II C")

st.divider()

# 5. Instruksi pengisian
word_input = st.text_area("**Silahkan Masukkan komentar disini:**", placeholder="Example: FURAB selalu di hati💜", height=200)
word_input.lower()

# 6. Logika input
if word_input:
    st.success("**Terima kasih, telah mengisi komentar** 🙏")
    teks = word_input.lower() # Jadi kecil semua
    
    # 7. Konversi semua simbol menjadi 'tidak ada'
    tanda_baca = ".,!?;:()\"'-" # Semua simbol 
    tampung = {} # Dict sebagai penampung

    for simbol in tanda_baca:
        teks = teks.replace(simbol, "") # Ubah simbol jadi space kosong

    daftar_kata = teks.split() # Kasih Jeda per-kata

    for daftar in daftar_kata: # Menghitung dengan perulangan

        if daftar in tampung:
            tampung[daftar] += 1

        else:
            tampung[daftar] = 1

    st.divider()

    st.subheader("📊Hasil analisis \'NGAWI\'")
    st.metric("**Total kata:**", len(daftar_kata)) # Menampilkan hasil dengan angka yang menonjol

    # Frekuensi data dalam bentuk dict (file json)
    st.write("**Rincian Frekuensi Kata:**")
    st.json(tampung) 

    st.write("**Visualisasi Frekuensi Kata:**")
    st.bar_chart(daftar_kata) # Menampilkan dalam bentuk diagram
    
    st.toast("**Keren bung!!**", icon="🚀")
    st.snow() # Efek salju

else:
    st.warning("⚠️ **Harap isi komentar!**")
import streamlit as st
from collections import Counter # Import Counter untuk menghitung kata

st.set_page_config(page_title="Word Count", layout="centered") # Mengatur tampilan halaman

st.title("📝 Word Count Komentar") # Judul aplikasi
st.write("Masukkan teks, nanti akan dihitung jumlah tiap kata") # Petunjuk Input

text = st.text_area("Tulis komentar di sini...") # Input teks dari user

# Jika ada teks yang dimasukan
if text:
    words = text.lower().split() # Mengubah ke huruf kecil lalu memecah kata
    
    # Bersihkan tanda baca dari setiap kata
    clean_words = [w.strip(".,!?()[]{}\"'") for w in words]

    # Menghitung jumlah kemunculan tiap kata
    word_count = Counter(clean_words)

    st.divider()
    st.subheader("📊 Hasil Perhitungan")

    # Tampilkan total kata
    st.metric("Total Kata", len(clean_words)) # Total semua kata
    st.metric("Kata Unik", len(word_count)) # Jumlah kata unik

    st.divider()

    # Visualisasi 
    st.subheader("📊 Visualisasi Frekuensi Kata")
    st.bar_chart(word_count)

    st.divider()
    
    # Tampilkan hasil per kata
    for word, count in word_count.items():
        st.write(f"🔹 **{word}** : {count}")

    st.divider()
    st.success("✅ Perhitungan selesai!")

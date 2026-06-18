import streamlit as st
import re

st.set_page_config(page_title="Word Count Pro",)

# 🎨 Background Gradient + Style
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #ff1a1a, #000000);
        color: white;
    }
    .stButton>button {
        background-color: #ff4d4d;
        color: white;
        border-radius: 10px;
        height: 50px;
        width: 100%;
        font-size: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 🔥 Judul
st.title(" Word Count Analyzer ")
st.write("Analisis komentar + grafik + ranking + filter kata umum")

# 📥 Input teks
text = st.text_area("Masukkan komentar kamu")

# 🚫 Stopwords (kata umum)
stopwords = ["aku", "kamu", "dan", "yang", "di", "ke", "dari", "itu", "ini"]

# 🚀 Tombol proses
if st.button("🚀 Proses"):
    if text:
        # Bersihkan teks
        text = re.sub(r'[^\w\s]', '', text.lower())

        words = text.split()

        # Filter kata umum
        words = [word for word in words if word not in stopwords]

        count = {}
        for word in words:
            count[word] = count.get(word, 0) + 1

        st.success("✅ Analisis selesai!")

        st.info(f"Total kata (setelah filter): {len(words)}")

        # Sorting ranking
        sorted_count = dict(sorted(count.items(), key=lambda x: x[1], reverse=True))

        # 📊 Hasil teks
        st.subheader("📊 Frekuensi Kata:")
        for word, jumlah in sorted_count.items():
            st.write(f"🔹 {word} : {jumlah}")

        # 🏆 Top 5
        st.subheader("🏆 Top 5 Kata Terbanyak:")
        top5 = dict(list(sorted_count.items())[:5])
        st.write(top5)

        # 📈 Grafik
        st.subheader("📈 Grafik Frekuensi Kata")
        st.bar_chart(sorted_count)

    else:
        st.warning("⚠️ Masukkan teks terlebih dahulu!")
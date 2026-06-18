import streamlit as st

st.set_page_config(page_title="Operasi Set ", )

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

# Judul
st.title(" Visualisasi Operasi Set ")
st.write("Masukkan angka dipisahkan koma (contoh: 1,2,3)")

# 📥 Input 2 kolom
col1, col2 = st.columns(2)

with col1:
    a = st.text_input("Masukkan Set A")

with col2:
    b = st.text_input("Masukkan Set B")

# 🚀 Tombol proses
if st.button("🚀 Proses"):
    if a and b:
        try:
            setA = set(map(int, a.split(",")))
            setB = set(map(int, b.split(",")))

            st.success("✅ Berhasil diproses!")

            st.subheader("📊 Hasil Operasi")
            st.info(f"Union: {setA | setB}")
            st.info(f"Intersection: {setA & setB}")
            st.info(f"Difference (A-B): {setA - setB}")
            st.info(f"Difference (B-A): {setB - setA}")
            st.info(f"Symmetric Difference: {setA ^ setB}")

            st.subheader("📌 Info Tambahan")
            st.write(f"Jumlah elemen Set A: {len(setA)}")
            st.write(f"Jumlah elemen Set B: {len(setB)}")

        except:
            st.error("❌ Input harus angka dan dipisahkan koma!")
    else:
        st.warning("⚠️ Harap isi kedua set terlebih dahulu!")
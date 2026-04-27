import streamlit as st

st.set_page_config(page_title="Tugas Struktur Data", layout="centered")

st.title("Aplikasi Struktur Data")

menu = st.sidebar.selectbox("Pilih Menu", ["Operasi Set", "Word Count"])

if menu == "Operasi Set":
    st.header("🔢 Visualisasi Operasi Set")

    input_A = st.text_input("Masukkan elemen Set A (pisahkan dengan koma)")
    input_B = st.text_input("Masukkan elemen Set B (pisahkan dengan koma)")

    if input_A and input_B:
        set_A = set([x.strip() for x in input_A.split(",")])
        set_B = set([x.strip() for x in input_B.split(",")])

        st.write("Set A:", set_A)
        st.write("Set B:", set_B)

        st.subheader("Hasil Operasi")

        st.success(f"Union: {set_A | set_B}")
        st.info(f"Intersection: {set_A & set_B}")
        st.warning(f"Difference (A - B): {set_A - set_B}")
        st.warning(f"Difference (B - A): {set_B - set_A}")
        st.error(f"Symmetric Difference: {set_A ^ set_B}")


elif menu == "Word Count":
    st.header("📝 Word Count Komentar")

    text = st.text_area("Masukkan komentar:")

    if text:
        words = text.lower().split()

        word_count = {}

        for word in words:
            word = word.strip(".,!?")  # hapus tanda baca
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1

        st.subheader("Hasil Word Count")
        st.write(word_count)

        st.subheader("Grafik")
        st.bar_chart(word_count)
import streamlit as st

menu = st.sidebar.selectbox(
    "Pilih Menu",
    ["Operasi Set", "Word Count"]
)

if menu == "Operasi Set":
    st.header("Visualisasi Operasi Set")

    A_input = st.text_input("Masukkan Set A (pisahkan dengan koma)", "1,2,3,4")
    B_input = st.text_input("Masukkan Set B (pisahkan dengan koma)", "3,4,5,6")

    # Konversi ke set
    A = set(A_input.split(","))
    B = set(B_input.split(","))

    st.write("A =", A)
    st.write("B =", B)

    st.header("Hasil Operasi Set")
    st.write("Union =", A | B)
    st.write("Intersection =", A & B)
    st.write("Difference =", A - B)
    st.write("Symmetric Difference =", A ^ B)

elif menu == "Word Count":
    st.header("Word Count Komentar")

    text = st.text_area("Masukkan komentar sosial media")

    if st.button("Hitung Kata"):
        words = text.lower().split()

        word_count = {}

        for word in words:
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1

        st.subheader("Hasil (Dictionary)")
        st.write(word_count)

        st.subheader("Detail Frekuensi")

        for key in word_count:
            st.write(f"{key} : {word_count[key]}")
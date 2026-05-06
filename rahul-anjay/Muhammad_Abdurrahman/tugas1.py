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

    st.subheader("Pilih Operasi")

    col1, col2 = st.columns(2)

    with col1:
        show_union = st.checkbox("Union (A | B)")
        show_intersection = st.checkbox("Intersection (A & B)")

    with col2:
        show_difference = st.checkbox("Difference (A - B)")
        show_symdiff = st.checkbox("Symmetric Difference (A ^ B)")

    st.subheader("Hasil")

    if show_union:
        st.write("Union =", A | B)

    if show_intersection:
        st.write("Intersection =", A & B)

    if show_difference:
        st.write("Difference =", A - B)

    if show_symdiff:
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
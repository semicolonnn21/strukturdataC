import streamlit as st
from collections import Counter
import pandas as pd

st.title("Aplikasi Visualisasi Interaktif")

menu = st.sidebar.selectbox(
    "Pilih Fitur",
    ["Operasi Himpunan", "Word Count"]
)

if menu == "Operasi Himpunan":
    st.header("Visualisasi Operasi Himpunan")

    st.write("Masukkan elemen himpunan dipisahkan dengan koma (,)")

    set_a_input = st.text_input("Himpunan A", "1,2,3,4")
    set_b_input = st.text_input("Himpunan B", "3,4,5,6")

    try:
        set_a = set(map(int, set_a_input.split(",")))
        set_b = set(map(int, set_b_input.split(",")))

        union = set_a | set_b
        intersection = set_a & set_b
        difference_ab = set_a - set_b
        difference_ba = set_b - set_a
        symmetric_diff = set_a ^ set_b

        st.subheader("Hasil Operasi")
        st.write(f"A = {set_a}")
        st.write(f"B = {set_b}")

        st.write("Union (A ∪ B):", union)
        st.write("Intersection (A ∩ B):", intersection)
        st.write("Difference (A - B):", difference_ab)
        st.write("Difference (B - A):", difference_ba)
        st.write("Symmetric Difference (A △ B):", symmetric_diff)

    except:
        st.error("Pastikan input berupa angka yang dipisahkan koma!")

elif menu == "Word Count":
    st.header("Visualisasi Word Count Komentar Sosial Media")

    text = st.text_area(
        "Masukkan komentar:",
        "Saya suka belajar Python, Python itu mudah dan menyenangkan"
    )

    if text:
        words = text.lower().split()

        word_count = Counter(words)

        df = pd.DataFrame(word_count.items(), columns=["Kata", "Frekuensi"])
        df = df.sort_values(by="Frekuensi", ascending=False)

        st.subheader("Hasil Word Count")
        st.write(df)

        st.bar_chart(df.set_index("Kata"))
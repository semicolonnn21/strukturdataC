import streamlit as st
import pandas as pd

data = {
    "Ukuran Data": [100, 1000, 10000, 50000],
    "Insertion Sort": [0.000602, 0.069353, 5.833697, 140.480564],
    "Selection Sort": [0.000455, 0.106189, 5.807709, 145.746770],
    "Quick Sort": [0.000282, 0.003214, 0.063431, 0.377714]
}

df = pd.DataFrame(data)

st.title("Perbandingan Waktu Eksekusi Algoritma Sorting")

st.write("### Data Eksekusi")
st.dataframe(
    df.style.format({
        "Insertion Sort": "{:.6f}",
        "Selection Sort": "{:.6f}",
        "Quick Sort": "{:.6f}"
    })
)


st.write("### Grafik Line Chart")
st.line_chart(df.set_index("Ukuran Data"))
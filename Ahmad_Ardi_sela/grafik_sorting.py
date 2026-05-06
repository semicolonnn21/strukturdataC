import streamlit as st
import pandas as pd

st.title("Laporan Benchmarking Sorting")

# Menyiapkan data angka (gunakan tipe data float agar bisa dibaca oleh grafik)
data_grafik = {
    "Ukuran Data": [100, 1000, 10000, 50000],
    "Selection Sort": [0.00039, 0.03622, 1.54348, 38.53780],
    "Merge Sort": [0.00036, 0.00293, 0.03598, 0.11124],
    "Quick Sort": [0.00025, 0.00157, 0.01454, 0.10648]
}

# Membuat DataFrame
df_grafik = pd.DataFrame(data_grafik)

# Mengatur 'Ukuran Data' sebagai sumbu X (bawah)
df_grafik.set_index("Ukuran Data", inplace=True)

st.subheader("Visualisasi Waktu Eksekusi")
st.write("Grafik perbandingan kecepatan ketiga algoritma:")

# Menampilkan grafik garis
st.line_chart(df_grafik)
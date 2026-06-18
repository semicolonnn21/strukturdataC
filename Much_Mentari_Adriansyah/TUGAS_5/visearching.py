import streamlit as st
import time

# Pengaturan halaman
st.set_page_config(
    page_title="Visualisasi Algoritma Searching",
    page_icon="🔍",
    layout="wide"
)

# Fungsi menampilkan array
def tampilkan_array(data, indeks_aktif=-1, indeks_ketemu=-1, indeks_dicek=[]):
    hasil = ""
    for i, angka in enumerate(data):
        if i == indeks_ketemu:
            hasil += f"🟩[{angka}] "
        elif i == indeks_aktif:
            hasil += f"🟨[{angka}] "
        elif i in indeks_dicek:
            hasil += f"🟥[{angka}] "
        else:
            hasil += f"⬜[{angka}] "
    hasil += "\n"
    for i in range(len(data)):
        hasil += f" [{i}]  "
    return hasil

# Linear Search
def linear_search_visual(data, target, tampilan_array, tampilan_info, kecepatan):
    indeks_sudah_dicek = []
    for i in range(len(data)):
        tampilan_array.text(
            tampilkan_array(
                data,
                indeks_aktif=i,
                indeks_dicek=indeks_sudah_dicek
            )
        )
        tampilan_info.info(
            f"Langkah {i+1}: Memeriksa indeks [{i}] dengan nilai {data[i]}"
        )
        time.sleep(kecepatan)
        if data[i] == target:
            tampilan_array.text(
                tampilkan_array(
                    data,
                    indeks_ketemu=i,
                    indeks_dicek=indeks_sudah_dicek
                )
            )
            tampilan_info.success(
                f"Data ditemukan di indeks [{i}] setelah {i+1} langkah"
            )
            return i
        indeks_sudah_dicek.append(i)
    tampilan_info.error("Data tidak ditemukan")
    return -1

# Binary Search
def binary_search_visual(data, target, tampilan_array, tampilan_info, kecepatan):
    kiri = 0
    kanan = len(data) - 1
    langkah = 0
    indeks_sudah_dicek = []
    while kiri <= kanan:
        langkah += 1
        tengah = (kiri + kanan) // 2
        tampilan_array.text(
            tampilkan_array(
                data,
                indeks_aktif=tengah,
                indeks_dicek=indeks_sudah_dicek
            )
        )
        tampilan_info.info(
            f"Langkah {langkah}: kiri={kiri}, kanan={kanan}, tengah={tengah}, nilai={data[tengah]}"
        )
        time.sleep(kecepatan)
        if data[tengah] == target:
            tampilan_array.text(
                tampilkan_array(
                    data,
                    indeks_ketemu=tengah,
                    indeks_dicek=indeks_sudah_dicek
                )
            )
            tampilan_info.success(
                f"Data ditemukan di indeks [{tengah}]"
            )
            return tengah
        elif data[tengah] < target:
            indeks_sudah_dicek += list(range(kiri, tengah + 1))
            kiri = tengah + 1
        else:
            indeks_sudah_dicek += list(range(tengah, kanan + 1))
            kanan = tengah - 1
    tampilan_info.error("Data tidak ditemukan")
    return -1

# Judul aplikasi
st.title("🔍 Visualisasi Algoritma Searching")
st.write("Belajar Linear Search dan Binary Search langkah demi langkah")

# Sidebar
with st.sidebar:
    pilihan_algoritma = st.selectbox(
        "Pilih Algoritma",
        ["Linear Search", "Binary Search"]
    )

    input_data = st.text_input(
        "Masukkan angka (pisahkan dengan koma)",
        "5,12,3,8,21,1,17,9"
    )

    angka_dicari = st.number_input(
        "Angka yang dicari",
        value=17
    )

    kecepatan_animasi = st.slider(
        "Kecepatan animasi",
        0.1,
        2.0,
        0.5
    )
    tombol_mulai = st.button("Mulai Pencarian")

# Proses input
try:
    data_array = [
        int(x.strip())
        for x in input_data.split(",")
        if x.strip()
    ]
except:
    st.error("Input harus berupa angka yang dipisahkan koma")
    st.stop()

# Binary Search wajib urut
if pilihan_algoritma == "Binary Search":
    data_array = sorted(data_array)

# Tampilkan data awal
st.subheader("Array:")
st.text(tampilkan_array(data_array))

# Placeholder visualisasi
tampilan_array = st.empty()
tampilan_info = st.empty()

# Jalankan pencarian
if tombol_mulai:
    if pilihan_algoritma == "Linear Search":
        linear_search_visual(
            data_array,
            angka_dicari,
            tampilan_array,
            tampilan_info,
            kecepatan_animasi
        )
    else:
        binary_search_visual(
            data_array,
            angka_dicari,
            tampilan_array,
            tampilan_info,
            kecepatan_animasi
        )

# Kompleksitas
st.subheader("Kompleksitas Waktu:")

if pilihan_algoritma == "Linear Search":
    st.write("Best Case: O(1)")
    st.write("Worst Case: O(n)")
else:
    st.write("Best Case: O(1)")
    st.write("Worst Case: O(log n)")
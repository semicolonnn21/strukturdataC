import streamlit as st
import time

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Tugas 5 Struktur Data - Wafah Khonia",
    layout="centered"
)

# ==========================================
# ALGORITMA SEARCHING
# ==========================================

def sequential_search(data_list, target):
    st.subheader("Proses Sequential Search")

    posisi_ditemukan = -1

    for indeks in range(len(data_list)):

        if data_list[indeks] == target:
            st.write(
                f"Pengecekan indeks {indeks} "
                f"(nilai {data_list[indeks]}) → ✅ Ditemukan"
            )
            posisi_ditemukan = indeks
            break

        else:
            st.write(
                f"Pengecekan indeks {indeks} "
                f"(nilai {data_list[indeks]}) → ❌ Tidak Cocok"
            )

        time.sleep(0.3)

    return posisi_ditemukan


def binary_search(data_list, target):
    st.subheader("Proses Binary Search")

    kiri = 0
    kanan = len(data_list) - 1
    tahap = 1

    while kiri <= kanan:

        tengah = (kiri + kanan) // 2

        st.write(
            f"Tahap {tahap}: "
            f"Indeks tengah = {tengah} "
            f"(nilai {data_list[tengah]})"
        )

        if data_list[tengah] == target:
            return tengah

        elif data_list[tengah] < target:
            kiri = tengah + 1

        else:
            kanan = tengah - 1

        tahap += 1
        time.sleep(0.5)

    return -1


# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("📌 Menu")
pilihan_menu = st.sidebar.radio(
    "Pilih Materi",
    ["Searching", "Hashing Table"]
)

# ==========================================
# MENU SEARCHING
# ==========================================

if pilihan_menu == "Searching":

    st.title("🔍 Simulasi Algoritma Searching")

    input_data = st.text_input(
        "Masukkan data angka (pisahkan dengan koma):",
        "25, 30, 80, 10, 59"
    )

    input_target = st.text_input(
        "Masukkan angka yang dicari:",
        "10"
    )

    metode_pencarian = st.selectbox(
        "Pilih Metode Pencarian:",
        ["Sequential Search", "Binary Search"]
    )

    if st.button("Cari Data"):

        try:

            daftar_angka = [
                int(x.strip())
                for x in input_data.split(",")
            ]

            target = int(input_target)

            if metode_pencarian == "Sequential Search":

                hasil = sequential_search(
                    daftar_angka,
                    target
                )

            else:

                daftar_angka = sorted(daftar_angka)

                st.info(
                    f"Data setelah diurutkan: "
                    f"{daftar_angka}"
                )

                hasil = binary_search(
                    daftar_angka,
                    target
                )

            if hasil != -1:

                st.success(
                    f"Angka {target} ditemukan "
                    f"pada indeks {hasil}"
                )

            else:

                st.error(
                    f"Angka {target} tidak ditemukan"
                )

        except ValueError:

            st.warning(
                "Masukkan data berupa angka."
            )

# ==========================================
# MENU HASHING
# ==========================================

else:

    st.title("🗄️ Implementasi Hashing Table (Mod 7)")

    if "hash_table" not in st.session_state:
        st.session_state.hash_table = [
            [] for _ in range(7)
        ]

    angka_input = st.text_input(
        "Masukkan angka:",
        "14"
    )

    if st.button("Simpan Data"):

        try:

            nilai = int(angka_input)

            posisi = nilai % 7

            if (
                nilai
                not in st.session_state.hash_table[posisi]
            ):
                st.session_state.hash_table[posisi].append(
                    nilai
                )

        except ValueError:

            st.error(
                "Input harus berupa angka."
            )

    st.subheader("Isi Hash Table")

    for indeks in range(7):

        st.write(
            f"Index {indeks}: "
            f"{st.session_state.hash_table[indeks]}"
        )

# ==========================================
# IDENTITAS
# ==========================================

st.sidebar.divider()

st.sidebar.caption(
    "Wafah Khonia | NIM: 2530801081"
)

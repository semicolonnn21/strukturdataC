import streamlit as st
import time

st.title("Simulasi Lampu Lalu Lintas 🚦")

lampu = [
    ("Merah", 5),
    ("Hijau", 3),
    ("Kuning", 2)
]

placeholder = st.empty()

def tampil(warna_aktif, sisa):
    merah = "🔴" if warna_aktif == "Merah" else "⚫"
    kuning = "🟡" if warna_aktif == "Kuning" else "⚫"
    hijau = "🟢" if warna_aktif == "Hijau" else "⚫"

    placeholder.markdown(f"""
    ## {merah}
    ## {kuning}
    ## {hijau}

    ### Lampu: {warna_aktif}
    ### Sisa waktu: {sisa} detik
    """)

if st.button("Start"):
    for _ in range(3):
        for warna, durasi in lampu:
            for sisa in range(durasi, 0, -1):
                tampil(warna, sisa)
                time.sleep(1)

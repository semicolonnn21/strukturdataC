import streamlit as st

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Project Struktur Data🚀", layout="wide")

# 2. Judul Besar
st.title("📊 Tool Operasi Himpunan (*Set*)")
st.caption("***Untuk memenuhi Tugas Mata kuliah: Struktur Data😁***")

# 3. Garis Pembatas
st.divider()

# 4. Identitas (Bisa pakai kolom agar rapi)
col_nama, col_nim, col_mk, col_class = st.columns(4)
with col_nama:
    st.write("**Nama:** Abil Ghinaya Azka")
with col_nim:
    st.write("**NIM:** 2530801056")
with col_mk:
    st.write("**Mata kuliah:** Struktur Data")
with col_class:
    st.write("**Kelas:** II C")

st.divider()

# 5. Instruksi Singkat
st.info("Silakan masukkan elemen ***set*** pada kolom di bawah ini untuk melihat hasil operasinya.")

# 6. Menampilkan input teks
col1, col2 = st.columns(2)
with col1:
    st.subheader("⭐Himpunan A:") # subjudul
    st.warning("**Attention ⚠️:** Pisah antar elemen dengan koma!") # Peringatan
    input_a = st.text_input("***Masukkan elemen input***:", placeholder="Example: 1, 2, 3", key="setA")
    # Placeholder: fungsi yang berguna untuk memberi contoh
    # Sedangkan key: berguna untuk kata kunci 'Membedakan input A dengan input B'
    st.caption("💡 Tekan **Enter** untuk memproses..")

with col2:
    st.subheader("⭐Himpunan B:")
    st.warning("&nbsp;") # Mengkosongkan warning agar sejajar dengan 'Himpunan A'
    input_b = st.text_input("***Masukkan elemen input***:", placeholder="Example: 1, 2, 3", key="setB")

st.divider()

st.markdown("### 📊 Tabel Operasi Himpunan")

# 7. Membuat class Error
class HarusAdaKoma(Exception):
    pass

# 8. Cek apakah input sudah diisi
if input_a and input_b:
    try: # Coba dulu!
        # --- PROSES UNTUK HIMPUNAN A ---
        list_mentah_a = input_a.split(",") 
        list_bersih_a = [] 

        for elemen in list_mentah_a:
            bersih = elemen.strip() 
            if bersih == "": 
                raise HarusAdaKoma("Ada koma yang tidak ada isinya atau spasi berlebih!")
            list_bersih_a.append(bersih) 
        set_a = set(list_bersih_a)

        # --- PROSES UNTUK HIMPUNAN B ---
        list_mentah_b = input_b.split(",")
        list_bersih_b = []
        
        for elemen in list_mentah_b:
            bersih = elemen.strip() 
            if bersih == "": 
                raise HarusAdaKoma("Ada koma yang tidak ada isinya atau spasi berlebih!")
            list_bersih_b.append(bersih) 
        set_b = set(list_bersih_b)

        # --- TAMPILKAN HASILNYA (Hanya jika tidak ada error) ---
        # Keunggulan markdown dapat membuat tabel, meski kode nya tidak rapi (serasa pakai st.table)
        tabel_hasil = f"""
        | Operasi | Simbol | Hasil |
        | :--- | :---: | :--- |
        | **Union** | ∪ | `{set_a | set_b}` |
        | **Intersection** | ∩ | `{set_a & set_b}` |
        | **Difference (A-B)** | - | `{set_a - set_b}` |
        | **Symmetric Diff** | Δ | `{set_a ^ set_b}` |
        """
        st.toast("Meluncur!", icon="🚀") # Efek notif
        st.balloons() # Efek ballons mwehehehe

        st.markdown(tabel_hasil)

    except HarusAdaKoma as e:
        st.error(f"⚠️ Kesalahan Input: {e}")
        st.stop() # Menghentikan program karena ada Error

else: # Keadaan ketika masih kosong
    st.warning("Silakan isi kedua input dulu ya!")

# Tugas Struktur Data - Web Apps dengan Streamlit

Proyek ini berisi kumpulan aplikasi interaktif yang dibangun menggunakan Python dan framework Streamlit untuk memvisualisasikan berbagai konsep dasar dalam mata kuliah Struktur Data.

## 🚀 Fitur Utama

### 1. Traffic Light Visualization (Circular Linked List)
- **Konsep**: Mengimplementasikan Circular Linked List di mana setiap node (lampu) memiliki referensi ke node berikutnya, dan node terakhir kembali menunjuk ke node pertama.
- **Logika**: Simulasi pergantian lampu otomatis (Merah -> Hijau -> Kuning) dengan durasi waktu yang berbeda menggunakan pointer `next`.
- **File**: `traffic_light.py`

### 2. Queue Simulation (Circular Queue)
- **Konsep**: Menggunakan struktur data Antrean Melingkar (Circular Queue) berbasis array/list dengan ukuran tetap.
- **Logika**: Menggunakan dua pointer, `head` (depan) dan `tail` (belakang), serta operasi modulo `%` untuk menangani konsep *wrap-around* (kembali ke awal saat mencapai batas maksimal).
- **File**: `circular_queue.py`

### 3. Set Operations Visualizer
- **Fitur**: Visualisasi operasi himpunan (Union, Intersection, Difference, Symmetric Difference).
- **Logika**: Menggunakan tipe data `set` bawaan Python untuk pengolahan data unik.
- **File**: `tugas1_set.py`

### 4. Social Media Word Count
- **Fitur**: Menganalisis frekuensi kemunculan kata dalam teks/komentar.
- **Logika**: Implementasi Dictionary/Hash Map untuk memetakan kata ke jumlah kemunculannya.
- **File**: `word_count.py`

## 🛠️ Cara Menjalankan

Pastikan Anda memiliki Python terinstal, kemudian ikuti langkah berikut:

1. **Buat virtual environment:**
   ```bash
   python -m venv env
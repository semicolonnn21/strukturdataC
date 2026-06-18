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

### 5. Sorting Algorithm Benchmarking
- **Fitur**: Membandingkan kecepatan eksekusi antara **Bubble Sort**, **Merge Sort**, dan **Quick Sort**.
- **Konsep**: Analisis kompleksitas waktu ($O(n^2)$ vs $O(n \log n)$) menggunakan data acak dalam berbagai skala (10, 100, 1000 data).
- **Logika**: 
    - Melakukan *stress test* sebanyak 3 kali per ukuran data untuk menghitung nilai rata-rata.
    - Menggunakan fungsi `.copy()` untuk memastikan setiap algoritma mengurutkan kumpulan data yang identik.
    - Penyesuaian `sys.setrecursionlimit` untuk mendukung kedalaman rekursi pada algoritma Quick Sort.
- **File**: `sorting_benchmark.py`

### 6. Binary Search Tree (BST) Visualizer & Traversal
- **Fitur**: Visualisasi struktur pohon biner dan tiga metode penelusuran (traversal).
- **Konsep**: Implementasi rekursif di mana setiap node kiri memiliki nilai lebih kecil dari induk, dan node kanan memiliki nilai lebih besar.
- **Logika**:
    - **Insert Rekursif**: Mekanisme "oper-operan" data dari Root ke bawah hingga menemukan posisi `None` yang tepat sesuai aturan nilai.
    - **Traversal Framework**: Implementasi fungsi tunggal untuk mengeksekusi **Preorder**, **Inorder**, dan **Postorder** dengan memanipulasi posisi *pencatatan* (append) relatif terhadap pemanggilan rekursif.
    - **Validasi**: Analisis hasil traversal di mana mode *Inorder* digunakan untuk memverifikasi kebenaran struktur data (hasil harus terurut secara numerik).
- **Visualisasi**: Representasi hierarki pohon menggunakan blok kode (`st.code`) dengan font monospace untuk menjaga akurasi visual dahan dan node.
- **File**: `bst_app.py`

## 🛠️ Cara Menjalankan

1. **Persiapkan Lingkungan:**
   Pastikan Python sudah terinstal di sistem Anda.
   
2. **Install Dependensi:**
   Buka terminal **sel-sel ngawi** dan jalankan:
   ```bash
   pip install streamlit
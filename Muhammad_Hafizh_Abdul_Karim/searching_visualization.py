import streamlit as st
import time
import random

st.set_page_config(page_title="Searching Algorithm Visualization", layout="wide")
st.title("🔍 Visualisasi Algoritma Searching")

# --- Sidebar Settings ---
st.sidebar.header("⚙️ Pengaturan")
array_size = st.sidebar.slider("Ukuran Array", 5, 20, 10)
search_input = st.sidebar.text_input("Nilai yang Dicari", placeholder="Masukkan angka...")
search_target = int(search_input) if search_input.strip().isdigit() else None
speed = st.sidebar.slider("Kecepatan Animasi (detik)", 0.1, 1.0, 0.4)
algorithm = st.sidebar.selectbox("Pilih Algoritma", ["Linear Search", "Binary Search"])

# Generate array
if "array" not in st.session_state or st.sidebar.button("🔀 Generate Array Baru"):
    if algorithm == "Binary Search":
        st.session_state.array = sorted(random.sample(range(1, 101), array_size))
    else:
        st.session_state.array = random.sample(range(1, 101), array_size)

arr = st.session_state.array

st.subheader(f"Array: {arr}")

# --- Visualization Helper ---
def render_array(arr, highlights: dict):
    """highlights: {index: color_label}"""
    cols = st.columns(len(arr))
    color_map = {
        "current":  ("🟡", "#FFA500"),
        "found":    ("🟢", "#00C853"),
        "checked":  ("🔴", "#FF1744"),
        "boundary": ("🔵", "#2196F3"),
        "default":  ("⬜", "#ECEFF1"),
    }
    for i, col in enumerate(cols):
        label, bg = color_map.get(highlights.get(i, "default"), color_map["default"])
        col.markdown(
            f"<div style='text-align:center; background:{bg}; border-radius:8px;"
            f"padding:8px; font-weight:bold; color:white'>{arr[i]}</div>",
            unsafe_allow_html=True,
        )

# --- Algorithms ---
def linear_search(arr, target, speed):
    st.markdown("### 📌 Linear Search")
    placeholder = st.empty()
    log = st.empty()
    checked = []
    for i in range(len(arr)):
        checked.append(i)
        highlights = {j: "checked" for j in checked[:-1]}
        highlights[i] = "current"
        with placeholder.container():
            render_array(arr, highlights)
        log.info(f"Memeriksa indeks {i} → nilai {arr[i]}")
        time.sleep(speed)
        if arr[i] == target:
            highlights[i] = "found"
            with placeholder.container():
                render_array(arr, highlights)
            st.success(f"✅ Nilai {target} ditemukan di indeks {i}!")
            return i
    st.error(f"❌ Nilai {target} tidak ditemukan.")
    return -1

def binary_search(arr, target, speed):
    st.markdown("### 📌 Binary Search (Array harus terurut)")
    placeholder = st.empty()
    log = st.empty()
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        highlights = {}
        for i in range(len(arr)):
            if i < low or i > high:
                highlights[i] = "checked"
            elif i == low or i == high:
                highlights[i] = "boundary"
        highlights[mid] = "current"
        with placeholder.container():
            render_array(arr, highlights)
        log.info(f"low={low}, mid={mid}, high={high} → arr[mid]={arr[mid]}")
        time.sleep(speed)
        if arr[mid] == target:
            highlights[mid] = "found"
            with placeholder.container():
                render_array(arr, highlights)
            st.success(f"✅ Nilai {target} ditemukan di indeks {mid}!")
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    st.error(f"❌ Nilai {target} tidak ditemukan.")
    return -1

# --- Run ---
if st.button("▶️ Jalankan Pencarian"):
    if algorithm == "Linear Search":
        linear_search(arr, search_target, speed)
    else:
        if arr != sorted(arr):
            arr = sorted(arr)
            st.session_state.array = arr
            st.warning("Array diurutkan otomatis untuk Binary Search.")
        binary_search(arr, search_target, speed)

# Legend
st.markdown("---")
st.markdown("**Legenda:** 🟡 Sedang diperiksa &nbsp;|&nbsp; 🟢 Ditemukan &nbsp;|&nbsp; 🔴 Sudah diperiksa &nbsp;|&nbsp; 🔵 Batas (Binary)")
import streamlit as st
import time

st.set_page_config(page_title="Searching Visualizer", layout="centered")

st.title("Visualisasi Algoritma Searching")
st.write("STRUKTUR DATA - SALIM MUBAROK - UINSSC")

# ===== INPUT =====
input_data = st.text_input("Masukkan data (pisahkan koma)")
target = st.number_input("Masukkan angka yang dicari", step=1)

algo = st.selectbox("Pilih algoritma", ["Linear Search", "Binary Search"])

if input_data:
    data = list(map(int, input_data.split(",")))

# ===== STYLE KOTAK =====
def render_boxes(arr, active=None, found=None):
    cols = st.columns(len(arr))
    for i, val in enumerate(arr):
        color = "#2c3e50"

        if i == active:
            color = "#f39c12"  # orange
        if i == found:
            color = "#27ae60"  # green

        cols[i].markdown(
            f"""
            <div style="
                background:{color};
                padding:25px;
                border-radius:12px;
                text-align:center;
                font-size:22px;
                font-weight:bold;
                color:white;
                box-shadow: 0 4px 10px rgba(0,0,0,0.2);
            ">
                {val}
            </div>
            """,
            unsafe_allow_html=True
        )

# ===== INFO STEP =====
step_text = st.empty()

# ===== LINEAR SEARCH =====
def linear_search(arr, target):
    for i in range(len(arr)):
        step_text.info(f"🔎 Mengecek index {i} (nilai = {arr[i]})")
        render_boxes(arr, active=i)
        time.sleep(0.7)

        if arr[i] == target:
            step_text.success(f"✅ Ditemukan di index {i}")
            render_boxes(arr, found=i)
            return i

    step_text.error("❌ Data tidak ditemukan")
    return -1

# ===== BINARY SEARCH =====
def binary_search(arr, target):
    arr.sort()
    low, high = 0, len(arr) - 1

    while low <= high:
        mid = (low + high) // 2

        step_text.info(f"🔎 Mid index {mid} (nilai = {arr[mid]})")
        render_boxes(arr, active=mid)
        time.sleep(1)

        if arr[mid] == target:
            step_text.success(f"✅ Ditemukan di index {mid}")
            render_boxes(arr, found=mid)
            return mid
        elif arr[mid] < target:
            step_text.warning("➡️ Geser ke kanan")
            low = mid + 1
        else:
            step_text.warning("⬅️ Geser ke kiri")
            high = mid - 1

    step_text.error("❌ Data tidak ditemukan")
    return -1

# ===== BUTTON =====
if st.button("Mulai Visualisasi"):
    if algo == "Linear Search":
        linear_search(data, target)
    else:
        binary_search(data, target)
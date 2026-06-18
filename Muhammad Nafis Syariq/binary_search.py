import streamlit as st

st.set_page_config(page_title="Binary Search")
st.title("Binary Search")
st.divider()

raw = st.text_input("Masukkan data (pisah koma)", placeholder="contoh: 40, 10, 70, 25, 5, 90")
key = st.number_input("Key yang dicari", step=1, value=0)

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    return quick_sort([x for x in arr if x < pivot]) + \
           [x for x in arr if x == pivot] + \
           quick_sort([x for x in arr if x > pivot])

def binary_search_steps(arr, key):
    steps = []
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        steps.append({"low": low, "high": high, "mid": mid, "val": arr[mid]})
        if arr[mid] == key:
            return steps, mid
        elif arr[mid] < key:
            low = mid + 1
        else:
            high = mid - 1
    return steps, -1

if st.button("Cari", type="primary"):
    if not raw.strip():
        st.warning("Masukkan data terlebih dahulu.")
        st.stop()
    try:
        arr_input = [int(x.strip()) for x in raw.split(",")]
    except ValueError:
        st.error("Format salah, pastikan semua nilai adalah angka.")
        st.stop()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Data Awal")
        st.write(arr_input)
    with col2:
        st.subheader("Setelah Quick Sort")
        arr_sorted = quick_sort(arr_input)
        st.write(arr_sorted)

    st.divider()
    st.subheader("Proses Binary Search")

    steps, result = binary_search_steps(arr_sorted, int(key))

    for i, s in enumerate(steps):
        low, high, mid, val = s["low"], s["high"], s["mid"], s["val"]

        display = []
        for j, v in enumerate(arr_sorted):
            if j == mid and v == key:
                display.append(f"**:green[{v}]**")
            elif j == mid:
                display.append(f"**:orange[{v}]**")
            elif low <= j <= high:
                display.append(f":blue[{v}]")
            else:
                display.append(f":gray[{v}]")

        st.markdown(f"**Step {i+1}** &nbsp; `LOW={low}` &nbsp; `MID={mid}` &nbsp; `HIGH={high}`")
        st.write("  ".join(display))

        if val == key:
            st.success(f"✅ Key **{key}** ditemukan di index **{mid}**")
        elif val < key:
            st.caption(f"arr[{mid}] = {val} < {key} → cari ke kanan")
        else:
            st.caption(f"arr[{mid}] = {val} > {key} → cari ke kiri")

        st.markdown("---")

    if result == -1:
        st.error(f"Key **{key}** tidak ditemukan.")
    else:
        st.caption(f"Selesai dalam **{len(steps)} langkah**.")
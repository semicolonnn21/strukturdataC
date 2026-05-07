import streamlit as st

st.title("🔍 Visualisasi Binary Search")

# Input
data_input = st.text_input("Masukkan angka (pisahkan dengan koma)")
target = st.number_input("Masukkan angka yang dicari", value=0)

# Tombol
start = st.button("Mulai Binary Search")

# Semua proses hanya jalan kalau tombol ditekan
if start:
    try:
        arr = list(map(int, data_input.split(",")))
        arr.sort()

        st.write("Array setelah diurutkan:", arr)

        low = 0
        high = len(arr) - 1
        langkah = 1

        while low <= high:
            mid = (low + high) // 2

            st.write(f"### Langkah {langkah}")

            # Visualisasi
            visual = []
            for i in range(len(arr)):
                if i == mid:
                    visual.append(f"🔴{arr[i]}")  # mid
                elif i >= low and i <= high:
                    visual.append(f"🟢{arr[i]}")  # range aktif
                else:
                    visual.append(f"⚪{arr[i]}")  # di luar

            st.write(" | ".join(visual))
            st.write(f"low={low}, mid={mid}, high={high}")

            if arr[mid] == target:
                st.success(f"✅ Ditemukan di index {mid}")
                break
            elif arr[mid] < target:
                low = mid + 1
            else:
                high = mid - 1

            langkah += 1
        else:
            st.error("❌ Data tidak ditemukan")

    except:
        st.error("Masukkan angka dengan format benar (contoh: 1,2,3,4)")
import streamlit as st

st.set_page_config(page_title="Hash Table", page_icon="🗃️")

st.title("Implementasi Hash Table")
st.divider()

m_raw = st.text_input("Ukuran tabel (m)", placeholder="contoh: 7")
st.caption("Fungsi hash yang digunakan: `h(k) = k mod m`")

# Validasi m
m = None
if m_raw.strip():
    try:
        m = int(m_raw.strip())
        if m < 2:
            st.warning("Ukuran tabel minimal 2.")
            m = None
    except ValueError:
        st.error("Ukuran tabel harus berupa angka.")

# Data input hanya muncul kalau m sudah valid
if m:
    raw = st.text_input("Masukkan data (pisah koma)", placeholder=f"contoh: angka, maks {m} elemen")

    data = []
    if raw.strip():
        try:
            data = [int(x.strip()) for x in raw.split(",")]
            if len(data) > m:
                st.warning(f"Jumlah data ({len(data)}) melebihi ukuran tabel! ({m}). Kurangi data atau tambah ukuran tabel.")
                data = []
        except ValueError:
            st.error("Format salah, pastikan semua nilai adalah angka.")

    if data and st.button("Proses", type="primary"):
        # Linear probing
        table = [None] * m
        log   = []

        for k in data:
            orig = k % m
            pos  = orig
            probe_list = [pos]
            while table[pos] is not None:
                pos = (pos + 1) % m
                probe_list.append(pos)
            table[pos] = k
            log.append({"key": k, "orig": orig, "final": pos, "probes": probe_list})

        st.divider()
        st.subheader("Proses Penyisipan")
        for entry in log:
            k, orig, final, probes = entry["key"], entry["orig"], entry["final"], entry["probes"]
            st.markdown(f"**h({k})** = {k} mod {m} = **{orig}**")
            if len(probes) == 1:
                st.caption(f"Slot [{orig}] kosong → masuk di [{orig}]")
            else:
                probe_str = " → ".join(f"[{p}]" for p in probes)
                st.caption(f"⚠️ Collision, coba: {probe_str} → masuk di [{final}]")
            st.markdown("---")

        st.subheader("Hash Table")
        for i, val in enumerate(table):
            if val is not None:
                entry = next(e for e in log if e["final"] == i)
                if len(entry["probes"]) > 1:
                    st.markdown(f"`[{i}]` &nbsp; **{val}** &nbsp; ⚠️ *geser dari [{entry['orig']}]*")
                else:
                    st.markdown(f"`[{i}]` &nbsp; **{val}**")
            else:
                st.markdown(f"`[{i}]` &nbsp; :gray[—]")

        st.divider()
        total_col = sum(1 for e in log if len(e["probes"]) > 1)
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Data", len(data))
        col2.metric("Ukuran Tabel", m)
        col3.metric("Collision", total_col)
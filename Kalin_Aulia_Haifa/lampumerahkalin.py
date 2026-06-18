import streamlit as st
import time

class Node:
    def __init__(self, warna_teks, emoji, durasi_detik):
        self.warna_teks = warna_teks
        self.emoji = emoji          
        self.durasi = durasi_detik  
        self.next = None              

class CircularLinkedList:
    def __init__(self):
        self.head = None

    def tambah_lampu(self, warna_teks, emoji, durasi_detik):
        new_node = Node(warna_teks, emoji, durasi_detik)
        
        if not self.head:
    
            self.head = new_node
            new_node.next = self.head
        else:
           
            temp = self.head
            while temp.next != self.head:
                temp = temp.next
            temp.next = new_node
            new_node.next = self.head


tugu_lampu = CircularLinkedList()

tugu_lampu.tambah_lampu("Merah", "🔴 BERHENTI", 40)
tugu_lampu.tambah_lampu("Hijau", "🟢 JALAN", 20)
tugu_lampu.tambah_lampu("Kuning", "🟡 SIAP-SIAP", 5)

st.set_page_config(page_title="Lampu merah UINSSC")
st.title("🚦 Lampu merah UINSSC")
st.markdown("Awas jangan nyerobot, ada CCTV!")
st.divider()

lampu_visual = st.empty()
timer_visual = st.empty()

if tugu_lampu.head:
    node_saat_ini = tugu_lampu.head

    while True:
        lampu_visual.markdown(f"# {node_saat_ini.emoji}")
        
        for detik_tersisa in range(node_saat_ini.durasi, 0, -1):
            timer_visual.metric(
                label=f"Status: {node_saat_ini.warna_teks}", 
                value=f"{detik_tersisa} detik",
                help=f"Total durasi: {node_saat_ini.durasi} detik"
            )
            time.sleep(1) 

        node_saat_ini = node_saat_ini.next
else:
    st.error("Data lampu belum dimasukkan.")
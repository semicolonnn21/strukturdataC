import streamlit as st
import time

class Node:
    def __init__(self, warna, durasi):
        self.warna = warna
        self.durasi = durasi
        self.next = None

class CircularLinkedList:
    def __init__(self):
        self.head = None

    def tambah_lampu(self, warna, durasi):
        new_node = Node(warna, durasi)
        if not self.head:
            self.head = new_node
            new_node.next = self.head
        else:
            temp = self.head
            while temp.next != self.head:
                temp = temp.next
            temp.next = new_node
            new_node.next = self.head

st.set_page_config(page_title="Simulasi Lampu Merah", page_icon="🚦")
st.title("🚦 Visualisasi Lampu Merah")
st.write("Hafidzar Ashyawal Sinatryas - 2530801075")

cll = CircularLinkedList()
cll.tambah_lampu("Merah", 40)
cll.tambah_lampu("Kuning", 5)
cll.tambah_lampu("Hijau", 20)

wadah_visual = st.empty()
wadah_pesan = st.empty()
wadah_timer = st.empty()

if st.button("Mulai Simulasi"):
    curr = cll.head
    
    while True: 
        color_code = {"Merah": "#FF0000", "Hijau": "#00FF00", "Kuning": "#FFFF00"}
        
        wadah_visual.markdown(
            f"""
            <div style="display: flex; flex-direction: column; align-items: center; 
                        background-color: #333; padding: 20px; border-radius: 50px; 
                        width: 150px; margin: auto;">
                <div style="width: 80px; height: 80px; border-radius: 50%; background-color: {color_code['Merah'] if curr.warna == 'Merah' else '#555'}; margin-bottom: 10px;"></div>
                <div style="width: 80px; height: 80px; border-radius: 50%; background-color: {color_code['Kuning'] if curr.warna == 'Kuning' else '#555'}; margin-bottom: 10px;"></div>
                <div style="width: 80px; height: 80px; border-radius: 50%; background-color: {color_code['Hijau'] if curr.warna == 'Hijau' else '#555'};"></div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        if curr.warna == "Kuning":
            wadah_pesan.warning("⚠️ Tunggu sampai hijau...")
        elif curr.warna == "Merah":
            wadah_pesan.error("🛑 Berhenti! Lampu Merah")
        else:
            wadah_pesan.success("✅ Silahkan Jalan!")

        for i in range(curr.durasi, 0, -1):
            wadah_timer.metric(label=f"Status: {curr.warna}", value=f"{i} Detik")
            time.sleep(1)
            
        curr = curr.next
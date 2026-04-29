import uuid
import os

# =========================
# Utility
# =========================
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# =========================
# Data Storage
# =========================
users = {}
# Dokter + Poli + Spesialis + Jam Praktek
doctors = {
    "Dr. Budi": {"poli": "Umum", "spesialis": "Dokter Umum", "start": "08:00", "end": "15:00"},
    "Dr. Siti": {"poli": "Anak", "spesialis": "Spesialis Anak", "start": "09:00", "end": "14:00"},
    "Dr. Andi": {"poli": "Gigi", "spesialis": "Dokter Gigi", "start": "10:00", "end": "16:00"},
    "Dr. Rina": {"poli": "Kandungan", "spesialis": "Spesialis Obgyn", "start": "08:00", "end": "13:00"},
    "Dr. Dewa": {"poli": "Jantung", "spesialis": "Spesialis Kardiologi", "start": "07:00", "end": "12:00"}
}
appointments = {}

# =========================
# User Class
# =========================
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

# =========================
# Appointment Class
# =========================
class Appointment:
    def __init__(self, username, doctor, poli, spesialis, schedule):
        self.id = str(uuid.uuid4())[:8]
        self.username = username
        self.doctor = doctor
        self.poli = poli
        self.spesialis = spesialis
        self.schedule = schedule
        self.status = "Aktif"

# =========================
# Helper
# =========================
def validate_time(time_str):
    try:
        jam, menit = map(int, time_str.split(":"))
        return 0 <= jam < 24 and 0 <= menit < 60
    except:
        return False


def time_to_minutes(t):
    h, m = map(int, t.split(":"))
    return h * 60 + m


def is_within_schedule(input_time, start, end):
    t = time_to_minutes(input_time)
    return time_to_minutes(start) <= t <= time_to_minutes(end)

# =========================
# System Functions
# =========================
def register():
    clear_screen()
    username = input("Masukkan username: ")
    password = input("Masukkan password: ")

    if username in users:
        print("User sudah ada!")
    else:
        users[username] = User(username, password)
        print("Registrasi berhasil!")


def login():
    clear_screen()
    username = input("Username: ")
    password = input("Password: ")

    user = users.get(username)
    if user and user.password == password:
        print("Login berhasil!")
        return username
    else:
        print("Login gagal!")
        return None


def daftar_antrian(username):
    clear_screen()

    print("=== Pilih Dokter ===")
    doc_list = list(doctors.keys())
    for i, doc in enumerate(doc_list, 1):
        info = doctors[doc]
        print(f"{i}. {doc} | Poli: {info['poli']} | {info['spesialis']} | Jam: {info['start']} - {info['end']}")

    try:
        pilihan_doc = int(input("Pilih nomor dokter: ")) - 1
    except:
        print("Input tidak valid!")
        return

    if pilihan_doc not in range(len(doc_list)):
        print("Pilihan tidak valid!")
        return

    doctor = doc_list[pilihan_doc]
    data = doctors[doctor]

    schedule = input("Masukkan jam (contoh 13:30): ")

    if not validate_time(schedule):
        print("Format jam salah! Gunakan HH:MM")
        return

    if not is_within_schedule(schedule, data["start"], data["end"]):
        print(f"Jam di luar praktek dokter! ({data['start']} - {data['end']})")
        return

    appt = Appointment(username, doctor, data["poli"], data["spesialis"], schedule)
    appointments[appt.id] = appt

    print("\nBerhasil daftar!")
    print(f"ID: {appt.id}")
    print(f"Dokter: {doctor}")
    print(f"Poli: {data['poli']}")
    print(f"Jam: {schedule}")


def lihat_antrian(username):
    clear_screen()
    print("=== Antrian Anda ===")
    for appt in appointments.values():
        if appt.username == username:
            print(f"ID: {appt.id} | {appt.doctor} | {appt.poli} | {appt.schedule} | {appt.status}")

    input("\nTekan Enter untuk kembali...")


def cancel_antrian(username):
    clear_screen()
    lihat_antrian(username)
    appt_id = input("Masukkan ID yang ingin dibatalkan: ")

    appt = appointments.get(appt_id)
    if appt and appt.username == username:
        appt.status = "Dibatalkan"
        print("Antrian berhasil dibatalkan")
    else:
        print("Data tidak ditemukan!")


def reschedule_antrian(username):
    clear_screen()
    lihat_antrian(username)
    appt_id = input("Masukkan ID yang ingin diubah: ")

    appt = appointments.get(appt_id)
    if appt and appt.username == username:
        data = doctors[appt.doctor]
        new_schedule = input(f"Masukkan jam baru ({data['start']} - {data['end']}): ")

        if not validate_time(new_schedule):
            print("Format jam salah!")
            return

        if not is_within_schedule(new_schedule, data["start"], data["end"]):
            print("Di luar jam praktek!")
            return

        appt.schedule = new_schedule
        appt.status = "Reschedule"
        print("Berhasil reschedule!")
    else:
        print("Data tidak ditemukan!")

# =========================
# Main Program
# =========================
def main():
    while True:
        clear_screen()
        print("=== SISTEM ANTRIAN RS ===")
        print("1. Registrasi")
        print("2. Login")
        print("3. Keluar")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            register()
            input("Tekan Enter...")

        elif pilihan == "2":
            user = login()
            input("Tekan Enter...")
            if user:
                while True:
                    clear_screen()
                    print(f"=== MENU ({user}) ===")
                    print("1. Daftar Antrian")
                    print("2. Lihat Antrian")
                    print("3. Cancel")
                    print("4. Reschedule")
                    print("5. Logout")

                    menu = input("Pilih: ")

                    if menu == "1":
                        daftar_antrian(user)
                        input("\nTekan Enter...")
                    elif menu == "2":
                        lihat_antrian(user)
                    elif menu == "3":
                        cancel_antrian(user)
                        input("\nTekan Enter...")
                    elif menu == "4":
                        reschedule_antrian(user)
                        input("\nTekan Enter...")
                    elif menu == "5":
                        break
                    else:
                        print("Menu tidak valid!")
                        input("Tekan Enter...")

        elif pilihan == "3":
            print("Terima kasih!")
            break

        else:
            print("Pilihan tidak valid!")
            input("Tekan Enter...")


if __name__ == "__main__":
    main()
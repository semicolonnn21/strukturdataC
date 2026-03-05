jam = int(input("Waktu mulai (jam): "))
menit = int(input("Waktu mulai (menit): "))
durasi = int(input("Durasi Acara (menit): "))

menit = menit + durasi
jam = jam + menit // 60
menit = menit % 60

print("Acara selesai pukul", jam,":",menit)
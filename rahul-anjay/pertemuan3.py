list1 = [21,32,44,45]
list2 = [12,23,34,28]
list3 = [1,2,3,4,5]

print("list1:", list1)
print("list2:", list2)
print("list3:", list3)

listgabungan = [list1, list2, list3]
print("listgabungan :", listgabungan)

listtipedata = [24, "Cahyono", 3.12, False]
print("listtipedata :",listtipedata)
# print(listtipedata[:2])

# del listtipedata[1]
# listtipedata.pop(2)

print(listtipedata)

# warna = ['merah', 'hijau', 'kuning', 'biru', 'pink', 'ungu']

# warna.reverse()
# print("warna setelah di sort :", warna)
listtipedatacopy = listtipedata.copy()
print("list salinan", listtipedatacopy)
listtipedatacopy.append("Python")
print("list salinan tambahan", listtipedatacopy)
print("list asli",listtipedata)

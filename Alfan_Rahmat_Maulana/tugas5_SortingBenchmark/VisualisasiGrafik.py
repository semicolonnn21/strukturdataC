import matplotlib.pyplot as plt

# Data dari hasil benchmarking (contoh struktur)
sizes = [100, 1000, 10000, 50000]

selection = [0.00012, 0.0105, 1.2, None]   # None = tidak diuji
insertion = [0.00008, 0.0082, 0.9, None]
merge = [0.00005, 0.0012, 0.015, 0.09]

# =========================
# Plot Grafik
# =========================

def plot_data(x, y, label):
    x_plot = []
    y_plot = []

    for i in range(len(x)):
        if y[i] is not None:
            x_plot.append(x[i])
            y_plot.append(y[i])

    plt.plot(x_plot, y_plot, marker='o', label=label)

plot_data(sizes, selection, "Selection Sort")
plot_data(sizes, insertion, "Insertion Sort")
plot_data(sizes, merge, "Merge Sort")

plt.xlabel("Ukuran Data")
plt.ylabel("Waktu Eksekusi (detik)")
plt.title("Perbandingan Performa Sorting Algorithm")
plt.legend()
plt.grid()

plt.show()
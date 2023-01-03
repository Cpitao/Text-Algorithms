import matplotlib.pyplot as plt


def plot_compression():
    static_times = [0.02397, 0.09396, 0.67599, 10.01131]
    dynamic_times = [0.14059, 1.37615, 15.32152, 162.7036]
    xs = [1, 10, 100, 1024]

    _, ax = plt.subplots()
    ax.scatter(xs, static_times, label="Static algorithm")
    ax.scatter(xs, dynamic_times, label="Dynamic algorithm")

    ax.legend()
    ax.set_xscale('log')
    ax.set_xlabel("Text size in bytes")
    ax.set_ylabel("Time[s]")
    plt.show()


def plot_decompression():
    static_times = [0.006, 0.03403, 0.29696, 3.02817]
    dynamic_times = [0.009, 0.032, 0.29951, 3.1319]
    xs = [1, 10, 100, 1024]

    _, ax = plt.subplots()
    ax.scatter(xs, static_times, label="Static algorithm")
    ax.scatter(xs, dynamic_times, label="Dynamic algorithm")

    ax.legend()
    ax.set_xscale('log')
    plt.show()


def plot_compression_coefficients():
    static_compression = [38.09, 45.34, 46.04, 46.06]
    dynamic_compression = [37.89, 45.16, 45.95, 46.04]
    xs = [1, 10, 100, 1024]

    _, ax = plt.subplots()
    ax.scatter(xs, static_compression, label="Static algorithm")
    ax.scatter(xs, dynamic_compression, label="Dynamic algorithm")

    ax.legend()
    ax.set_xscale('log')
    plt.show()


plot_compression_coefficients()
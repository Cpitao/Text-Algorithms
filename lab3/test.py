import random
from numpy.random import choice
import os


# frequencies of letters in polish alphabet, can be used to generate random data with realistic frequencies
freq = [
        ['a', 0.0916],
        ['b', 0.0193],
        ['c', 0.0449],
        ['d', 0.0335],
        ['e', 0.0981],
        ['f', 0.0026],
        ['g', 0.0146],
        ['h', 0.0125],
        ['i', 0.0883],
        ['j', 0.0227],
        ['k', 0.0301],
        ['l', 0.0461],
        ['m', 0.0281],
        ['n', 0.0585],
        ['o', 0.0832],
        ['p', 0.0287],
        ['r', 0.0415],
        ['s', 0.0484],
        ['t', 0.0385],
        ['u', 0.0206],
        ['w', 0.0411],
        ['y', 0.0403],
        ['z', 0.0668]
    ]


def generate_file(size, frequency_based=False):
    with open(f"random_{size}k.txt", "w+", encoding='utf-8') as f:
        for i in range(size):
            if frequency_based:
                f.write(chr(choice([ord(f[0]) for f in freq], p=[f[1] for f in freq])))
            else:
                f.write(chr(random.randint(ord('a'), ord('z') + 1)))

    return f"random_{size}k.txt"


def test_compression(compression_f, decompression_f, frequency_based=False):
    sizes = [1024, 1024 * 10, 1024 * 100, 1024 * 1024]
    for size in sizes:
        print(f"Test for {size//1024}kB file")
        f = generate_file(size, frequency_based)
        compression_f(f)
        compressed_file = f[:-4] + ".cbin"
        print(f"Compression coefficient "
              f"{round((1 - os.path.getsize(compressed_file) / os.path.getsize(f)) * 100, 2)}%")
        decompression_f(f[:-4] + ".cbin")
        print("-------------------------------------------")

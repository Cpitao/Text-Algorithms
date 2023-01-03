from test import test_compression
from bitarray import bitarray
from bitarray.util import int2ba
from collections import deque
from nodes import *
from time import time


def huffman(letter_counts: dict, count_time=False):
    if count_time:
        print("Counting time taken by tree construction")
        start = time()

    nodes = []
    for a, weight in letter_counts.items():
        nodes.append(HuffmanLeaf(a, weight))

    internal_nodes = deque()
    leafs = sorted(nodes, key=lambda x: x.weight, reverse=True)

    x, y = leafs.pop(), leafs.pop()
    internal_nodes.append(HuffmanInternal(x, y, x.weight + y.weight))
    while len(leafs) + len(internal_nodes) > 1:
        elements = []
        for i in range(2):
            if len(internal_nodes) == 0 or (len(leafs) > 0 and leafs[-1].weight < internal_nodes[0].weight):
                elements.append(leafs.pop())
            else:
                elements.append(internal_nodes.popleft())

        internal_nodes.\
            append(HuffmanInternal(elements[0], elements[1], elements[0].weight + elements[1].weight))

    if count_time:
        print("Time taken:", round(time() - start, 7), "s")

    return internal_nodes[0]


def get_representations(root, representations=None):
    if representations is None:
        representations = {}

    # recursion replaced with stack
    stack = [(root, bitarray())]
    while len(stack) > 0:
        node, current = stack.pop()
        if isinstance(node, HuffmanInternal):
            stack.append((node.left, current + bitarray([0])))
            stack.append((node.right, current + bitarray([1])))
        else:
            representations[node.value] = current
    return representations


def huffman_compress(in_file, out_file=None, count_time=True):
    if count_time:
        start = time()
    with open(in_file, "r", encoding="utf-8") as f:
        text = f.read()

    letter_counts = get_frequencies(text)
    root = huffman(letter_counts)
    representations = get_representations(root)

    if out_file is None:
        out_file = in_file[:-4] + ".cbin"  # compressed binary
    binary_data = bitarray()
    for i in range(len(text)):
        print(f"Compressed {round(i / len(text) * 100, 2)}%", end="")
        c = text[i]
        binary_data += representations[c]
        print("\r", end="")
    print("Compressing done!")

    dict_binary = bitarray()
    codes = bitarray()
    for k, v in representations.items():
        dict_binary.frombytes((k + str(len(v)) + '$').encode('utf-8'))
        codes += v

    header = dict_binary + codes
    letters_size = len(dict_binary)
    all_data = int2ba(letters_size, length=32) + header + binary_data
    with open(out_file, "wb+") as f:
        all_data.tofile(f)

    if count_time:
        print(f"Compression time:{round(time() - start, 5)}s")


def huffman_decompress(in_file, out_file=None, count_time=True):
    if count_time:
        start = time()

    if out_file is None:
        out_file = in_file[:-5] + "_d.txt"

    with open(in_file, "rb") as f:
        binary = bitarray()
        binary.fromfile(f)

    letters_size = int.from_bytes(binary[:32], byteorder='big')
    letters = []
    code_lengths = []
    codes = []
    encoded_letters = binary[32:32+letters_size].tobytes().decode('utf-8').split(sep='$')
    for i in range(len(encoded_letters) - 1):
        if encoded_letters[i] == '':
            encoded_letters[i+1] = '$' + encoded_letters[i+1]
            continue

        letters.append(encoded_letters[i][0])
        code_lengths.append(int(encoded_letters[i][1:]))

    current = 32 + letters_size
    for length in code_lengths:
        codes.append(binary[current:current+length])
        current += length

    dictionary = dict(zip([str(code) for code in codes], letters))
    text = ""

    letter_start = current
    while current < len(binary):
        if str(binary[letter_start:current]) in dictionary:
            text += dictionary[str(binary[letter_start:current])]
            letter_start = current
        current += 1

    with open(out_file, "w+", encoding="utf-8") as f:
        f.write(text)

    if count_time:
        print(f"Decompression time: {round(time() - start, 5)}s")


def get_frequencies(text):
    letter_counts = {}
    for c in text:
        letter_counts[c] = letter_counts.get(c, 0) + 1

    return letter_counts


if __name__ == "__main__":
    test_compression(huffman_compress, huffman_decompress, frequency_based=True)

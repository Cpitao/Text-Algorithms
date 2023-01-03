import os
import random
from collections import defaultdict
from collections import deque

from bitarray import bitarray
from bitarray.util import int2ba
from test import test_compression
from time import time


class Node:

    nodes = []

    def __init__(self, value, weight=0, parent=None, left=None, right=None, index=None):
        self.value = value
        self.weight = weight
        self.left = left
        self.right = right
        self.parent = parent
        self.index = index

    def swap(self, i):
        if self.index == i:
            return
        self_parent, i_parent = self.parent, Node.nodes[i].parent

        self.parent, Node.nodes[i].parent= i_parent, self.parent

        if self.parent.left == Node.nodes[i]:
            self.parent.left = self
        else:
            self.parent.right = self
        if Node.nodes[i].parent.left == self:
            Node.nodes[i].parent.left = Node.nodes[i]
        else:
            Node.nodes[i].parent.right = Node.nodes[i]


def fix_indexing(root):
    Node.nodes = [root]
    q = deque()
    q.append(root)
    while q:
        current = q.popleft()
        if current.right is not None:
            Node.nodes.append(current.right)
            current.right.index = len(Node.nodes) - 1
            q.append(current.right)
        if current.left is not None:
            Node.nodes.append(current.left)
            q.append(current.left)
            current.left.index = len(Node.nodes) - 1


def dynamic_huffman(text, count_time=False):
    if count_time:
        print("Counting time taken by tree construction")
        start = time()

    Node.nodes = []
    nodes = {'NYT': Node('NYT', index=0)}
    root = nodes['NYT']

    for c in text:
        if c not in nodes:
            new_symbol = Node(c, weight=1, parent=nodes['NYT'])
            nodes[c] = new_symbol
            new_nyt = Node('NYT', parent=nodes['NYT'])
            nodes['NYT'].value = None
            nodes['NYT'].weight += 1

            nodes['NYT'].left = new_nyt
            nodes['NYT'].right = new_symbol
            nodes['NYT'] = new_nyt
            fix_indexing(root)
            node = new_symbol.parent.parent
        else:
            node = nodes[c]

        while node is not None:
            i = node.index
            while i >= 0 and node.weight >= Node.nodes[i].weight:
                i -= 1
            i += 1
            if Node.nodes[i] == node.parent:
                i += 1

            node.swap(i)
            fix_indexing(root)
            node.weight += 1
            node = node.parent

    if count_time:
        print("Time taken:", round(time() - start, 7), "s")

    return root


def get_representations(root, representations=None):
    if representations is None:
        representations = {}

    stack = [(root, bitarray())]
    while len(stack) > 0:
        node, current = stack.pop()
        if node.value is None:
            stack.append((node.left, current + bitarray([0])))
            stack.append((node.right, current + bitarray([1])))
        else:
            if node.value != 'NYT':
                representations[node.value] = current
    return representations


def dynamic_huffman_compress(in_file, out_file=None, count_time=True):
    if count_time:
        start = time()

    with open(in_file, "r", encoding="utf-8") as f:
        text = f.read()

    root = dynamic_huffman(text)
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
        print(f"Compression time: {round(time() - start, 5)}s")


def dynamic_huffman_decompress(in_file, out_file=None, count_time=True):
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


if __name__ == "__main__":
    test_compression(dynamic_huffman_compress, dynamic_huffman_decompress, frequency_based=True)

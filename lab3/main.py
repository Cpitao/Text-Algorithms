from static_huffman import huffman_compress, huffman_decompress
from dynamic_huffman import dynamic_huffman_compress, dynamic_huffman_decompress
from test import test_compression


if __name__ == "__main__":
    test_compression(huffman_compress, huffman_decompress, frequency_based=True)
    test_compression(dynamic_huffman_compress, dynamic_huffman_decompress, frequency_based=True)
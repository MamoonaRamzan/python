import struct
import random

def generate_sorted_binary_file(filename, num_integers):
    data = sorted(random.randint(0, 1_000_000) for _ in range(num_integers))
    with open(filename, "wb") as f:
        for num in data:
            f.write(struct.pack("i", num))

generate_sorted_binary_file("chunk1.bin", 1000000)
generate_sorted_binary_file("chunk2.bin", 1500000)
generate_sorted_binary_file("chunk3.bin", 1200000)

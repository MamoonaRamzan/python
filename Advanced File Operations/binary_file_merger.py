import heapq
import os
import struct
import time

BUFFER_SIZE = 100 * 1024 * 1024  # 100 MB
INT_SIZE = 4  # 4 bytes per integer

def read_chunk(file, buffer_size):
    data = file.read(buffer_size)
    return list(struct.unpack(f"{len(data)//INT_SIZE}i", data))

def binary_file_merger(input_files, output_file):
    start_time = time.time()
    print("Binary File Merger")
    print(f"Starting merge operation with {len(input_files)} files")

    # Open all input files
    file_pointers = [open(file, "rb") for file in input_files]
    file_buffers = [read_chunk(fp, BUFFER_SIZE) for fp in file_pointers]
    file_indices = [0] * len(input_files)

    # Priority queue: (value, file_index)
    heap = []
    for i, buffer in enumerate(file_buffers):
        if buffer:
            heapq.heappush(heap, (buffer[0], i))

    with open(output_file, "wb") as out:
        merged_count = 0
        while heap:
            value, i = heapq.heappop(heap)
            out.write(struct.pack("i", value))
            merged_count += 1
            file_indices[i] += 1

            # If that buffer is exhausted, read next chunk
            if file_indices[i] >= len(file_buffers[i]):
                file_buffers[i] = read_chunk(file_pointers[i], BUFFER_SIZE)
                file_indices[i] = 0

            if file_buffers[i]:
                heapq.heappush(heap, (file_buffers[i][file_indices[i]], i))

            # Progress every 10 million integers
            if merged_count % 10_000_000 == 0:
                print(f"Merged: {merged_count // 1_000_000}M integers...")

    for fp in file_pointers:
        fp.close()

    end_time = time.time()
    print(f"Merge completed successfully in {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    input_files = ["chunk1.bin", "chunk2.bin", "chunk3.bin"]
    output_file = "merged_data.bin"
    binary_file_merger(input_files, output_file)

import numpy as np


class ChunkFactory:
    def __init__(self):
        self.buffer = None
        self.buffer_offset = 0

        self.fetched_size = 0

    def fetch(self, size, complete=True):
        chunks = []
        needed_size = size

        try:
            while needed_size > 0:
                if self.buffer is None or (
                        len(self.buffer) - self.buffer_offset) == 0:
                    self.buffer = self.load()
                    self.buffer_offset = 0

                if self.buffer is None:
                    if complete:
                        raise BufferError("buffer underflow")
                    else:
                        break
                else:
                    copy_len = min(
                        len(self.buffer) - self.buffer_offset, needed_size)

                    chunks.append(
                        self.buffer[self.buffer_offset:self.buffer_offset +
                                    copy_len])

                    self.buffer_offset += copy_len
                    needed_size -= copy_len
        finally:
            self.fetched_size += size - needed_size

        return np.concatenate(chunks)


class VideoHeader:
    magic = np.frombuffer(b'STEGOSAURUS', dtype=np.uint8)

    def __init__(self):
        self.payload_name = ""
        self.payload_size = 0

        self.is_random_frame = False
        self.is_random_pixel = False

        self.is_two_bits = False

    def serialize(self):
        return np.concatenate([
            # Magic.
            self.magic,
            # Flags.
            np.packbits(
                np.asarray([
                    self.is_random_frame,
                    self.is_random_pixel,
                    self.is_two_bits,
                ], dtype=np.uint8)),
            # Payload size.
            np.frombuffer(
                self.payload_size.to_bytes(4, 'big'), dtype=np.uint8),
            # Null-terminated payload name.
            np.frombuffer(self.payload_name.encode('utf8'), dtype=np.uint8),
            np.asarray([0], dtype=np.uint8),
        ])

    @classmethod
    def from_factory(cls, data_factory):
        h = cls()

        # Magic.
        if not np.array_equal(data_factory.fetch(len(cls.magic)), cls.magic):
            raise ValueError("magic number is not matched")

        # Flags.
        h.is_random_frame, h.is_random_pixel, h.is_two_bits = np.unpackbits(
            data_factory.fetch(1)).astype(bool)[:3]

        # Payload size.
        h.payload_size = int.from_bytes(
            data_factory.fetch(4).tobytes(), byteorder='big')

        # Null-terminated payload name.
        previous_chunks = []
        h.fetched_size = data_factory.fetched_size

        while True:
            fetched_data = data_factory.fetch(64, complete=False)

            search_indices = np.flatnonzero(fetched_data == 0)
            if len(search_indices) > 0:
                null_index = search_indices[0]

                previous_chunks.append(fetched_data[:null_index])

                merged_chunk = np.concatenate(previous_chunks)
                h.fetched_size += len(merged_chunk) + 1

                h.payload_name = merged_chunk.tobytes().decode('utf8')
                break
            else:
                previous_chunks.append(fetched_data)

        return h

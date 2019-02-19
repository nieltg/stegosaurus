import numpy as np


class ChunkFactory:
    def __init__(self):
        self.buffer = None
        self.buffer_offset = 0

        self.fetched_len = 0

    def fetch(self, size, complete=True):
        buffer = self.buffer
        buffer_offset = self.buffer_offset

        chunks = []

        while size > 0:
            if buffer is None or (len(buffer) - buffer_offset) == 0:
                buffer = self.load()
                buffer_offset = 0

            if buffer is None:
                if complete:
                    raise BufferError("buffer underflow")
                else:
                    break
            else:
                copy_len = min(len(buffer) - buffer_offset, size)

                chunks.append(buffer[:copy_len])
                size -= copy_len

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
    def from_bytes(cls, data_factory):
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

        while True:
            fetched_data = data_factory.fetch(64, complete=False)

            search_indices = (fetched_data == 0).nonzero()
            if len(search_indices) > 0:
                null_index = search_indices[0]

                previous_chunks.append(fetched_data[:null_index])
                h.payload_name = str.encode(
                    np.concatenate(previous_chunks).tobytes(), 'utf8')
                break
            else:
                previous_chunks.append(fetched_data)

        return h

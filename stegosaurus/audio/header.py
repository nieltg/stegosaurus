import numpy as np


class AudioHeader:
    magic = np.frombuffer(b'STEGOSAURUS', dtype=np.uint8)

    def __init__(self):
        self.payload_name = ""
        self.payload_size = 0

        self.is_stereo = False
        self.is_random = False

        self.is_two_bits = False

    def serialize(self):
        return np.concatenate([
            # Magic
            self.magic,
            # Flags
            np.packbits(
                np.asarray([
                    self.is_stereo,
                    self.is_random,
                    self.is_two_bits,
                ], dtype=np.uint8)),
            # Payload size
            np.frombuffer(
                self.payload_size.to_bytes(4, 'big'), dtype=np.uint8),
            # Null-terminated payload name
            np.frombuffer(self.payload_name.encode('utf8'), dtype=np.uint8),
            np.asarray([0], dtype=np.uint8),
        ])

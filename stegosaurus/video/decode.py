import numpy as np

from .header import ChunkFactory, VideoHeader
from .encode import build_frame_list

from ..util import gen_lsb_mask


def extract_payload(data, n_bits=1):
    lsb_mask = np.asarray([gen_lsb_mask(n_bits)], dtype=np.uint8)
    data_lsb = data & lsb_mask

    lsb_bits = np.unpackbits(data_lsb.reshape(-1, 1), axis=-1)[:, 8 - n_bits:8]
    return np.packbits(lsb_bits)


class HeaderChunkFactory(ChunkFactory):
    chunk_size = 1024

    def __init__(self, data):
        super().__init__()
        self.data = data

    def load(self):
        chunk_size = self.chunk_size

        data, self.data = self.data[:chunk_size], self.data[chunk_size:]
        return extract_payload(data)


def extract_header(data):
    return VideoHeader.from_factory(HeaderChunkFactory(data))


def decode(data, passphrase=None):
    r = np.random.RandomState(passphrase)

    # Header.
    header = extract_header(data)

    # Payload.
    frames = build_frame_list(data, header.fetched_size * 8)
    n_bits = 2 if header.is_two_bits else 1

    # Frame indices.
    frame_indices = range(0, len(frames))

    if header.is_random_frame:
        frame_indices = np.asarray(frame_indices)
        r.shuffle(frame_indices)

    payload_chunks = []

    payload_chunks_len = 0

    for frame_id in frame_indices:
        frame = frames[frame_id]

        if payload_chunks_len < header.payload_size:
            if header.is_random_pixel:
                pass
                # TODO: Random pixel.
            else:
                payload_chunk = extract_payload(frame, n_bits)
                payload_chunks_len += len(payload_chunk)

                payload_chunks.append(payload_chunk)
        else:
            break

    return (header, np.concatenate(payload_chunks)[:header.payload_size])

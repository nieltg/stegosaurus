import numpy as np

from .header import VideoHeader
from .encode import build_frame_list

from ..util import HeaderChunkFactory, extract_payload, extract_payload_random, gen_lsb_mask
from ..vigenere import decrypt


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
                payload_chunk = extract_payload_random(frame, r, n_bits)
            else:
                payload_chunk = extract_payload(frame, n_bits)

            payload_chunks_len += len(payload_chunk)
            payload_chunks.append(payload_chunk)
        else:
            break

    # Concatenate and Decrypt payload
    payload_chunks = np.concatenate(payload_chunks)[:header.payload_size]
    payload_chunks = decrypt(payload_chunks, passphrase)

    return (header, payload_chunks)

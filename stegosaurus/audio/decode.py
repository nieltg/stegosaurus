import numpy as np

from .header import AudioHeader

from ..util import HeaderChunkFactory, extract_payload, extract_payload_random, gen_lsb_mask

from ..vigenere import decrypt


def extract_header(data):
    return AudioHeader.from_factory(HeaderChunkFactory(data))


def decode(data, passphrase=None):
    r = np.random.RandomState(passphrase)

    flat_data = data.reshape(-1)

    # Header.
    header = extract_header(flat_data)

    data_header_len = header.fetched_size * 8

    # Payload.
    payload_data = flat_data[data_header_len:]

    if header.is_random:
        payload = extract_payload_random(payload_data, r)
    else:
        payload = extract_payload(payload_data)

    cut_payload = payload[:header.payload_size]
    return (header, decrypt(cut_payload, passphrase))

import numpy as np

from .header import AudioHeader

from ..util import HeaderChunkFactory, extract_payload, gen_lsb_mask

from ..vigenere import decrypt


def extract_header(data):
    return AudioHeader.from_factory(HeaderChunkFactory(data))


def decode(data, passphrase=None):
    r = np.random.RandomState(passphrase)

    # Header.
    header = extract_header(data)

    # Payload.
    if header.is_random:
        # TODO
        pass
    else:
        payload = extract_payload(data)[header.fetched_size:header.fetched_size + header.payload_size]
        payload = decrypt(payload,passphrase)

    return (header, payload)

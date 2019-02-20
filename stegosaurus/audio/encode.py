import numpy as np

from ..util import apply_lsb, apply_lsb_random, prepare_payload

from ..vigenere import encrypt

from .header import AudioHeader

def apply_header(data, header):
    header_data_lsb = np.unpackbits(header.serialize())

    copy_len = len(header_data_lsb)

    apply_lsb(data.reshape(-1)[:copy_len], header_data_lsb)
    return copy_len


def encode(data, payload_data, header, passphrase=None):
    r = np.random.RandomState(passphrase)

    # Metadata.
    header.payload_size = len(payload_data)

    flat_data = data.reshape(-1)

    # Header.
    data_header_len = apply_header(flat_data, header)

    # Payload.
    payload_lsb = prepare_payload(encrypt(payload_data, passphrase))

    if header.is_random:
        apply_lsb_random(flat_data[data_header_len:], payload_lsb, r)
    else:
        apply_lsb(flat_data[data_header_len:data_header_len + len(payload_lsb)], payload_lsb)

    return True

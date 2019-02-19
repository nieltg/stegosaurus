import numpy as np

from ..util import apply_lsb


def apply_header(data, header):
    header_data_lsb = np.unpackbits(header.serialize())

    apply_lsb(data.reshape(-1), header_data_lsb)
    return len(header_data_lsb)


def encode(data, payload_data, header, passphrase=None):
    # Put header
    apply_bits_to_lsb(data.reshape(-1), np.unpackbits(header.serialize()))

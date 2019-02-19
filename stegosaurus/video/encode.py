import numpy as np

from ..util import gen_lsb_mask


def apply_lsb(data, data_lsb, n_bits=1):
    lsb_mask = gen_lsb_mask(n_bits)

    for i in range(0, len(data_lsb)):
        data[i] = (data[i] & ~lsb_mask) | data_lsb[i]


def apply_header(data, header):
    header_data_lsb = np.unpackbits(header.serialize())

    apply_lsb(data.reshape(-1), header_data_lsb)
    return len(header_data_lsb)


def encode(data, payload_data, header, passphrase=None):
    # Put header
    apply_bits_to_lsb(data.reshape(-1), np.unpackbits(header.serialize()))
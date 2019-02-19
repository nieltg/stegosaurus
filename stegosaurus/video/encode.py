import numpy as np

from ..util import gen_lsb_mask


def apply_bits_to_lsb(data, lsb_data, n_bits=1):
    lsb_mask = gen_lsb_mask(n_bits)

    for i in range(0, len(lsb_data)):
        data[i] = (data[i] & ~lsb_mask) | lsb_data[i]


def encode(data, payload_data, header, passphrase=None):
    # Put header
    apply_bits_to_lsb(data.reshape(-1), np.unpackbits(header.serialize()))

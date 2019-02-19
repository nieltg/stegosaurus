import numpy as np


def gen_lsb_mask(n_bits=1):
    mask = 0
    for i in range(0, n_bits):
        mask = mask | (1 << i)
    return mask


def apply_lsb(data, data_lsb, n_bits=1):
    lsb_mask = np.asarray([gen_lsb_mask(n_bits)], dtype=np.uint8)

    data &= lsb_mask
    data |= data_lsb

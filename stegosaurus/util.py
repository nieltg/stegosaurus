from numpy.random import RandomState


def gen_lsb_mask(n_bits=1):
    mask = 0
    for i in range(0, n_bits):
        mask = mask | (1 << i)
    return mask

def random_range(start, stop):
    np.Rando
    range(start, stop)

def gen_lsb_mask(n_bits=1):
    mask = 0
    for i in range(0, n_bits):
        mask = mask | (1 << i)
    return mask

def apply_lsb(data, data_lsb, n_bits=1):
    lsb_mask = gen_lsb_mask(n_bits)

    for i in range(0, len(data_lsb)):
        data[i] = (data[i] & ~lsb_mask) | data_lsb[i]

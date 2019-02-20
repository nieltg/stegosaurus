import numpy as np


def gen_lsb_mask(n_bits=1):
    mask = 0
    for i in range(0, n_bits):
        mask = mask | (1 << i)
    return mask


def prepare_payload(payload_data, n_bits=1):
    payload_bits = np.unpackbits(payload_data).reshape(-1, n_bits)

    payload_msbs = np.packbits(payload_bits, axis=-1).reshape(-1)
    return np.right_shift(payload_msbs, 8 - n_bits)


def apply_lsb(data, data_lsb, n_bits=1):
    lsb_mask = np.asarray([gen_lsb_mask(n_bits)], dtype=np.uint8)

    data &= ~lsb_mask
    data |= data_lsb


def apply_lsb_random(data, data_lsb, r, n_bits=1):
    indices = np.arange(len(data))
    r.shuffle(indices)
    indices = indices[:len(data_lsb)]

    lsb_mask = np.asarray([gen_lsb_mask(n_bits)], dtype=np.uint8)

    data.put(indices, (data[indices] & lsb_mask) | data_lsb)


def psnr_video(data_1, data_2):
    flat_size = np.prod(data_1.shape[1:])

    data_1_reshaped = data_1.reshape(-1, flat_size)
    data_2_reshaped = data_2.reshape(-1, flat_size)

    abs_sq = np.subtract(data_1_reshaped, data_2_reshaped, dtype=np.float64)**2

    rms = np.sqrt(np.sum(abs_sq, axis=1) / flat_size, dtype=np.float64)
    rms = rms[rms > 0]
    psnr = np.sum(20 * np.log10(256 / rms)) / len(rms)

    return psnr


def psnr_audio(data_1, data_2):
    flat_size = np.prod(data_1.shape[1:])
    
    data_1_reshaped = data_1.reshape(-1, flat_size)
    data_2_reshaped = data_2.reshape(-1, flat_size)
    
    mse = np.sum(np.subtract(data_1_reshaped,data_2_reshaped,dtype=np.int16)**2)
    if(mse == 0):
        return inf
    max_value = 0xffff
    psnr = 10 * np.log10((max_value**2) / mse)
    return psnr

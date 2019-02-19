import numpy as np


def shape(data, key_length):
    n_padding = len(data) % key_length
    padded_data = np.concatenate([data, np.zeros(n_padding, dtype=np.uint8)])
    return padded_data.reshape(-1, key_length)


def unshape(data, real_data_length):
    return data.reshape(-1)[:real_data_length]


def encrypt(data, key):
    cipher_data = shape(data, len(key)) + key
    return unshape(cipher_data, len(data))


def decrypt(data, key):
    plain_data = shape(data, len(key)) - key
    return unshape(plain_data, len(data))

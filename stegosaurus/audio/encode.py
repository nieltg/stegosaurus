import numpy as np

from ..util import apply_lsb

from ..vigenere import encrypt

from .header import AudioHeader

def apply_header(data, header):
    header_data_lsb = np.unpackbits(header.serialize())
    
    copy_len = len(header_data_lsb)
    
    apply_lsb(data.reshape(-1)[:copy_len], header_data_lsb)
    return copy_len

def encode(data, payload_data, header, passphrase=None):
    # Put header
    data_header_len = apply_header(data, header)
    
    # Encrypt payload
    if(header.is_random):
        # Random bits here
        return false;
    else:
        payload_data = encrypt(payload_data, passphrase)
    
    # Put encrypted payload
    apply_lsb(data[data_header_len:data_header_len+len(payload_data)],payload_data, 1)
    
def stereo_to_mono(data):
    data = np.repeat(data,2)
    return data
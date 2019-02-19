import numpy as np

from .header import VideoHeader

from ..util import apply_lsb, apply_lsb_random


def apply_header(data, header):
    header_data_lsb = np.unpackbits(header.serialize())

    copy_len = len(header_data_lsb)

    apply_lsb(data.reshape(-1)[:copy_len], header_data_lsb)
    return copy_len


def build_frame_list(data, data_header_len):
    frames = []

    flat_data_element_size = np.prod(data.shape[1:])
    flat_data = data.reshape(-1, flat_data_element_size)

    # 1st frame
    first_frame_offset = data_header_len // flat_data_element_size
    first_offset = data_header_len % flat_data_element_size

    frames.append(flat_data[first_frame_offset][first_offset:])

    # Other frames
    for frame in flat_data[first_frame_offset + 1:]:
        frames.append(frame)

    return frames


def prepare_payload(payload_data, n_bits=1):
    payload_bits = np.unpackbits(payload_data).reshape(-1, n_bits)

    payload_msbs = np.packbits(payload_bits, axis=-1).reshape(-1)
    return np.right_shift(payload_msbs, 8 - n_bits)


def encode(data, payload_data, header: VideoHeader, passphrase):
    r = np.random.RandomState(passphrase)

    # Header.
    data_header_len = apply_header(data, header)

    # Payload.
    frames = build_frame_list(data, data_header_len)

    n_bits = 2 if header.is_two_bits else 1
    payload_lsb = prepare_payload(payload_data, n_bits)

    # Frame indices.
    frame_indices = range(0, len(frames))

    if header.is_random_frame:
        frame_indices = np.asarray(frame_indices)
        r.shuffle(frame_indices)

    payload_lsb_index = 0

    for frame_id in frame_indices:
        frame = frames[frame_id]

        if payload_lsb_index < len(payload_lsb):
            copy_len = min(len(frame), len(payload_lsb) - payload_lsb_index)

            frame_payload_lsb = payload_lsb[payload_lsb_index:
                                            payload_lsb_index + copy_len]

            if header.is_random_pixel:
                apply_lsb_random(frame, frame_payload_lsb, r, n_bits)
            else:
                apply_lsb(frame[:copy_len], frame_payload_lsb, n_bits)

            payload_lsb_index += copy_len
        else:
            return True

    return False

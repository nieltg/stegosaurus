from stegosaurus.video.encode import encode as encode_video
from stegosaurus.video.decode import decode as decode_video
from stegosaurus.video.header import VideoHeader
from stegosaurus.audio.encode import encode as encode_audio
from stegosaurus.audio.decode import decode as decode_audio
from stegosaurus.audio.header import AudioHeader
from sksound.sounds import Sound
import numpy as np
import skvideo.io
import skvideo.datasets

def create_header(type_data, data, payload_data):
    if type_data == 'video':
        h = VideoHeader()
        h.payload_name = data['payload_path'].split('/')[-1]
        h.payload_size = len(payload_data)
        h.is_random_pixel = data['pixel_mode'] == 'acak'
        h.is_random_frame = data['frame_mode'] == 'acak'
        return h
    elif type_data == 'audio':
        h = AudioHeader()
        h.payload_name = data['payload_path'].split('/')[-1]
        h.is_random_frame = data['mode'] == 'acak'
        return h

def load_video(filename):
    return skvideo.io.vread(filename, verbosity=1)

def load_payload(filename):
    return np.fromfile(filename, dtype=np.uint8)

def encode(type_data, data):
    if type_data=='video':
        print('LOAD VIDEO')
        video_data = load_video(data['filename'])
        print('LOAD PAYLOAD')
        payload_data = load_payload(data['payload_path'])
        header = create_header('video', data, payload_data)
        passphrase = np.frombuffer(data['key'].encode(), dtype=np.uint8)
        encode_video(video_data, payload_data, header, passphrase)
        skvideo.io.vwrite(data['save_path'], video_data, outputdict={
                          "-vcodec": "png"}, verbosity=1)
        print('DONE')
    elif type_data=='audio':
        print('LOAD AUDIO')
        audio = Sound(data['filename'])
        audio.summary()
        audio_data = np.copy(audio.data)
        print('LOAD PLAYLOAD')
        payload_data = load_payload(data['payload_path'])
        header = create_header('audio', data, payload_data)
        passphrase = np.frombuffer(data['key'].encode(), dtype=np.uint8)
        encode_audio(audio_data, payload_data, header, passphrase)
        stego_audio = Sound(inData=audio_data, inRate=audio.rate)
        stego_audio.write_wav(data['save_path'])
        print('DONE')

def decode(type_data, data):
    if type_data == 'video':
        print('LOAD VIDEO')
        video_data = load_video(data['filename'])
        passphrase = np.frombuffer(data['key'].encode(), dtype=np.uint8)
        header, payload = decode_video(video_data, passphrase)
        print('DONE')
        return header, payload
    elif type_data == 'audio':
        audio = Sound(data['filename'])
        audio.summary()
        audio_data = np.copy(audio.data)
        passphrase = np.frombuffer(data['key'].encode(), dtype=np.uint8)
        header, payload = decode_audio(audio_data, passphrase)
        print('DONE')
        return header, payload

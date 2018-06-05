import numpy as np
import imageio
import scipy.io.wavfile as wav
import sys

def normalize_between(data, min_t, max_t):
    data = np.copy(data)
    data = (data - np.min(data)) / (np.max(data) - np.min(data))
    data = data * (max_t - min_t) + min_t
    
    return data

def int_to_bin(integer, size):
    return (("{0:0" + str(size) + "b}").format(integer))

def bin_to_int(binary):
    return (int(binary, 2))

def split_bin(binary):
    return [binary[i : i + 2] for i in np.arange(0, len(binary), 2)]

def hide_int(integer, img, positions):
    integer_bits = split_bin(int_to_bin(integer, len(positions) * 2))
    
    for i, mask in enumerate(integer_bits):
        channel = positions[i] // (img.shape[0] * img.shape[1])
        row = (positions[i] % (img.shape[0] * img.shape[1])) // img.shape[1]
        column = (positions[i] % (img.shape[0] * img.shape[1])) % img.shape[1]

        img[row, column, channel] = bin_to_int(int_to_bin(img[row, column, channel], 8)[:-2] + mask)      

    return

def get_int(img, positions):
    binary = ""
    for pos in positions:
        channel = pos // (img.shape[0] * img.shape[1])
        row = (pos % (img.shape[0] * img.shape[1])) // img.shape[1]
        column = (pos % (img.shape[0] * img.shape[1])) % img.shape[1]

        binary += int_to_bin(img[row, column, channel], 8)[-2:]
    
    return bin_to_int(binary)


def encode():
    # Reading and setting the seed
    seed = sys.argv[2].rstrip()
    np.random.seed(int.from_bytes(seed.encode(), "little") % (2**32 - 1))

    # Reading the wav file and calculating the space required for hiding
    wav_filename = sys.argv[3].rstrip()
    wav_rate, wav_data = wav.read(wav_filename)

    if (type(wav_data[0]) is np.ndarray):
        wav_data = (wav_data[:, 0] + wav_data[:, 1]) // 2
    wav_data = normalize_between(wav_data, 0, 255).astype(np.uint8)

    required_space = 32*2 + len(wav_data) * 8

    # Reading the image file and calculating the available space for hiding
    img_filename = sys.argv[4].rstrip()
    img = imageio.imread(img_filename)
    available_space = (img.shape[0] * img.shape[1] * img.shape[2] * 8) // 4

    if (available_space < required_space):
        print("The image provided is not big enough to store the sound file")
        print("It needs, at least, an image of " + str(required_space * 4) + " bits")
        sys.exit(-1)

    # Generating the positions using the seed
    random_positions = np.arange(img.shape[0] * img.shape[1] * img.shape[2])
    np.random.shuffle(random_positions)

    # Hiding the wav bit rate
    hide_int(wav_rate, img, random_positions[:16])

    # Hiding the number of samples
    hide_int(len(wav_data), img, random_positions[16 : 32])

    # Hiding the samples
    pos = 32
    for sample in wav_data:
        hide_int(sample, img, random_positions[pos : pos + 4])
        pos += 4

    imageio.imwrite("out.png", img)

    return

def decode():
    # Reading and setting the seed
    seed = sys.argv[2].rstrip()
    np.random.seed(int.from_bytes(seed.encode(), "little") % (2**32 - 1))

    # Reading the image file
    img_filename = sys.argv[3].rstrip()
    img = imageio.imread(img_filename)

    # Recovering the positions used for hiding using the seed
    positions = np.arange(img.shape[0] * img.shape[1] * img.shape[2])
    np.random.shuffle(positions)

    # Recovering the bit rate
    wav_rate = get_int(img, positions[:16])

    # Recovering the total number of samples
    total_samples = get_int(img, positions[16 : 32])

    # Recovering the samples
    wav_data = np.zeros(total_samples)
    pos = 32
    for i in np.arange(total_samples):
        sample = get_int(img, positions[pos : pos + 4])
        wav_data[i] = np.uint8(sample)
        pos += 4

    wav.write("out.wav", wav_rate, wav_data)

    return



encode_flag = "-e"
decode_flag = "-d"

op_flag = sys.argv[1].rstrip()
if (op_flag == encode_flag):
    encode()
elif (op_flag == decode_flag):
    decode()
import numpy as np
import imageio
import soundfile as sf
import sys

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

    # Reading the wav file
    wav_filename = sys.argv[3].rstrip()
    wav_data, wav_rate = sf.read(wav_filename, dtype='int16')

    # If stereo, convert to mono
    if (type(wav_data[0]) is np.ndarray):
        wav_data = (wav_data[:, 0] + wav_data[:, 1]) // 2
    
    # Convert samples from int16 to uint16
    wav_data = (wav_data.astype(int) + (2**15 - 1)).astype(np.uint16)

    # Calculating required space for hiding
    required_space = 32*2 + len(wav_data) * 16

    # Reading the image file and calculating the available space for hiding
    img_filename = sys.argv[4].rstrip()
    img = imageio.imread(img_filename).astype(np.uint8)
    available_space = (img.shape[0] * img.shape[1] * img.shape[2] * 8) // 4

    if (available_space < required_space):
        print("The image provided is not big enough to store the sound file")
        sys.exit(-1)

    # Reading the name of the output destination
    img_output_dest = sys.argv[5].rstrip()

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
        hide_int(sample, img, random_positions[pos : pos + 8])
        pos += 8

    imageio.imwrite(img_output_dest, img)

    return

def decode():
    # Reading and setting the seed
    seed = sys.argv[2].rstrip()
    np.random.seed(int.from_bytes(seed.encode(), "little") % (2**32 - 1))

    # Reading the image file
    img_filename = sys.argv[3].rstrip()
    img = imageio.imread(img_filename)

    # Reading the name of the output destination
    wav_output_dest = sys.argv[4].rstrip()

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
        sample = get_int(img, positions[pos : pos + 8])
        wav_data[i] = np.uint16(sample)
        pos += 8

    # Converting samples to int16
    wav_data = (wav_data.astype(int) - (2**15 - 1)).astype(np.int16)

    sf.write(wav_output_dest, wav_data, wav_rate, 'PCM_16')

    return

encode_flag = "-e"
decode_flag = "-d"

op_flag = sys.argv[1].rstrip()
if (op_flag == encode_flag):
    encode()
elif (op_flag == decode_flag):
    decode()
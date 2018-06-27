import numpy as np
import imageio
import soundfile as sf
import sys

def backspace(n):
    for i in np.arange(n):
        print('\r', end='')

    return

def rmse_error(image1, image2):
    squared_diff = np.power(image1 - image2, 2)
    error = np.sqrt(squared_diff.mean())

    return error

def int_to_bin(integer, size):
    return (("{0:0" + str(size) + "b}").format(integer))

def bin_to_int(binary):
    return (int(binary, 2))

def split_bin(binary, size):
    return [binary[i : i + size] for i in np.arange(0, len(binary), size)]

def hide_int(integer, int_size, img, positions):
    bits_n = int_size // len(positions)
    integer_bits = split_bin(int_to_bin(integer, int_size), bits_n)
    
    for i, mask in enumerate(integer_bits):
        channel = positions[i] // (img.shape[0] * img.shape[1])
        row = (positions[i] % (img.shape[0] * img.shape[1])) // img.shape[1]
        column = (positions[i] % (img.shape[0] * img.shape[1])) % img.shape[1]

        img[row, column, channel] = bin_to_int(int_to_bin(img[row, column, channel], 8)[:-bits_n] + mask)      

    return

def get_int(int_size, img, positions):
    bits_n = int_size // len(positions)
    binary = ""
    for pos in positions:
        channel = pos // (img.shape[0] * img.shape[1])
        row = (pos % (img.shape[0] * img.shape[1])) // img.shape[1]
        column = (pos % (img.shape[0] * img.shape[1])) % img.shape[1]

        binary += int_to_bin(img[row, column, channel], 8)[-bits_n:]
    
    return bin_to_int(binary)


def encode(seed, wav_filename, img_filename, bits_n, img_output_dest):
    # Setting the seed
    np.random.seed(int.from_bytes(seed.encode(), "little") % (2**32 - 1))

    # Reading the wav file
    wav_data, wav_rate = sf.read(wav_filename, dtype='int16')

    # If stereo, convert to mono
    if (type(wav_data[0]) is np.ndarray):
        wav_data = (wav_data[:, 0] + wav_data[:, 1]) // 2
    
    # Convert samples from int16 to uint16
    wav_data = (wav_data.astype(int) + (2**15 - 1)).astype(np.uint16)

    # Calculating required space for hiding
    required_space = 32*2 + len(wav_data) * 16

    # Reading the image file and calculating the available space for hiding
    img = imageio.imread(img_filename).astype(np.uint8)

    available_space = (img.shape[0] * img.shape[1] * img.shape[2] * 8) // (8 // bits_n)

    if (available_space < required_space):
        print("The image provided is not big enough to store the sound file using the " + str(bits_n)\
        + " least significant bit(s)")
        sys.exit(-1)   

    # Generating the positions using the seed
    random_positions = np.arange(img.shape[0] * img.shape[1] * img.shape[2])
    np.random.shuffle(random_positions)

    # Hiding the wav bit rate
    hide_int(wav_rate, 32, img, random_positions[:(32 // bits_n)])

    # Hiding the number of samples
    hide_int(len(wav_data), 32, img, random_positions[(32 // bits_n) : 2 * (32 // bits_n)])

    # Hiding the samples
    pr_str = "Progress: 0%"
    print(pr_str, end='')
    backspace(len(pr_str))

    pos = 2 * (32 // bits_n)
    k = 0
    for sample in wav_data:
        hide_int(sample, 16, img, random_positions[pos : pos + (16 // bits_n)])
        pos += (16 // bits_n)

        k += 1
        progress = k / len(wav_data)
        pr_str = "Progress: " + "{:.2f}".format(progress * 100) + "%"
        print(pr_str, end='')

        if (progress < 1):
            backspace(len(pr_str))
        else:
            print("")
        

    imageio.imwrite(img_output_dest, img)
    print("Done")

    return

def decode(seed, img_filename, bits_n, wav_output_dest):
    # Reading and setting the seed
    np.random.seed(int.from_bytes(seed.encode(), "little") % (2**32 - 1))

    # Reading the image file
    img = imageio.imread(img_filename)

    # Recovering the positions used for hiding using the seed
    positions = np.arange(img.shape[0] * img.shape[1] * img.shape[2])
    np.random.shuffle(positions)

    # Recovering the bit rate
    wav_rate = get_int(32, img, positions[:(32 // bits_n)])

    # Recovering the total number of samples
    total_samples = get_int(32, img, positions[(32 // bits_n) : 2 * (32 // bits_n)])

    # Recovering the samples
    pr_str = "Progress: 0%"
    print(pr_str, end='')
    backspace(len(pr_str))

    wav_data = np.zeros(total_samples)
    pos = 2 * (32 // bits_n)
    k = 0
    for i in np.arange(total_samples):
        sample = get_int(16, img, positions[pos : pos + (16 // bits_n)])
        wav_data[i] = np.uint16(sample)
        pos += (16 // bits_n)

        k += 1
        progress = k / total_samples
        pr_str = "Progress: " + "{:.2f}".format(progress * 100) + "%"
        print(pr_str, end='')

        if (progress < 1):
            backspace(len(pr_str))
        else:
            print("")

    # Converting samples to int16
    wav_data = (wav_data.astype(int) - (2**15 - 1)).astype(np.int16)

    sf.write(wav_output_dest, wav_data, wav_rate, 'PCM_16')
    print("Done")

    return

def main():
	op_flag = sys.argv[1].rstrip()
	if (op_flag == encode_flag):
		m_seed = sys.argv[2].rstrip()
		m_wav = sys.argv[3].rstrip()
		m_img = sys.argv[4].rstrip()
		m_bits = int(sys.argv[5])
		m_out = sys.argv[6].rstrip() 
		
		encode(m_seed, m_wav, m_img, m_bits, m_out)

	elif (op_flag == decode_flag):
		m_seed = sys.argv[2].rstrip()
		m_img = sys.argv[3].rstrip()
		m_bits = int(sys.argv[4])
		m_out = sys.argv[5].rstrip() 
		
		decode(m_seed, m_img, m_bits, m_out)
		
encode_flag = "-e"
decode_flag = "-d"

if __name__ == "__main__":
	main()
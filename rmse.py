import numpy as np
import imageio
import sys

def rmse_error(image1, image2):
    squared_diff = np.power(image1 - image2, 2)
    error = np.sqrt(squared_diff.mean())

    return error

img1_file = sys.argv[1]
img1 = imageio.imread(img1_file).astype(np.uint8)

img2_file = sys.argv[2]
img2 = imageio.imread(img2_file).astype(np.uint8)

err = rmse_error(img1, img2)
print ("{:.4f}".format(err))
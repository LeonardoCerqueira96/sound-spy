import imageio
import sys
import numpy as np

def normalize_between(data, min_t, max_t):
    data = (data - np.min(data)) / (np.max(data) - np.min(data))
    data = data * (max_t - min_t) + min_t
    
    return data

jpgfile = sys.argv[1].rstrip()
img = normalize_between(imageio.imread(jpgfile), 0.0, 255.0).astype(np.uint8)
imageio.imwrite(jpgfile[:jpgfile.find(".jpg")] + ".png", img)
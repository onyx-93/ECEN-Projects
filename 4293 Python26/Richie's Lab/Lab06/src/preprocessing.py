"""Image preprocessing functions for Lab 6"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def read_image(filename: str):
    """Read the file indicated by filename as a numpy rgb image array."""
    return np.array(plt.imread(Path(filename)))

def luma_transform(rgb_ndarray):
    """Perform the luma transform on the red, green, and blue channels of the image ndarray"""
    return np.dot(rgb_ndarray[...,:3], [.2989, .5870, .1140])

def preprocess(filename: str):
    """Given an image filename, load and convert the image to a grayscale ndarray."""
    return luma_transform(read_image(filename))

if __name__ == "__main__":
    # Run self-test code if called directly
    G = preprocess('images/hallett_peak.jpg')
    print(G.shape)
    plt.imshow(G, cmap='gray')
    plt.axis('off')
    plt.show()


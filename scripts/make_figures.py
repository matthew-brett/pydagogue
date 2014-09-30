#!/usr/bin/env python
""" Make stunning_figure.png
"""

# The brain analysis script
import numpy as np

import scipy.ndimage as spnd
import matplotlib.pyplot as plt

np.random.seed(42)

# Make brain data
brain_size = (128, 128)


def getfig():
    data = np.random.normal(size=brain_size)
    return spnd.gaussian_filter(data, 8)


plt.imshow(getfig(), cmap='gray')
plt.savefig('stunning_figure.png')

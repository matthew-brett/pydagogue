""" Script to make some expensive-looking data

Data that are in fact about as cheap as you can imagine.
"""

import numpy as np

N = 5000
FUDGE = 42

np.random.seed(42)

# The data from outside the brain
x = np.random.normal(10, 3, size=N)

# Data from inside the brain
y0 = np.random.normal(20, 6, size=N) + 2 * x
y1 = np.e ** y0 / FUDGE / np.e ** np.pi

# Save it to use later
np.savetxt('expensive_data.csv', np.c_[x, y1], delimiter=',')

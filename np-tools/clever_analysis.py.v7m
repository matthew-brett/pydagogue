# The brain analysis script
import numpy as np

import matplotlib.pyplot as plt

FUDGE = 42
HOT_FUDGE = 1.707

# Load data from the brain
data = np.loadtxt('expensive_data.csv', delimiter=',')

# First column is something from world, second is something from brain
from_world, from_brain = data.T

# Process data
from_brain_processed = np.log(from_brain) * FUDGE * np.e ** np.pi
from_brain_processed = from_brain_processed / HOT_FUDGE

# Make plot
plt.plot(from_world, from_brain_processed, 'r:')
plt.plot(from_world, from_brain_processed, 'bx')
plt.xlabel('Data from the outside world')
plt.ylabel('Data from inside the brain')
plt.title('Important finding')
plt.savefig('fancy_figure.png')

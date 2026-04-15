import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import random

x_0 = random.uniform(1, 4)

def asymptote_func(x):
    return 1/(x - x_0)

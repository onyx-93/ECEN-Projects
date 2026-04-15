############################################################################################
# Spice + c2q are a computationally expensive noisy black function, main goal is to attack #
# these using Bayesian optimization learn where to probe next to reduce the SPICE call for #
# far less times. Aims to solve x^* = argmax f(x), where x belongs to X, f(x) is an        #
# unknown expensive function.                                                               #
#
#
#
# 
############################################################################################
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import random

def generate_x0(low = 0.0, high = 100.0):
    return random.uniform(low, high)

def toy_delay_asymptote(x, x0, d_nom=50.0, scale=2000.0):
    """
    Delay model: d(x) = scale / (x - x0) for x > x0
    For x <= x0, treat as failure (NaN).
    """
    if x <= x0:
        return float('NaN')
    return d_nom + scale / (x - x0)





# Bayesian Optimization general approach code
import numpy as np
from scipy.stats import norm
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern

# Objective function (example: unknown function)
def f(x):
    return np.sin(3*x) + x**2 - 0.7*x

# Expected Improvement acquisition function
def expected_improvement(X, X_sample, Y_sample, gp, xi=0.01):
    mu, sigma = gp.predict(X, return_std=True)
    mu_sample = gp.predict(X_sample)

    sigma = sigma.reshape(-1, 1)
    mu_sample_opt = np.max(mu_sample)

    with np.errstate(divide='warn'):
        Z = (mu - mu_sample_opt - xi) / sigma
        ei = (mu - mu_sample_opt - xi) * norm.cdf(Z) + sigma * norm.pdf(Z)
        ei[sigma == 0.0] = 0.0

    return ei

# Propose next sampling point
def propose_location(acquisition, X_sample, Y_sample, gp, bounds, n_restarts=25):
    dim = bounds.shape[0]
    best_x = None
    best_acq = -np.inf

    for _ in range(n_restarts):
        x0 = np.random.uniform(bounds[:, 0], bounds[:, 1], size=dim)
        x = x0.reshape(1, -1)

        acq_value = acquisition(x, X_sample, Y_sample, gp)

        if acq_value > best_acq:
            best_acq = acq_value
            best_x = x

    return best_x

# Bayesian Optimization loop
def bayesian_optimization(n_iters, sample_loss, bounds):
    X_sample = np.random.uniform(bounds[:, 0], bounds[:, 1], (3, bounds.shape[0]))
    Y_sample = sample_loss(X_sample)

    kernel = Matern(nu=2.5)
    gp = GaussianProcessRegressor(kernel=kernel)

    for i in range(n_iters):
        gp.fit(X_sample, Y_sample)

        X_next = propose_location(expected_improvement, X_sample, Y_sample, gp, bounds)
        Y_next = sample_loss(X_next)

        X_sample = np.vstack((X_sample, X_next))
        Y_sample = np.vstack((Y_sample, Y_next))

        print(f"Iteration {i+1}: x = {X_next}, y = {Y_next}")

    return X_sample, Y_sample

# Run
bounds = np.array([[-2.0, 2.0]])
X, Y = bayesian_optimization(10, f, bounds)

best_idx = np.argmax(Y)
print("Best solution:", X[best_idx], Y[best_idx])
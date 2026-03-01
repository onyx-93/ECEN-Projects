import matplotlib.pyplot as plt
import numpy as np
import math

# Problem 1 
# Takes: function (f), two brackets (a, b), tolerance which is <10^-8, and a max number of iterations (max_it).
def bisection(f, a, b, tol=1e-9, max_it=200):

    fa, fb = f(a), f(b) # Inititalize function variables

    iteration_counter = 0

    if fa * fb >= 0: # Sign check feature
        raise ValueError("f(a) and f(b) must have different signs.")
    
    for _ in range(max_it): # Iteration through the max amount of attempts
        c = 0.5 * (a + b) # Obtain midpoint
        fc = f(c) # Obtain func value at midpoint
    
        if abs(fc) < tol or 0.5 * (b - a) < tol: # Tolerance satisfaction check
            return c, iteration_counter
    
        if fa * fc < 0: # Limit check and assignment
            b, fb = c, fc
        else:
            a, fa = c, fc
        
        iteration_counter += 1

    return 0.5 * (a + b), iteration_counter # If tolerance not reached, return closest value

# Function problem 1. Sin(theta) - (theta)^2 Vectorized using numpy for graphing

def f_vector_plot_p1(x):
    return np.sin(x) - x**2

# Function for problem 1. Scalar version to pass to bisection for calculation.

def f_scalar_p1(x):
    return math.sin(x) - x**2

# Obtain/assign x and y plotting points

# values_xrange = np.linspace(-50, 50, 100)

# values_yrange = f_vector_plot_p1(values_xrange)

# plt.figure(figsize=(8, 6)) # Adjusts the size of the figure
# plt.plot(values_xrange, values_yrange, label='$Sin(x) - x^2$')

# plt.xlabel("f(x) inputs")
# plt.ylabel("f(x) outputs")
# plt.legend()
# plt.grid(True)

# plt.show()

# Obtain the bisection approximation once the limit brackets were set to: -0.5 and 0.5

# root = bisection(f_scalar_p1, -345e6, -0.1)
# print(f"\n\tThe value obtiained from the bisection method was: {root}")

# ========================================================================================
#                                   --- Problem 2 ---
# ========================================================================================

def f_vector_plot_p2(x):
    return np.cos(x) - x

def f_scalar_p2(x):
    return math.cos(x) - x

# default_output_p2, iterations_p2 = bisection(f_scalar_p2, -1, 1, 10e-4)
# print(f"\n\tThe number of iterations for cos(theta) - theta is: {iterations_p2}\n")

# # Result was 10

# values_xrange_p2 = np.linspace(-10, 10, 100)
# values_yrange_p2 = f_vector_plot_p2(values_xrange_p2)

# plt.plot(values_xrange_p2, values_yrange_p2, label='$Cos(x) - x$')
# plt.grid(True)
# plt.show()

# Define regula falsi function

def reg_falsi(f, a, b, tol=10e-8, max_it=100):
    
    # Declare all needed variables

    iteration_counter = 0
    fa, fb = f(a), f(b)

    if fa * fb >= 0:
        raise ValueError("Limit points f(a) and f(b) should be of opposite sign.")
    
    for _ in range(max_it):
        c = ((a*fb - b*fa)/(fb - fa))
        fc = f(c)

        if (abs(fc) < tol):
            return c, iteration_counter
    
        # Reassign c
        if fa * fc < 0:
            b, fb = c, fc
        else:
            a, fa = c, fc
        # Update limits

        iteration_counter += 1

    return c, iteration_counter

p2_output, iter_reg_falsi_p2 = reg_falsi(f_scalar_p2, -1, 1)
print(f"The total number of iterations for regula falsi on the range [-1, 1] is: {iter_reg_falsi_p2}")

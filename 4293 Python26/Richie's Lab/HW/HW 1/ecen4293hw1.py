import matplotlib.pyplot as plt
import numpy as np
import math

# ========================================================================================
#                               --- Function Definition ---
# ========================================================================================

# ================================== Problem 1 Functions =================================

# Function problem 1. Sin(theta) - (theta)^2 Vector version (Plotting)

def f_vector_plot_p1(x):
    return np.sin(x) - x**2

# Function for problem 1. Scalar version to pass to bisection for calculation.

def f_scalar_p1(x):
    return math.sin(x) - x**2

# ================================== Problem 2 Functions =================================

# Function problem 2. Cos(theta) - theta | Vector version (Plotting)

def f_vector_plot_p2(x):
    return np.cos(x) - x

# Function problem 2. Cos(theta) - theta | Scalar version

def f_scalar_p2(x):
    return math.cos(x) - x

# ================================== Problem 3 Functions =================================

# Function problem 3. sin(sqrt(x)) - x | Vector version (Plotting)

def p3_vect(x):
    return np.sin(np.sqrt(x)) - x

# Function problem 3. sin(sqrt(x)) - x | Vector version (Plotting)

def p3_scal(x):
    return math.sin(math.sqrt(x)) - x

# ================================== Problem 4 Functions =================================



# ================================== Problem 5 Functions =================================



# ================================== Problem 6 Functions =================================

def p6_scal(x):
    return -0.3*x**4 + 1.8*x**3 - 1.2*x**2 + 2*x

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ========================================================================================
#                                   --- Problem 1 ---
# ========================================================================================

# Takes: function (f), two brackets (a, b), tolerance which is <10^-8, and a max number of iterations (max_it).
def bisection(f, a, b, tol=1e-9, max_it=100):

    fa, fb = f(a), f(b) # Inititalize function variables
    roots_list = []
    iteration_counter = 0

    if fa * fb >= 0: # Sign check feature
        raise ValueError("f(a) and f(b) must have different signs.")
    
    for _ in range(max_it): # Iteration through the max amount of attempts
        c = 0.5 * (a + b) # Obtain midpoint
        fc = f(c) # Obtain func value at midpoint
    
        if abs(fc) < tol or 0.5 * (b - a) < tol: # Tolerance satisfaction check
            return c, iteration_counter, roots_list
    
        if fa * fc < 0: # Limit check and assignment
            b, fb = c, fc
        else:
            a, fa = c, fc
        
        iteration_counter += 1
        roots_list.append(c)

    return 0.5 * (a + b), iteration_counter, roots_list # If tolerance not reached, return closest value

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


# ========================== --- Function iteraction check --- ============================

default_output_p2, iterations_p2, ls_bisection = bisection(f_scalar_p2, -1, 1, 10e-4)
# print(f"\n\tThe number of iterations for cos(theta) - theta is: {iterations_p2}\n")

# # Result was 10

# values_xrange_p2 = np.linspace(-10, 10, 100)
# values_yrange_p2 = f_vector_plot_p2(values_xrange_p2)

# plt.plot(values_xrange_p2, values_yrange_p2, label='$Cos(x) - x$')
# plt.grid(True)
# plt.show()

# ============================= --- Regula Falsi definition --- ============================

def reg_falsi(f, a, b, tol=1e-9, max_it=100):
    
    # Declare all needed variables
    
    fa, fb = f(a), f(b)
    roots_list = []
    iteration_counter = 0

    if fa * fb >= 0:
        raise ValueError("Limit points f(a) and f(b) should be of opposite sign.")
    
    for _ in range(max_it):
        c = ((a*fb - b*fa)/(fb - fa))
        fc = f(c)

        if (abs(fc) < tol):
            return c, iteration_counter, roots_list
    
        # Reassign c
        if fa * fc < 0:
            b, fb = c, fc
        else:
            a, fa = c, fc
        # Update limits

        iteration_counter += 1
        roots_list.append(c)

    return c, iteration_counter, roots_list

# p2_output, iter_reg_falsi_p2, ls_reg_falsi = reg_falsi(f_scalar_p2, -1, 1)
# print(f"The total number of iterations for regula falsi on the range [-1, 1] is: {iter_reg_falsi_p2}")

# x_true = 0.739085

# error_bis = [abs(x - x_true) for x in ls_bisection]
# error_rf   = [abs(x - x_true) for x in ls_reg_falsi]

# iters_bis = range(len(error_bis))
# iters_rf = range(len(error_rf))


# plt.semilogy(iters_bis, error_bis, label="Bisection")
# plt.semilogy(iters_rf, error_rf, label="Regula Falsi")

# plt.xlabel("Iteration")
# plt.ylabel("Absolute Error")
# plt.grid(True, which="both")
# plt.legend()
# plt.show()

# ========================================================================================
#                                   --- Problem 3 ---
# ========================================================================================

# =========================== --- Fixed Point Definition --- =============================

def fixed_point(f, guess, tol=1e-9, max_it=100):
    memory = [guess] # List to store the values  to calculate error
    x = guess
    for i in range(max_it):
        x_next = f(x)
        memory.append(x_next)

        if abs(x_next - x) < tol:
            return x_next, memory
        
        x = x_next

    raise ValueError("Solution did not converge")

# root, list_high_tolerance = fixed_point(p3_scal, 0.5, 1e-4)
# root_ref, list_low_tolerance = fixed_point(p3_scal, 0.5, 1e-10)
# print(f"Solution with high tolerance:{root:.4f} | low tolerance: {root_ref:.4f}")

# true_error = [abs(root_ref - x) for x in list_low_tolerance]
# relative_error = [abs(root_ref - x)/abs(root_ref) for x in list_low_tolerance]

# iterations = range(len(list_low_tolerance))

# plt.plot(iterations, true_error, label="True Error")
# plt.plot(iterations, relative_error, label="Relative Error")

# plt.yscale("log")
# plt.xlabel("Iteration")
# plt.ylabel("Error")
# plt.legend()
# plt.grid(True)
# plt.show()

# ========================================================================================
#                                   --- Problem 4 ---
# ========================================================================================






# ========================================================================================
#                                   --- Problem 5 ---
# ========================================================================================






# ========================================================================================
#                                   --- Problem 6 ---
# ========================================================================================

def golden_section(f, xl, xu, es=1):
    R = (np.sqrt(5) - 1) / 2

    iter_counter = 0
    ea = 100

    x1 = xu - R*(xu - xl)
    x2 = xl + R*(xu - xl)
    f1, f2 = f(x1), f(x2)

    while ea > es:
        iter_counter += 1

        if f1 < f2:
            xu = x2
            x2 = x1
            f2 = f1
            x1 = xu - R*(xu-xl)
            f1 = f(x1)
        else:
            xl = x1
            x1 = x2
            f1 = f2
            x2 = xl + R*(xu-xl)
            f2 = f(x2)

        xopt = (xl + xu)/2
        ea = (1 - R)*abs((xu - xl)/xopt)*1000

    return xopt, f(xopt), iter_counter

x_max, f_max, iters = golden_section(p6_scal, -2, 4, 1)

print("Golden Section Result:")
print("x_max =", x_max)
print("f(x_max) =", f_max)
print("iterations =", iters)


def parabolic_max(f, x1, x2, x3, iterations=5):
    
    for i in range(iterations):
        f1, f2, f3 = f(x1), f(x2), f(x3)

        numerator = ((x2 - x1)**2 * (f2 - f3) - 
                     (x2 - x3)**2 * (f2 - f1))
        
        denominator = ((x2 - x1)*(f2 - f3) - 
                       (x2 - x3)*(f2 - f1))
        
        xr = x2 - 0.5 * numerator / denominator

        x1, x2, x3 = x2, xr, x3
    
    return xr, f(xr)

x_max_p, f_max_p = parabolic_max(p6_scal, 1.7, 2, 2.7, 5)

print("\nParabolic Interpolation Result:")
print("x_max =", x_max_p)
print("f(x_max) =", f_max_p)
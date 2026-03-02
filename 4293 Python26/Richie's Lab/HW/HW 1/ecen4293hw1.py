import matplotlib.pyplot as plt
import numpy as np
import math

# Code done by: Ricardo Landeros Aranda
# ECEN 4293 - Python with Numerical Methods
# Spring 2026 | Oklahoma State University

# This code was completed and checked with the use of generative AI. Mostly to understand
# concepts, and how to apply them.
# Link to the chat: https://chatgpt.com/share/69a3c0b2-1de8-8013-abd1-d7806ed3c7e3

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

# Scalar versions of functions

def p4_func_one(x):
    return -0.87*x**2 + 1.65*x + 8.25

def p4_dfunc_one(x):    # Derivative of p4_func_one
    return -1.74*x + 1.65


def p4_funct_two(x):
    return 0.7*x**3 - 3.7*x**2 + 6.31*x -1.9

def p4_dfunct_two(x):   # Derivative of p4_func_two
    return  2.1*x**2 - 7.4*x + 6.31


# ================================== Problem 5 Functions =================================

# Functions problem 5. -(theta)^3 + 3sin(theta) + cos(theta) + 9 | Vector version

def p5_vect(x):
    return -x**3 + 3*np.sin(x) + np.cos(x) + 9


# Functions problem 5. -(theta)^3 + 3sin(theta) + cos(theta) + 9 | Scalar version

def p5_scalar(x):
    return -x**3 + 3*math.sin(x) + math.cos(x) + 9

def p5_scalar_df(x):
    return -3*x**2 + 3*math.cos(x) - math.sin(x) 

# ================================== Problem 6 Functions =================================

# Only need scalar version of function

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

    if fa * fb >= 0: # Sign check feature
        raise ValueError("f(a) and f(b) must have different signs.")
    
    for i in range(max_it): # Iteration through the max amount of attempts
        c = 0.5 * (a + b) # Obtain midpoint
        fc = f(c) # Obtain func value at midpoint
    
        if abs(fc) < tol or 0.5 * (b - a) < tol: # Tolerance satisfaction check
            return c, i, roots_list
    
        if fa * fc < 0: # Limit check and assignment
            b, fb = c, fc
        else:
            a, fa = c, fc
        
        roots_list.append(c)

    return 0.5 * (a + b), i, roots_list # If tolerance not reached, return closest value

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

# default_output_p2, iterations_p2, ls_bisection = bisection(f_scalar_p2, -1, 1, 10e-4)
# print(f"\n\tThe number of iterations for cos(theta) - theta is: {iterations_p2}\n")

# -- Result was 10 --

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

    if fa * fb >= 0:
        raise ValueError("Limit points f(a) and f(b) should be of opposite sign.")
    
    for i in range(max_it):
        c = ((a*fb - b*fa)/(fb - fa))
        fc = f(c)

        if (abs(fc) < tol):
            return c, i, roots_list
    
        # Reassign c
        if fa * fc < 0:
            b, fb = c, fc
        else:
            a, fa = c, fc
        # Update limits

        roots_list.append(c)

    return c, i, roots_list

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

def newton_raphson(f, df, x0, tol=1e-8, max_it=100):
    memory =[x0]
    x = x0

    for i in range(max_it):
        fx = f(x)
        dfx = df(x)

        if abs(dfx) < 1e-12:
            raise ValueError("Derivative too small -- risk of division by zero.")
        
        x_next = x - fx/dfx
        memory.append(x_next)

        if abs(x_next - x) < tol:
            return x_next, i, memory
        
        x = x_next


    raise ValueError("\n\tFunction did not converge\n")

# Plotting and finding roots graphically

# x_vals = np.linspace(-4, 6, 100)
# y_vals_f1 = p4_func_one(x_vals)
# y_vals_f2 = p4_funct_two(x_vals)

# plt.plot(x_vals, y_vals_f1, label="$f(x)_1$")
# plt.plot(x_vals, y_vals_f2, label="$f(x)_2$")
# plt.ylim(-10, 10)
# plt.grid(True)
# plt.legend()
# plt.show()

# Roots for f(x)_1: x1 = -2.273, x2 = 4.17
# Root for f(x)_2: x1 = 0.381

# root1_nr_f1, iterf1 = newton_raphson(p4_func_one, p4_dfunc_one, 5)
# print(f"First root of f(x)_1 : {root1_nr_f1:.4f}")  # Approximated root: 4.1704
# root2_nr_f1, iterf1_r2 = newton_raphson(p4_func_one, p4_dfunc_one, -4)
# print(f"First root of f(x)_1 : {root2_nr_f1:.4f}")  # Approximated root: -2.2738
# root1_nr_f2, iterf2 = newton_raphson(p4_funct_two, p4_dfunct_two, 2)
# print(f"Root of f(x)_2 : {root1_nr_f2:.4f}") # Approximated root: 0.3795

# print(p4_func_one(4.1704))
# print(p4_func_one(-2.2738))
# print(p4_funct_two(0.3795))




# ========================================================================================
#                                   --- Problem 5 ---
# ========================================================================================

def secant_method(f, a, b, tol=1e-9, max_it=100):
    memory = []
    x1, x2 = a, b
    

    for i in range(max_it):
        fx1, fx2 = f(x1), f(x2)

        if abs(fx2 - fx1) < 1e-14:
            raise ValueError("Denominator too small -- risk to divide by zero.")
        
        # Secant update
        x3 = x2 - fx2 * (x2 - x1)/(fx2 - fx1)
        memory.append(x3)
        # Convergence check
        if abs(x3 - x2) < tol:
            return x3, i, memory
        
        x1, x2 = x2, x3

    raise ValueError("Function did not converge.")

# root_bisection, iteration_bisection, bisection_roots = bisection(p5_scalar, 0, 4, 1e-4)

# root_reg_fal, iteration_reg_fal, reg_fal_roots = reg_falsi(p5_scalar, 0, 4, 1e-4)

# root_new_raph, counter_new_raph, new_raphson_roots = newton_raphson(p5_scalar, p5_scalar_df, 3, 1e-4)

# root_sec_met, counter_sec_met, roots_sec_met = secant_method(p5_scalar, 0, 4, 1e-4)

# plt.plot(bisection_roots, label="Bisection")
# plt.plot(reg_fal_roots, label="Regula Falsi")
# plt.plot(new_raphson_roots, label="Newton-Raphson")
# plt.plot(roots_sec_met, label="Secant")

# plt.xlabel("Iterations")
# plt.ylabel("Approximation of Theta")
# plt.legend()
# plt.grid(True)
# plt.show()



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

# x_max, f_max, iters = golden_section(p6_scal, -2, 4, 1)

# print("Golden Section Result:")
# print("x_max =", x_max)
# print("f(x_max) =", f_max)
# print("iterations =", iters)


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

# x_max_p, f_max_p = parabolic_max(p6_scal, 1.7, 2, 2.7, 5)

# print("\nParabolic Interpolation Result:")
# print("x_max =", x_max_p)
# print("f(x_max) =", f_max_p)
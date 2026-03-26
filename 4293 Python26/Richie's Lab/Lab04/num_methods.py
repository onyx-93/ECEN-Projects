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

# ============================= --- Bisection method definition --- ======================

def bisection(f, a, b, tol=1e-9, max_it=100):

    fa, fb = f(a), f(b) # Inititalize function variables
    roots_list = []

    # if fa * fb >= 0: # Sign check feature
    #     raise ValueError("f(a) and f(b) must have different signs.")
    
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

# ============================= --- Regula Falsi definition --- ==========================

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

# ============================= --- Newton-Raphson definition --- =========================

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

# ============================= --- Secant method definition --- ==========================

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

# ============================= --- Golden-Section and Parabolic interpolation definition --- ============================

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

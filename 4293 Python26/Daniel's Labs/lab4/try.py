import numpy as np
import matplotlib.pyplot as plt
from numerical_methods import method_gen


#GEN = method_gen() # method generator

def f(x):
    """Original function f(x) = sin(√x) - x"""
    return np.sin(np.sqrt(x)) - x

def g(x):
    """Fixed-point form: x = g(x) = sin(√x)"""
    return np.sin(np.sqrt(x))

def d_fx(func, x, h=1e-8):
    """Approximate f'(x) using central finite difference"""
    return (func(x + h) - func(x - h)) / (2 * h)


 
def error_analysis(num_method, x_true, *args, **kwargs):
    """ *args will accept f(x), g(x),x0, x1, x2, df, tolerance
        **kwargs will accept plot_err, plot_con
    """
    
    
    
    # order_of _convergence = xi-1 / xi
    return None # order_of_convergence







import numpy as np
import matplotlib.pyplot as plt


def d_fx(func, x, h=1e-8):
    """Approximate f'(x) using central finite difference"""
    return (func(x + h) - func(x - h)) / (2 * h)

def bisection_gen(xl, xu, TOL, func):
    """MODIFICATION: Generator version. Yields each xm. Accepts func for generality."""
    if func(xl) * func(xu) >= 0:
        raise ValueError("Error: No sign change — bad bracket")
    i = 0
    while abs(xu - xl) >= TOL and i < 500:
        xm = (xl + xu) / 2
        yield xm
        if func(xm) * func(xl) < 0:
            xu = xm
        else:
            xl = xm
        i += 1
    yield xm   # final refined value

def regula_falsi_gen(xl, xu, TOL, func):
    """MODIFICATION: Generator version. Yields each xr."""
    if func(xl) * func(xu) >= 0:
        raise ValueError("Error: No sign change — bad bracket")
    
    yield xl, xu
    
    while abs(xu - xl) >= TOL:
        denominator = (func(xl) - func(xu))
        
        if abs(denominator) < 1e-12:
            raise ValueError("Error: denominator zero — cannot proceed")
        
        xr = (xu * func(xl) - xl * func(xu)) / denominator
        yield xr
        
        if func(xr) * func(xl) < 0:
            xl = xr
        else:
            xu = xr

    yield xr


def fixed_point_gen(x0, TOL, g_func):
    """MODIFICATION: Generator for fixed-point. Uses g_func (you pass your g)."""
    xi = x0
    yield xi 
    i = 0
        
    while True:
        i += 1
        if i > 500:
            raise ValueError("Fixed point did not converge")
        
        x_new = g_func(xi)
        yield x_new
        diff = abs(x_new - xi)
        
        if diff < TOL:
            break
        
        xi = x_new
        

def newton_raphson_gen(x0, TOL, func):
    x = x0
    yield x                     # starting point
    
    while True:
        fx = func(x)
        dfx = d_fx(func, x)
        
        if abs(dfx) < 1e-12:
            raise ValueError("Derivative near zero")
        
        x_new = x - fx / dfx
        yield x_new
        
        if abs(x_new - x) < TOL:
            break
        x = x_new
    

def secant_gen(x0, x1, TOL, func):
    xa, xb = x0, x1               # xa = older, xb = newer
    fa, fb = func(xa), func(xb)
    
    yield xb                      # first meaningful point
    
    while True:
        denom = fb - fa
        if abs(denom) < 1e-12:
            raise ValueError("secant denominator near zero")
        
        xc = xb - fb * (xb - xa) / denom
        yield xc
        
        if abs(xc - xb) < TOL:
            break
        
        # shift
        xa, fa = xb, fb
        xb, fb = xc, func(xc)
    

def golden_section_search_gen(xl, xu, epsilon_s, func):
    """MODIFICATION: Generator version. Yields current midpoint estimate each iteration."""
    phi = (1 + np.sqrt(5)) / 2
    r = 1 / phi
    while xu - xl >= epsilon_s:
        d = r * (xu - xl)
        x1 = xl + d
        x2 = xu - d
        f1 = func(x1)
        f2 = func(x2)

        if f1 < f2:          
            xu = x2
            x2 = x1
            x1 = xu
        else:
            xl = x1
            x1 = x2
            x2 = xl
        
        x_max = (xl + xu) / 2
        yield x_max
    


def parabolic_interpol_gen(x1, x2, x3, func):
    """MODIFICATION: Generator version (fixed 5 iterations as in your original)."""
    for i in range(5):
        f1 = func(x1)
        f2 = func(x2)
        f3 = func(x3)
        num = (x2 - x1)**2 * (f2 - f3) - (x2 - x3)**2 * (f2 - f1)
        den = (x2 - x1) * (f2 - f3) - (x2 - x3) * (f2 - f1)
        
        if abs(den) < 1e-12:
            yield x2
        
        x4 = x2 - (0.5 * (num / den))
        yield x4
        f4 = func(x4)
        
        if f1 == max([f1, f2, f3, f4]) or f2 == max([f1, f2, f3, f4]):
            x3 = x2
        else:
            x1 = x2
            x2 = x3
            x3 = x4
    
    


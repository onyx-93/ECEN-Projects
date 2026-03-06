import numpy as np
import matplotlib.pyplot as plt


def d_fx(func, x, h=1e-8):
    """Approximate f'(x) using central finite difference"""
    return (func(x + h) - func(x - h)) / (2 * h)

def Bisection(xl, xu, TOL, func):
    """MODIFICATION: Generator version. Yields each xm. Accepts func for generality."""
    if func(xl) * func(xu) >= 0:
        raise ValueError("Error: No sign change — bad bracket")
    
    i = 0
    while True:
        i += 1
        if i > 500:
            raise ValueError("Bisection method did not converge")
        
        xm = (xl + xu) / 2
        
        if abs(xu - xl) < TOL:
            yield xm
            break
        
        yield xm

        if func(xm) * func(xl) < 0:
            xu = xm
        else:
            xl = xm
    
def Regula_Falsi(xl, xu, TOL, func):
    """MODIFICATION: Generator version. Yields each xr."""
    if func(xl) * func(xu) >= 0:
        raise ValueError("Error: No sign change — bad bracket")
    
    i = 0
    while True:
        i += 1
        if i > 500:
            raise ValueError("Regula Falsi method did not converge")
    
        denominator = (func(xl) - func(xu))
        
        if abs(denominator) < 1e-14:
            yield xu
            break
        
        xr = (xu * func(xl) - xl * func(xu)) / denominator
        
        if abs(xu - xl) < TOL:
            yield xr
            break
        
        yield xr
        
        if func(xr) * func(xl) < 0:
            xl = xr
        else:
            xu = xr



def Fixed_Point(x0, TOL, g):
    """MODIFICATION: Generator for fixed-point. Uses g_func (you pass your g)."""
    xi = x0
    yield xi 
    i = 0    
    while True:
        i += 1
        if i > 500:
            raise ValueError("Fixed point did not converge")
        
        x_new = g(xi)
        yield x_new
        diff = abs(x_new - xi)
        
        if diff < TOL:
            break
        
        xi = x_new
        

def Newton_Raphson(x0, TOL, func):
    x = x0
    yield x                     # starting point
    i = 0
    while True:
        i += 1
        if i > 500:
            raise ValueError("Newton-Raphson method did not converge")
        
        fx = func(x)
        dfx = d_fx(func, x)
        
        if abs(dfx) < 1e-12:
            raise ValueError("Derivative near zero")
        
        x_new = x - fx / dfx
        yield x_new
        
        if abs(x_new - x) < TOL:
            break
        
        x = x_new
    

def Secant(x0, x1, TOL, func):
    xa, xb = x0, x1               # xa = older, xb = newer
    fa, fb = func(xa), func(xb)
    yield xb                      # first meaningful point
    i = 0
    while True:
        i += 1
        if i > 500:
            raise ValueError("Secant method did not converge")
        
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
    

def Golden_Section_Search(xl, xu, epsilon_s, func):
    """MODIFICATION: Generator version. Yields current midpoint estimate each iteration."""
    phi = (1 + np.sqrt(5)) / 2
    r = 1 / phi
    i = 0
    while True:
        i += 1
        if i > 500:
            raise ValueError("Golden Section Search method did not converge")
        
        d = r * (xu - xl)
        x1 = xl + d
        x2 = xu - d
        f1 = func(x1)
        f2 = func(x2)

        if f1 <= f2:          
            xu = x2
            x2 = x1
            x1 = xu
        else:
            xl = x1
            x1 = x2
            x2 = xl
        
        x_max = (xl + xu) / 2
        
        if  xu - xl < epsilon_s:
            yield x_max
            break
        
        yield x_max


def Parabolic_Interpol(x1, x2, x3, TOL, func):
    """
    Stable generator version of parabolic interpolation for maximization.
    Keeps bracket and avoids denominator collapse.
    """

    i = 0
    while True:
        i += 1
        if i > 500:
            raise ValueError("Parabolic interpolation did not converge")

        f1 = func(x1)
        f2 = func(x2)
        f3 = func(x3)

        # Parabolic interpolation formula
        num = (x2 - x1)**2 * (f2 - f3) - (x2 - x3)**2 * (f2 - f1)
        den = (x2 - x1) * (f2 - f3) - (x2 - x3) * (f2 - f1)
        #print ('denominator:',den)

        # Near convergence safeguard
        if abs(den) < 1e-14:
            yield x2 #best estimate
            break

        x4 = x2 - 0.5 * (num / den)
        f4 = func(x4)

        if abs(x4 - x2) < TOL or abs(x3 - x1) < TOL:
            yield x4
            break

        yield x4

        # ---- Maintain bracket around maximum ----
        if f1 == max([f1, f2, f3, f4]) or f2 == max([f1, f2, f3, f4]):
            # x1 or x2 produces the maximum f(x) → eliminate x4
            x3 = x2                     # tighten the right side
        else:
            # otherwise eliminate x1 (shift the bracket rightward)
            x1 = x2
            x2 = x3
            x3 = x4
        


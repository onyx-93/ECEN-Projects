import numpy as np
import matplotlib.pyplot as plt


def f(x):
    return -x**3 + np.sin(x)*3 + np.cos(x) + 9 

def d_fx(func, x, h=1e-8):
    """Approximate f'(x) using central finite difference"""
    return (func(x + h) - func(x - h)) / (2 * h)

def bisection(xl, xu, TOL):
    #i = 0
    iterates = []
    while abs(xu - xl) >= TOL:
        xm = (xl + xu) / 2
        #i += 1
        #print(f"x{i} = {xm:.4f}") # Print each iterate
        
        iterates.append(xm) # Store iterates in a list
        
        if f(xm) * f(xl) < 0: 
            xu = xm
        else: 
            xl = xm
    
    return xm, iterates # Return final root and list of iterates

def regula_falsi(xl, xu, TOL):
    if f(xl) * f(xu) >= 0:
        print("Error: No sign change — bad bracket")
        return None, []
    
    #i = 0
    iterates = []
    while abs(xu - xl) >= TOL:
        denominator = (f(xl) - f(xu))
        if denominator == 0:
            print("Error: denominator zero — cannot proceed")
            return None

        xr = (xu * f(xl) - xl * f(xu)) / denominator
        #i += 1
        #print(f"x{i} = {xr:.4f}") # Print each iterate
        
        iterates.append(xr) # Store iterates in a list
        
        if f(xr) * f(xl) < 0:
            xl = xr
        else:
            xu = xr
    
    return xr, iterates # Return final root and list of iterates

def Newton_Raphson(x0, func, TOL):
    xi = x0 # initial guess
    function = func(xi) # initial function value at x0
    df = d_fx(func, xi) # initial derivative at x0
    iterates = [xi] # store all x values 
    
    # First iteration outside the loop to have valid diff
    x_new = xi - (function/df) # initial guess for Newton-Raphson
    diff = abs(x_new - xi)
    
    #i = 0
    #print(f"x{i+1} = {x_new:.4f}") # Print initial iterate
    
    iterates.append(x_new)
    
    while diff >= TOL:
        
        xi = x_new
        function = func(xi)
        df = d_fx(func, xi)
        x_new = xi - (function/df) #current value of Newton-Raphson
        diff = abs(x_new - xi)
        #i += 1
        #print(f"x{i+1} = {x_new:.4f}") # Print each iterate
        iterates.append(x_new)
    
    return x_new, iterates # Return final root and list of iterates
    
def secant(x0, x1, func, TOL):

    function_i = func(x0) # initial function value at x0
    function_j = func(x1) # initial function value at x1
    iterates = [x0] # store all x values  
    
    # First iteration outside the loop to have valid diff
    x_new = x0 - ((function_i * (x0 - x1)) / (function_i - function_j)) # initial guess for Secant method
    diff = abs(x_new - x0)
    
    #i = 0
    #print(f"x{i+1} = {x_new:.4f}") # Print initial iterate
    
    #iterates.append(x_new)
    
    while diff >= TOL:
        x0 = x_new
        x1 = x0 - 1 # Update xj to be the previous xi
        function_i = func(x0)
        function_j = func(x1)
        x_new = x0 - ((function_i * (x0 - x1)) / (function_i - function_j)) # Secant method update
        diff = abs(x_new - x0)
        iterates.append(x0)
        
        #i += 1
        #print(f"x{i+1} = {x_new:.4f}") # Print each iterate
        
    
    return x_new, iterates # Return final root and list of iterates


if __name__ == "__main__":

    TOL = 1e-4
    
    # Bisection and Regula Falsi parameters
    xl = 1.0
    xu = 2.5
    
    # Run bracketing methods with tracking
    root_b, iter_b = bisection(xl, xu, TOL)
    root_rf, iter_rf = regula_falsi(xl, xu, TOL)
    
    print(f"Bisection root: {root_b:.5f}")
    print(f"Regula Falsi root: {root_rf:.5f}")

    
    # Initial guesses for Secant method and Newton-Raphson
    x0 = 1.0
    x1 = 2.0
    
    # Run Newton-Raphson (already returns iterates)
    root_nr, iter_nr = Newton_Raphson(x0, f, TOL)
    print(f"Newton-Raphson root: {root_nr:.5f}")
    
    # Run Secant (already returns iterates)
    root_sec, iter_sec = secant(x0, x1, f, TOL)
    print(f"Secant root: {root_sec:.5f}")
    
    # ──────────────────────────────────────────────
    # Plot: approximation value vs iteration for each method
    # ──────────────────────────────────────────────
    plt.figure(figsize=(12, 7))
    
    # Bisection
    plt.plot(np.arange(len(iter_b)), iter_b, 'o-', 
             label='Bisection', linewidth=1.5, markersize=15, alpha=0.9)
    
    # Regula Falsi
    plt.plot(np.arange(len(iter_rf)), iter_rf, 'o-', 
             label='Regula Falsi', linewidth=1.5, markersize=10, alpha=0.9)
    
    # Newton-Raphson
    plt.plot(np.arange(len(iter_nr)), iter_nr, 'o-', 
             label='Newton-Raphson', color='black', linewidth=1.8, markersize=10, alpha=0.9)
    
    # Secant
    plt.plot(np.arange(len(iter_sec)), iter_sec, 'o-', 
             label='Secant', color='purple', linewidth=1.5, markersize=5, alpha=0.9)
    
    # Reference line at the converged root (average of all methods)
    avg_root = np.mean([root_b, root_rf, root_nr, root_sec])
    plt.axhline(avg_root, color='black', linestyle='--', linewidth=1.5, 
                label=f'Converged root ≈ {avg_root:.5f}')
    
    plt.xlabel('Iteration number')
    plt.ylabel('Approximation value x')
    plt.title('Convergence Behavior of Root-Finding Methods\n')
    plt.grid(True, which="both", ls="--", alpha=0.6)
    plt.legend(loc='best', fontsize=10)
    plt.tight_layout()
    
    # Save the plot (useful for homework submission)
    plt.savefig("problem5_convergence_plot.png", dpi=300, bbox_inches='tight')
    plt.show()
  

    # plotting the function to visually estimate the root
    #x_vals = np.linspace(-5, 5, 5000)
    #plt.figure(figsize=(10, 6))
    #plt.plot(x_vals, f(x_vals), label='f(x)', color='blue')
    #plt.axhline(0, color='black', lw=1.3, ls='--')
    #plt.axvline(0, color='black', lw=1.3, ls='--')
    #plt.xlim(-10, 10)
    #plt.ylim(-10, 15)
    #plt.xlabel('x')
    #plt.ylabel('f(x)')
    #plt.title('Plot of f(x) to visually estimate the root')
    #plt.grid()
    #plt.show()
    
    
    
    

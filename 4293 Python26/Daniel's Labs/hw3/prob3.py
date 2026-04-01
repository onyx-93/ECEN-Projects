import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial.polynomial import Polynomial

def lagrange(points):
    """Compute interpolating polynomial using Lagrange method."""
    points = np.asarray(points, dtype=float)
    if points.ndim != 2 or points.shape[1] != 2:
        raise ValueError("points must be a 2D array of shape (n, 2)")
    
    x = points[:, 0]
    y = points[:, 1]
    n = len(x)
    
    total_coeffs = np.zeros(n, dtype=float)
    
    for i in range(n):
        basis = np.array([1.0])
        for j in range(n):
            if i == j:
                continue
            denom = x[i] - x[j]
            linear = np.array([-x[j], 1.0])
            basis = np.polymul(basis, linear) / denom
        
        basis_scaled = basis * y[i]
        total_coeffs = np.polyadd(total_coeffs, basis_scaled)
    
    return Polynomial(total_coeffs)

def d_fx(func, x, h=1e-8):
    """Approximate f'(x) using central finite difference"""
    return (func(x + h) - func(x - h)) / (2 * h)

def Newton_Raphson(x0, func, TOL):
    xi = x0 # initial guess
    function = func(xi) # initial function value at x0
    df = d_fx(func, xi) # initial derivative at x0
    
    # First iteration outside the loop to have valid diff
    x_new = xi - (function/df) # initial guess for Newton-Raphson
    diff = abs(x_new - xi)
    
    while diff >= TOL:
        
        xi = x_new
        function = func(xi)
        df = d_fx(func, xi)
        x_new = xi - (function/df) #current value of Newton-Raphson
        diff = abs(x_new - xi)
    
    return x_new # Return final root
    

if __name__ == "__main__":
    # Data from the table: Wavelength (Å) vs Refractive Index (n)
    data = np.array([
        [6563, 1.50883],
        [6439, 1.50917],
        [5890, 1.51124],
        [5338, 1.51386],
        [5086, 1.51534],
        [4861, 1.51690],
        [4340, 1.52136],
        [3988, 1.52546]
    ])
    
    # Compute the Lagrange interpolating polynomial
    p = lagrange(data)
    
# Part (a) - Print the polynomial
    print("\nLagrange Interpolating Polynomial for Refractive Index")
    print("====================================================")   
    print("\nPolynomial can be written as:")
    print(p)
    
        # Verification at original data points
    print("\nVerification at given wavelengths:")
    print("Wavelength (Å)   Interpolated n    True n")
    print("-" * 45)
    
    for wl, n_true in data:
        n_interp = p(wl)
        print(f"{wl:12.0f}     {n_interp:10.5f}     {n_true:8.5f}")
        
# Part (b) - Root finding for n = 1.52
    
    TOL = 1e-10
    func_shifted = p - 1.52  # Shift the function down by 1.52 to find the root where p(wavelength) = 1.52
    root = Newton_Raphson(4861, func_shifted, TOL)
    print("\nFinding wavelength where n = 1.52 using Newton-Raphson method:")
    print(f'\nRoot = {root:.2f}')
    print(f"f({root:.2f}) = {p(root):.3f}")   # Verify that the root gives n ≈ 1.52 
    
    # Plot for visualization
    
    T_plot = np.linspace(3000, 7000, 500)
    rho_plot = p(T_plot)
    plt.figure(figsize=(10, 6))
    plt.plot(T_plot, rho_plot, 'b-', linewidth=2.5, label='Interpolantion')
    plt.plot(data[:, 0], data[:, 1], 'ro', markersize=10, label='Data Points')
    plt.plot(root, p(root), 'go', markersize=10, label=f'Wavelength: {root:.2f}')
    plt.xlabel('Wavelength', fontsize=12)
    plt.ylabel('Refractive Index', fontsize=12)
    plt.title('Part (b): Lagrange Interpolation', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=11)
    plt.tight_layout()
    plt.show()

    
    
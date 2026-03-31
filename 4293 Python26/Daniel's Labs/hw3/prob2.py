import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial.polynomial import Polynomial

# ==================== Vandermonde Interpolant ====================
def vandermonde(points):
    """Compute interpolating polynomial using Vandermonde matrix."""
    points = np.asarray(points, dtype=float)
    if points.ndim != 2 or points.shape[1] != 2:
        raise ValueError("points must be a 2D array of shape (n, 2)")
    
    x = points[:, 0]
    y = points[:, 1]
    
    V = np.vander(x, increasing=True)
    coeffs = np.linalg.solve(V, y)
    return Polynomial(coeffs)


# ==================== Lagrange Interpolant ====================
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


# ====================== TEST SCRIPT ======================

if __name__ == "__main__":
    print("=== Testing Lagrange vs Vandermonde Interpolation ===\n")
    
    # Choose a nice test case: f(x) = cos(2πx) with n=8 points
    n = 15
    def f(x):
        return np.cos(2 * np.pi * x)
    
    # Generate interpolation points
    x_points = np.linspace(0, 2, n)
    y_points = f(x_points)
    points = np.column_stack((x_points, y_points))
    
    # Compute both interpolants
    p_vand = vandermonde(points)
    p_lag  = lagrange(points)
    
    # Print coefficients for comparison
    print(f"Test case: f(x) = cos(2πx) with n = {n} equally spaced points")
    print(f"Vandermonde : {p_vand}")
    print(f"Lagrange : {p_lag}")
    
    x_fine = np.linspace(0, 2, 1000)
    
    # ====================== PLOT ======================
    plt.figure(figsize=(11, 7))
    
    # True function
    y_true = f(x_fine)
    plt.plot(x_fine, y_true, 'b-', linewidth=2.5, label='True function: cos(2πx)')
    
    # Vandermonde interpolant
    y_vand = p_vand(x_fine)
    plt.plot(x_fine, y_vand, 'r--', linewidth=2.0, label='Vandermonde Interpolation')
    
    # Lagrange interpolant
    y_lag = p_lag(x_fine)
    plt.plot(x_fine, y_lag, 'g-.', linewidth=2.0, label='Lagrange Interpolation')
    
    # Data points
    plt.plot(x_points, y_points, 'ko', markersize=4)
    
    plt.xlabel('x', fontsize=12)
    plt.ylabel('f(x)', fontsize=12)
    plt.title(f'Comparison: Lagrange vs Vandermonde Interpolation\n'
              f'f(x) = cos(2πx) with n = {n} equally spaced points', 
              fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=11)
    plt.ylim(-1.3, 1.3)
    plt.tight_layout()
    plt.show()

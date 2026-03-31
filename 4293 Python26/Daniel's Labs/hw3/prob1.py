import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial.polynomial import Polynomial

def vandermonde(points):
    """
    Compute the unique interpolating polynomial using the Vandermonde matrix.
    
    Parameters
    ----------
    points : array-like of shape (n, 2)
        Array of ordered pairs [x_i, y_i]
    
    Returns
    -------
    p : numpy.polynomial.polynomial.Polynomial
        The interpolating polynomial object
    """
    points = np.asarray(points, dtype=float)
    if points.ndim != 2 or points.shape[1] != 2:
        raise ValueError("points must be a 2D array with shape (n, 2)")
    
    x = points[:, 0]
    y = points[:, 1]
    
    # Build Vandermonde matrix (columns: 1, x, x², ..., x^{n-1})
    V = np.vander(x, increasing=True)
    
    # Solve V @ coeffs = y
    coeffs = np.linalg.solve(V, y)
    
    return Polynomial(coeffs)


# ====================== MAIN SCRIPT ======================

if __name__ == "__main__":
    print("=== Part (a): Air Density Interpolation ===\n")
    
    # Air density data: T (K) vs ρ (kg/m³)
    data = np.array([
        [300, 0.616],
        [400, 0.525],
        [500, 0.457]
    ])
    
    # Compute the interpolating polynomial
    p_density = vandermonde(data)
    
    print("Vandermonde Interpolating Polynomial for Density")
    print("===============================================")
    print(f"Coefficients : {p_density.coef}")
    print(f"Polynomial: {p_density}\n")
    
    # Evaluate at T = 350 K
    T_eval = 350
    rho_eval = p_density(T_eval)
    print(f"Interpolated density at T = {T_eval} K: ρ ≈ {rho_eval:.4f} kg/m³\n")
    
    # Plot for Part (a)
    T_plot = np.linspace(100, 700, 500)
    rho_plot = p_density(T_plot)
    
    plt.figure(figsize=(10, 6))
    plt.plot(T_plot, rho_plot, 'b-', linewidth=2.5, label='Interpolantion')
    plt.plot(data[:, 0], data[:, 1], 'ro', markersize=10, label='Data Points')
    plt.plot(T_eval, rho_eval, 'go', markersize=10, label=f'f(350) = {rho_eval:.3f}')
    
    for T, rho in data:
        plt.annotate(f'({T}, {rho:.3f})', xy=(T, rho), xytext=(8, 8), textcoords='offset points', fontsize=10)
        
    plt.annotate(f'({T_eval}, {rho_eval:.3f})', xy=(T_eval, rho_eval), xytext=(8, 8), textcoords='offset points', fontsize=10)
    plt.xlabel('Temperature T (C)', fontsize=12)
    plt.ylabel('Density ρ (kg/m³)', fontsize=12)
    plt.title('Part (a): Vandermonde Interpolation', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=11)
    plt.tight_layout()
    plt.show()
    
    # Part (b)
    print("\n=== Part (b): Cosine Interpolation with increasing n ===\n")
    
    # True function
    def f(x):
        return np.cos(2 * np.pi * x)
    
    # Values of n to test
    n_values = list(range(5, 101, 5))   # 5, 10, 15, ..., 100
    
    # Plot for each n 
    for n in n_values:
        # Generate n equally spaced points in [0, 2]
        x_points = np.linspace(0, 2, n)
        y_points = f(x_points)
        
        # Create points array for Vandermonde function
        points = np.column_stack((x_points, y_points))
        
        # Compute interpolating polynomial
        p = vandermonde(points)
        
        # Fine grid for smooth plotting
        x_fine = np.linspace(0, 2, 1000)
        y_true = f(x_fine)
        y_interp = p(x_fine)
        
        # Create the plot
        plt.figure(figsize=(10, 6))
        
        plt.plot(x_fine, y_true, 'b-', linewidth=2.0, label='True function: cos(2πx)')
        plt.plot(x_fine, y_interp, 'r--', linewidth=2.0, label='Interpolantion')
        plt.plot(x_points, y_points, 'ko', markersize=4)
        
        plt.xlabel('x', fontsize=12)
        plt.ylabel('f(x)', fontsize=12)
        plt.title(f'Part (b): Vandermonde Interpolation of cos(2πx) with n = {n} points', fontsize=14)
        plt.grid(True, alpha=0.3)
        plt.legend(fontsize=11)
        plt.ylim(-1.5, 1.5)
        plt.tight_layout()
        plt.show()

    print("All plots for Part (b) have been generated.")
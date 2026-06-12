import numpy as np
from scipy.integrate import quad

def f3(x):
    return np.exp(-3*x) * np.sin(4*x)

# (a) Composite Trapezoidal
def composite_trapezoidal(f, a, b, n):
    x = np.linspace(a, b, n+1)
    y = f(x)
    return (b-a)/n * (0.5*y[0] + np.sum(y[1:-1]) + 0.5*y[-1])

# (b) Composite 4-point Gaussian Quadrature
def composite_gauss4(f, a, b, n):
    # Standard 4-point nodes and weights for [-1, 1]
    nodes = np.array([-0.861136, -0.339981, 0.339981, 0.861136])
    weights = np.array([0.347855, 0.652145, 0.652145, 0.347855])
    
    total_area = 0
    h = (b - a) / n
    for i in range(n):
        ai = a + i*h
        bi = ai + h
        # Map nodes to [ai, bi]
        mapped_nodes = 0.5 * (bi - ai) * nodes + 0.5 * (bi + ai)
        total_area += 0.5 * (bi - ai) * np.sum(weights * f(mapped_nodes))
    return total_area

# (c) Adaptive Quadrature
result_adaptive, _ = quad(f3, 0, 3.7, epsabs=1e-6)

if __name__ == "__main__":
    a, b = 0, 3.7
    n = 10  # Number of subintervals for composite methods

    # Calculate integrals
    result_trapezoidal = composite_trapezoidal(f3, a, b, n)
    result_gauss4 = composite_gauss4(f3, a, b, n)

    print(f"Composite Trapezoidal: {result_trapezoidal:.6f}")
    print(f"Composite 4-point Gaussian Quadrature: {result_gauss4:.6f}")
    print(f"Adaptive Quadrature: {result_adaptive:.6f}")
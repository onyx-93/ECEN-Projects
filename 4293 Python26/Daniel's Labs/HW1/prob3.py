import numpy as np
import matplotlib.pyplot as plt


def f(x):
    """Original function f(x) = sin(√x) - x"""
    return np.sin(np.sqrt(x)) - x

def g(x):
    """Fixed-point form: x = g(x) = sin(√x)"""
    return np.sin(np.sqrt(x))


def fixed_point_iteration(x0, TOL):
    xi = x0 # initial guess   
    iterates = [xi] # store all x values
    
    i = 0
    # First iteration outside the loop to have valid diff
    x_new = g(xi) # initial value of g(x_0)
    diff = abs(x_new - xi)
    print(f"x{i+1} = {x_new:.4f}")
    
    iterates.append(x_new)
    
    while diff >= TOL:
        i += 1
        xi = x_new
        x_new = g(xi) #current value of g(x_i)
        diff = abs(x_new - xi)
        
        print(f"x{i+1} = {x_new:.4f}")
        iterates.append(x_new)
    
    if diff < TOL:
        print(f"\nConverged after {i+1} iterations")
    
    return x_new, iterates


if __name__ == "__main__":
    x0 = 0.5
    TOL = 1e-4
    
    final_x, iterates = fixed_point_iteration(x0, TOL)
    
    print(f"\nFinal approximation: {final_x:.4f}")
    
    # ─── Errors ────────────────────────────────────────────────
    true_root = 0.0
    true_errors = np.abs(iterates)   

    # Approximate relative error = consecutive diff / current value
    rel_errors = []
    for k in range(1, len(iterates)):
        delta = abs(iterates[k] - iterates[k-1])
        if abs(iterates[k]) > 1e-12:  # avoid division by very small numbers
            rel_errors.append(delta / abs(iterates[k]))
        else:
            rel_errors.append(np.nan)  # or very large number

    # ─── Plot ──────────────────────────────────────────────────
    plt.figure(figsize=(10, 6))
    
    # True error
    plt.plot(np.arange(len(iterates)), true_errors,
                 'o-', color='blue', label='True error |x_i|',
                 linewidth=1.5, markersize=6)
    
    # Approximate relative error
    plt.plot(np.arange(1, len(iterates)), rel_errors,
                 's-', color='red',
                 label=r'$\frac{|x_{i+1} - x_i|}{|x_{i+1}|}$  (approx. relative error)',
                 linewidth=1.5, markersize=6)
    
    plt.xlabel('Iteration count')
    plt.ylabel('Error')
    plt.title('Fixed-Point Iteration Convergence\n'
              r'$x = \sin(\sqrt{x})$, $x_0 = 0.5$, tol = $10^{-4}$')
    plt.grid(True, which="both", ls="--", alpha=0.7)
    plt.legend()
    plt.tight_layout()
    
    plt.savefig("problem3_errors.png", dpi=200, bbox_inches='tight')
    plt.show()
    
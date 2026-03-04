import numpy as np
import matplotlib.pyplot as plt
from numerical_methods import bisection_gen, regula_falsi_gen, newton_raphson_gen, fixed_point_gen, secant_gen, golden_section_search_gen, parabolic_interpol_gen

# ================================================
# FULL error_analysis.py (replace your stub)
# ================================================
# WHAT THIS DOES (exactly as the assignment requires):
# 1. Takes x_true, func=f(x), numerical_method=your *_gen function, *method_args (all args the generator needs, including TOL/epsilon_s and func/g_func).
# 2. Runs the generator, collects every xi it yields.
# 3. If it diverges (too many iterations or huge numbers) → raises clear error.
# 4. If plot_error=True → shows absolute error vs iteration on log-linear (semilogy) axes.
# 5. If plot_convergence=True → shows the (x_{i-1}, x_i) line plot with y=x reference line.
# 6. Returns order of convergence p estimated by linear regression (np.polyfit) on log|e_i| vs log|e_{i-1}|. 
#    This gives ~2 for Newton-Raphson, ~1 for bisection/secant/fixed-point, etc. — exactly what the assignment wants to test.


def error_analysis(x_true, func, numerical_method, *method_args,
                   plot_error=False, plot_convergence=False, max_iter=500):
    """
    Error analysis function per assignment guidelines.
    *method_args contains everything your generator needs (e.g. xl, xu, TOL, func).
    """
    iterates = []
    
    try:
        # Run the generator (this is the "callable generator function" part)
        for xi in numerical_method(*method_args):
            iterates.append(xi)
            
            if len(iterates) > max_iter:
                raise RuntimeError(f"Method did not converge after {max_iter} iterations — likely diverging.")
            if np.isnan(xi) or abs(xi) > 1e12:
                raise RuntimeError("Method diverging: values exploding.")
            
    except Exception as e:
        # Re-raise errors coming from the method itself (bad bracket, zero derivative, etc.)
        raise RuntimeError(f"Method failed: {e}") from e
    
    if len(iterates) < 2:
        raise ValueError("Not enough iterates produced.")
    
    # Final check against known true solution
    final_err = abs(iterates[-1] - x_true)
    if final_err > 1e-3:   # you can tighten this for your problems
        raise ValueError(f"Method did not reach the true solution (final error = {final_err:.2e}).")
    
    errors = np.abs(np.array(iterates) - x_true)
    
    # Plot 1: Absolute error on log-linear axes
    if plot_error:
        plt.figure(figsize=(9, 5))
        iters = np.arange(1, len(errors) + 1)
        plt.semilogy(iters, errors, 'b-o', linewidth=2, markersize=5)
        plt.xlabel('Iteration')
        plt.ylabel('|x_i - x_true| (log scale)')
        plt.title('Error Decay (log-linear)')
        plt.grid(True, which='both')
        plt.show()
    
    # Plot 2: Convergence plot (x_{i-1}, x_i)
    if plot_convergence:
        x_prev = np.array(iterates[:-1])
        x_curr = np.array(iterates[1:])
        plt.figure(figsize=(9, 5))
        plt.plot(x_prev, x_curr, 'g-o', label='Method path')
        # y = x reference line
        minv = min(x_prev.min(), x_curr.min())
        maxv = max(x_prev.max(), x_curr.max())
        plt.plot([minv, maxv], [minv, maxv], 'r--', label='y = x')
        plt.xlabel('$x_{i-1}$')
        plt.ylabel('$x_i$')
        plt.title('Convergence Plot')
        plt.legend()
        plt.grid(True)
        plt.show()
    
    # Order of convergence via linear regression on log-log errors
    order_est = None
    if len(errors) >= 4:
        log_e_prev = np.log(errors[:-1][2:])   # skip first few transient points
        log_e_curr = np.log(errors[1:][2:])
        slope, _ = np.polyfit(log_e_prev, log_e_curr, 1)
        order_est = slope
        print(f"Estimated order of convergence p ≈ {order_est:.3f}")
    else:
        print("Not enough iterates for order estimation.")
    
    return order_est


# Example test program (replace x_true with the known exact root/max for your problem)
if __name__ == "__main__":
   

    # Example 1: Root-finding with known root (use your own f and known x_true)
    def test_f(x):
        return x**2 - 2          # known root = sqrt(2) ≈ 1.41421356237
    
    x_true = np.sqrt(2)

    print("=== Newton-Raphson (should return ~2.0) ===")
    order = error_analysis(x_true, test_f, newton_raphson_gen,
                           1.0, 1e-10, test_f,          # args: x0, TOL, func
                           plot_error=True, plot_convergence=True)
    print("Newton order:", order)

    print("\n=== Bisection ===")
    order = error_analysis(x_true, test_f, bisection_gen,
                           1.0, 2.0, 1e-10, test_f,     # xl, xu, TOL, func
                           plot_error=True, plot_convergence=True)

    # Example 2: Fixed-point (pass g_func)
    def g(x):
        return np.sin(np.sqrt(x))   # example
    # x_true would be the fixed point of g
    # order = error_analysis(x_true, None, fixed_point_gen, 0.5, 1e-10, g, ...)

    # Example 3: Optimization (golden)
    # x_true = known maximizer of your f
    # order = error_analysis(x_true, f, golden_section_search_gen, -10, 10, 1e-6, f, ...)
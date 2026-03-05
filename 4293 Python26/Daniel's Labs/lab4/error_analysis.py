import numpy as np
import matplotlib.pyplot as plt
from numerical_methods import bisection_gen, regula_falsi_gen, newton_raphson_gen, fixed_point_gen, secant_gen, golden_section_search_gen, parabolic_interpol_gen

def error_analysis(x_true, func, numerical_method, *method_args,
                   plot_error=True, plot_convergence=True):
    """
    Generic error analysis tool for iterative numerical methods.

    Parameters
    ----------
    x_true : float
        Known exact solution.
    func : callable
        The function f(x).
    numerical_method : generator function
        Your iterative generator.
    *method_args :
        Arguments required by the numerical method.
    plot_error : bool
        If True → plots absolute error vs iteration (log scale).
    plot_convergence : bool
        If True → plots (x_{i-1}, x_i) convergence map.

    Returns
    -------
    order_est : float
        Estimated order of convergence.
    """

    iterates = []
    errors = []

    # Run generator
    try:
        # If fixed point method → do NOT pass func
        if numerical_method.__name__ == "fixed_point_gen":
            generator = numerical_method(*method_args)
        else:
            generator = numerical_method(*method_args, func)

        for x in generator:
            iterates.append(x)
            errors.append(abs(x - x_true))

            # Divergence detection
            if len(errors) > 5:
                if errors[-1] > errors[-2] > errors[-3]:
                    raise ValueError("Method appears to be diverging.")
                    #return None

    except Exception as e:
        print("Generator stopped:", e)
        plot_convergence = False
        plot_error = False
        return None

    iterates = np.array(iterates)
    errors = np.array(errors)

    # Remove zero errors (avoid log problems)
    mask = errors > 1e-14
    errors = errors[mask]

    if len(errors) < 3:
        print("Not enough data points to estimate convergence order.")
        return None

    # -----------------------------
    # Plot 1: Absolute Error
    # -----------------------------
    if plot_error:
        plt.figure()
        plt.semilogy(errors, marker='o')
        plt.xlabel("Iteration")
        plt.ylabel("Absolute Error")
        plt.title("Error vs Iteration (Log-Linear)")
        plt.grid(True)
        plt.show()

    # -----------------------------
    # Plot 2: Convergence Map
    # -----------------------------
    if plot_convergence and len(iterates) > 1:
        plt.figure()
        plt.plot(iterates[:-1], iterates[1:], marker='o')
        plt.xlabel("x_i")
        plt.ylabel("x_{i+1}")
        plt.title("Convergence Map")
        plt.grid(True)
        plt.show()

    # -----------------------------
    # Order of Convergence Estimate
    # -----------------------------
    # log(e_{n+1}) vs log(e_n)
    log_e_n = np.log(errors[:-1])
    log_e_np1 = np.log(errors[1:])

    slope, intercept = np.polyfit(log_e_n, log_e_np1, 1)

    order_est = slope

    print(f"Estimated order of convergence: {order_est:.2f}")

    return order_est

    # Test Function
    # -----------------------------------
def f(x):
    return x**2 - 2

    # Fixed point function
def g(x):
    return 0.5 * (x + 2/x)
# -----------------------------------
# Optimization Test Function
# -----------------------------------
def f_opt(x):
    """f(x) = -0.3x⁴ + 1.8x³ - 1.2x² + 2x"""
    return -0.3 * x**4 + 1.8 * x**3 - 1.2 * x**2 + 2 * x

# Example test program (replace x_true with the known exact root/max for your problem)
if __name__ == "__main__":
    
    x_true = np.sqrt(2)
    TOL = 1e-8

    print("\n==============================")
    print("Bisection Method")
    print("==============================")
    error_analysis(x_true, f, bisection_gen, 1, 2, TOL)

    print("\n==============================")
    print("Regula Falsi Method")
    print("==============================")
    error_analysis(x_true, f, regula_falsi_gen, 1, 2, TOL)

    print("\n==============================")
    print("Newton-Raphson Method")
    print("==============================")
    error_analysis(x_true, f, newton_raphson_gen, 1, TOL)

    print("\n==============================")
    print("Fixed-Point Iteration")
    print("==============================")
    error_analysis(x_true, f, fixed_point_gen, 1, TOL, g)

    print("\n==============================")
    print("Secant Method")
    print("==============================")
    error_analysis(x_true, f, secant_gen, 1, 2, TOL)
    
    # Optimization Methods (Maxima of function)
    maxima = 3
    print("\n==============================")
    print("Golden Section Search")
    print("==============================")
     # bracket around maximum
    error_analysis(maxima, f_opt, golden_section_search_gen, -2, 4, TOL)
    
    print("\n==============================")
    print("Parabolic Interpolation")
    print("==============================")
    # three points around max
    error_analysis(maxima, f_opt, parabolic_interpol_gen, -1, 2, 5)
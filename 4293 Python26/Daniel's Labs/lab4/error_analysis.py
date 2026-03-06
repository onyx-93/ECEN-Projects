import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from numerical_methods import Bisection, Regula_Falsi, Newton_Raphson, Fixed_Point, Secant, Golden_Section_Search, Parabolic_Interpol

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
        if numerical_method.__name__ == "Fixed_Point":
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


    # Order of Convergence Estimate
  
    # log(e_{n+1}) vs log(e_n)
    log_e_n = np.log(errors[:-1])
    log_e_np1 = np.log(errors[1:])

    slope, intercept = np.polyfit(log_e_n, log_e_np1, 1)

    order_est = slope

    #print(f"Estimated order of convergence: {order_est:.2f}")
    
    # Create ONE figure with TWO subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6), sharey=False)
    fig.suptitle(f"Numerical Method: {numerical_method.__name__}", fontsize=14, fontweight='bold')

    # Left: Error plot
    if plot_error:
        ax1.semilogy(errors, marker='o', color='darkblue', linewidth=1.2)
        ax1.set_xlabel("Iteration")
        ax1.set_ylabel("Absolute Error")
        ax1.set_title("Error vs Iteration (log scale)")
        ax1.grid(True, which="both", ls="--", alpha=0.7)

    # Right: Convergence map
    if plot_convergence and len(iterates) > 1:
        ax2.plot(iterates[:-1], iterates[1:], marker='o', color='darkgreen', linewidth=1.2)
        ax2.set_xlabel("$x_i$")
        ax2.set_ylabel("$x_{i+1}$")
        ax2.set_title("Convergence Map ($x_{i+1}$ vs $x_i$)")
        ax2.grid(True)
# === Add order value to legend using invisible proxy ===
        order_line = Line2D([], [], color='black', linestyle='none',  # completely invisible
                            label=f'Order of convergence: {order_est:.3f}')
        ax2.add_artist(order_line)

        ax2.legend(loc='best', fontsize=10, framealpha=0.9)

    # === Save the figure with meaningful name ===
    filename = f"plot_{numerical_method.__name__}.png"
    fig.savefig(filename, dpi=300, bbox_inches='tight') # Save the plot (useful for homework submission)
    print(f"Saved convergence plot for {numerical_method.__name__} as {filename}")
    
    # === Add instruction text at the bottom of the whole figure ===
    fig.text(0.5, 0.01,          # x=0.5 → center, y=0.01 → very bottom
         "Press Q for next set of graphs",
         ha='center', va='bottom',
         fontsize=14, color='black', style='italic')

    plt.tight_layout(rect=[0, 0.04, 1, 0.96])  # leave a bit more space at bottom 
    plt.show()

    return order_est

# Test Function
def f(x):
    return x**2 - 2

# Fixed point function
def g(x):
    return 0.5 * (x + 2/x)

# Optimization Test Function
def f_opt(x):
    """f(x) = -0x²/10 + 2sinx"""
    return -x**2/10 + 2*np.sin(x)

# Example test program (replace x_true with the known exact root/max for your problem)
if __name__ == "__main__":
    
    # Root Finding Methods
    x_true = np.sqrt(2)
    TOL = 1e-8
    error_analysis(x_true, f, Bisection, 1, 2, TOL)
    error_analysis(x_true, f, Regula_Falsi, 1, 2, TOL)
    error_analysis(x_true, f, Newton_Raphson, 1, TOL)
    error_analysis(x_true, f, Fixed_Point, 1, TOL, g)
    error_analysis(x_true, f, Secant, 1, 2, TOL)
    
    # Optimization Methods (Maxima of function)
    maxima = 1.42755
    TOL_opt = 1e-6
    error_analysis(maxima, f_opt, Golden_Section_Search, 0, 4, TOL_opt)
    error_analysis(maxima, f_opt, Parabolic_Interpol, 0, 1, 4, TOL_opt)
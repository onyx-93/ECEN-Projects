import numpy as np
import matplotlib.pyplot as plt


# Skeleton code:

class DivergenceError(Exception):
    pass

def error_analysis(
    x_true,
    f,
    method_gen,
    stop,
    *method_args,
    plot_error=True,
    plot_convergence=True
):
    # 1. Get the generator
    gen = method_gen(*method_args)

    xs = []
    errors = []

    # interpret `stop` as max_iter for simplicity
    max_iter = stop

    for k in range(max_iter):
        try:
            xk = next(gen)
        except StopIteration:
            break

        xs.append(xk)
        errors.append(abs(xk - x_true))

    xs = np.array(xs)
    errors = np.array(errors)

    # 2. Basic divergence / failure checks
    if len(xs) < 3:
        raise DivergenceError("Too few iterations to analyze convergence.")

    # Example: if error is not decreasing at all, or blows up
    if np.any(np.isnan(errors)) or np.any(np.isinf(errors)):
        raise DivergenceError("Method produced NaN or Inf; likely diverged.")

    # crude divergence: last error > first error by some factor
    if errors[-1] > 10 * errors[0]:
        raise DivergenceError("Error increased significantly; method appears to diverge.")

    # 3. Optional error vs iteration plot (semilogy)
    if plot_error:
        iters = np.arange(1, len(errors) + 1)
        plt.figure()
        plt.semilogy(iters, errors, marker='o')
        plt.xlabel("Iteration")
        plt.ylabel("Absolute error |x_n - x_true|")
        plt.title("Error vs iteration (semilogy)")
        plt.grid(True)
        plt.show()

    # 4. Convergence plot: (x_{n-1}, x_n)
    if plot_convergence:
        x_prev = xs[:-1]
        x_curr = xs[1:]

        plt.figure()
        plt.plot(x_prev, x_curr, 'o-')
        plt.xlabel("x_{n-1}")
        plt.ylabel("x_n")
        plt.title("Convergence plot")
        plt.grid(True)
        plt.show()

        # 5. Estimate "order of convergence" as slope of regression line
        # Fit x_curr ~ slope * x_prev + intercept
        coeffs = np.polyfit(x_prev, x_curr, 1)
        slope = coeffs[0]
    else:
        slope = np.nan

    return slope

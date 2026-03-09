import math
import matplotlib.pyplot as plt
import numpy as np

class DivergenceError(Exception):
    pass

def error_analysis(
    x_true,
    f,
    method_gen,
    max_iter,
    *method_args,
    tol=1e-10,
    plot_error=True,
    plot_convergence=True,
):
    gen = method_gen(*method_args)

    xs = []
    errors = []
    min_checks = 4
    growth_factor = 5

    converged = False

    for k in range(max_iter):
        try:
            xk = next(gen)
        except StopIteration:
            break

        xs.append(float(xk))
        ek = abs(xk - x_true)
        errors.append(float(ek))

        if not np.isfinite(ek):
            raise DivergenceError("Non-finite error encountered (NaN or Inf).")

        if ek < tol:
            converged = True
            break

    xs = np.array(xs, dtype=float)
    errors = np.array(errors, dtype=float)

    if len(xs) < 3:
        raise DivergenceError("Too few iterations to analyze convergence.")

    # simple divergence checks here...

    if len(errors) >= min_checks and errors[-1] > growth_factor * errors[0]:
        raise DivergenceError("Error increases significantly: method appears to diverge.")
    if not converged and errors[-1] > 0.9 * errors[0]:
        raise DivergenceError("Error did not decrease sufficiently; method may not converge.")
    # plotting block(s) here...

    # log–log regression for order p here...

    if len(errors) < 3:
        p_est = math.nan
    else:
        e_k = errors[:-1]
        e_k1 = errors[1:]

        mask = (e_k > 0) & (e_k1 > 0)
        e_k = e_k[mask]
        e_k1 = e_k1[mask]

        if len(e_k) < 2:
            p_est = math.nan
        else: 
            log_e_k = np.log(e_k)
            log_e_k1 = np.log(e_k1)
            coeffs = np.polyfit(log_e_k, log_e_k1, 1)
            p_est = coeffs[0]

    # if plot_error:
    #     iters = np.arrange(1, len(errors) + 1)
    #     plt.figure()
    #     plt.semilogy(iters, errors, marker='o')
    #     plt.xlabel("Iteration")
    #     plt.ylabel("Absolute error |x_k - x_true|")
    #     plt.title("Error vs Iteration in Semilogy")
    #     plt.grid(True, which="both")
    #     plt.tight_layout()
    #     plt.show()

    # if plot_convergence:
    #     x_prev = xs[:-1]
    #     x_curr = xs[1:]
    #     plt.figure()
    #     plt.plot(x_prev, x_curr, 'o-')
    #     x_min = min(x_prev.min(), x_curr.min())
    #     x_max = max(x_prev.max(), x_curr.max())
    #     plt.plot([x_min, x_max], [x_min, x_max], 'k--')
    #     plt.xlabel("x_{k-1}")
    #     plt.ylabel("x_k")
    #     plt.title("Convergence")
    #     plt.grid(True)
    #     plt.tight_layout()
    #     plt.show()

    if plot_error or plot_convergence:
        fig, axes = plt.subplots(1, 2, figsize=(10, 4))

        # Left: error vs iteration (semilogy)
        if plot_error:
            ax_err = axes[0]
            iters = np.arange(1, len(errors) + 1)
            ax_err.semilogy(iters, errors, marker='o')
            ax_err.set_xlabel("Iteration")
            ax_err.set_ylabel("|x_k - x_true|")
            ax_err.set_title("Error vs iteration")
            ax_err.grid(True, which="both")

        # Right: convergence plot (x_{k-1}, x_k)
        if plot_convergence:
            ax_conv = axes[1]
            x_prev = xs[:-1]
            x_curr = xs[1:]
            ax_conv.plot(x_prev, x_curr, 'o-')
            x_min = min(x_prev.min(), x_curr.min())
            x_max = max(x_prev.max(), x_curr.max())
            ax_conv.plot([x_min, x_max], [x_min, x_max], 'k--', linewidth=1)
            ax_conv.set_xlabel("x_{k-1}")
            ax_conv.set_ylabel("x_k")
            ax_conv.set_title("Convergence plot")
            ax_conv.grid(True)

        plt.tight_layout()
        plt.show()


        

    return p_est

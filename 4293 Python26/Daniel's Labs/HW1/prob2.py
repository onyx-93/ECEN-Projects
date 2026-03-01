import matplotlib.pyplot as plt
import numpy as np


def f(x):
    return np.cos(x) - x

def bisection_method(xl, xu, TOL, collect_history=False, history=None):
    if collect_history and history is None:
        history = []
    
    while abs(xu - xl) >= TOL:
        xm = (xl + xu) / 2
        
        if collect_history:
            history.append(xm)
        
        if f(xm) * f(xl) < 0: 
            xu = xm
        else: 
            xl = xm
    
    if collect_history:
        return xm, history
    return xm


def Regula_Falsi(xl, xu, TOL, collect_history=False, history=None):
    if collect_history and history is None:
        history = []
    
    while abs(xu - xl) >= TOL:
        xr = (f(xu) * xl - f(xl) * xu) / (f(xu) - f(xl))
        
        if collect_history:
            history.append(xr)
        
        if f(xr) * f(xl) < 0: 
            xl = xr
        else: 
            xu = xr
    
    if collect_history:
        return xr, history
    return xr


# ──────────────────────────────────────────────
# Plotting part — run both methods with history collection
# ──────────────────────────────────────────────
if __name__ == "__main__":
    xl_start = -1.0
    xu_start = 1.0
    TOL = 1e-4
    
    true_root = 0.7390  # Known root  rounded to 4 decimal places 

    # ─── Bisection ────────────────────────────────────────────────
    bis_history = []
    bis_root, _ = bisection_method(xl_start, xu_start, TOL,
                                   collect_history=True,
                                   history=bis_history)
    
    # ─── Regula Falsi ─────────────────────────────────────────────
    rf_history = []
    rf_root, _ = Regula_Falsi(xl_start, xu_start, TOL,
                              collect_history=True,
                              history=rf_history)

    # ─── Relative errors ──────────────────────────────────────────
    bis_iters = np.arange(1, len(bis_history) + 1)
    rf_iters  = np.arange(1, len(rf_history) + 1)

    bis_rel_error = np.abs(np.array(bis_history) - true_root) / np.abs(true_root)
    rf_rel_error  = np.abs(np.array(rf_history)  - true_root) / np.abs(true_root)

    # ─── Plot ─────────────────────────────────────────────────────
    plt.figure(figsize=(10, 6))
    plt.plot(bis_iters, bis_rel_error, 'o-', label='Bisection', linewidth=1.5, markersize=6)
    plt.plot(rf_iters,  rf_rel_error,  's-', label='Regula Falsi', linewidth=1.5, markersize=6)

    plt.xlabel('Iteration count')
    plt.ylabel('Relative error')
    plt.title('Convergence Comparison: Bisection vs Regula Falsi')
    plt.grid(True, which="both", ls="--", alpha=0.7)
    plt.legend()
    plt.tight_layout()

    plt.savefig("problem2_comparison.png", dpi=200, bbox_inches='tight')
    plt.show()

    # Summary
    print(f"Bisection final approx: {bis_root:.4f}  ({len(bis_history)} iterations)")
    print(f"Regula Falsi final approx: {rf_root:.4f}  ({len(rf_history)} iterations)")
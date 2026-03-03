import numpy as np
import matplotlib.pyplot as plt


# ──────────────────────────────────────────────
# Function definitions
# ──────────────────────────────────────────────
def f1(x):
    return -0.87*x**2 + 1.65*x +8.25 

def f2(x):
    return 0.7*x**3 - 3.7*x**2 + 6.31*x - 1.9

def d_fx(func, x, h=1e-8):
    """Approximate f'(x) using central finite difference"""
    return (func(x + h) - func(x - h)) / (2 * h)
    

def Newton_Raphson(x0, func, TOL):
    xi = x0 # initial guess
    function = func(xi) # initial function value at x0
    df = d_fx(func, xi) # initial derivative at x0
    iterates = [xi] # store all x values  
    i = 0
    
    # First iteration outside the loop to have valid diff
    x_new = xi - (function/df) # initial guess for Newton-Raphson
    diff = abs(x_new - xi)
   # print(f"x{i+1} = {x_new:.4f}")
    
    iterates.append(x_new)
    
    while diff >= TOL:
        i += 1
        xi = x_new
        function = func(xi)
        df = d_fx(func, xi)
        x_new = xi - (function/df) #current value of Newton-Raphson
        diff = abs(x_new - xi)
        
      #  print(f"x{i+1} = {x_new:.4f}")
        iterates.append(x_new)
    
    return x_new, iterates

# ──────────────────────────────────────────────
# Main execution + plotting
# ──────────────────────────────────────────────
if __name__ == "__main__":

    TOL = 1e-8
    # Roots of f1
    print("Finding roots of f₁(x) = −0.87x² + 1.65x + 8.25")
    root_pos1, iterates_pos = Newton_Raphson(1, f1, TOL)
    root_neg1, iterates_neg = Newton_Raphson(-1, f1, TOL)
    
    if root_pos1 == root_neg1:
        print(f"Final approximation: {root_pos1:.4f} (double root)")
    else:   
        print(f"Final approximation (positive root): {root_pos1:.4f}")
        print(f"Final approximation (negative root): {root_neg1:.4f}")
    
    # Roots of f2
    print("\nFinding roots of f₂(x) = 0.7x³ − 3.7x² + 6.31x − 1.9")
    root_pos2, iterates_pos = Newton_Raphson(1, f2, TOL)
    root_neg2, iterates_neg = Newton_Raphson(-1, f2, TOL)
    
    if root_pos2 == root_neg2:
        print(f"Final approximation: {root_pos2:.4f} (double root)")
    else:
        print(f"Final approximation (positive root): {root_pos2:.4f}")
        print(f"Final approximation (negative root): {root_neg2:.4f}")
        
    #Verify by plugging back into the functions
    print("\nVerification by plugging back into the functions:")
    print(f"f₁({root_pos1:.4f}) = {abs(f1(root_pos1)):.10f}")
    print(f"f₁({root_neg1:.4f}) = {abs(f1(root_neg1)):.10f}")
    print(f"f₂({root_pos2:.4f}) = {abs(f2(root_pos2)):.10f}")
    print(f"f₂({root_neg2:.4f}) = {abs(f2(root_neg2)):.10f}")

   
# Plotting the functions to visually estimate the roots
x = np.linspace(start=-3, stop=5, num=10000)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 8), sharey=False)

# Left: f1
ax1.plot(x, f1(x), color='blue', linewidth=2)
ax1.axhline(0, color='black', lw=1.3, ls='--')
ax1.axvline(0, color='black', lw=1.3, ls='--')
ax1.grid(True, alpha=0.5)
ax1.set_xlabel('x')
ax1.set_ylabel('f₁(x)')
ax1.set_title('f₁(x) = −0.87x² + 1.65x + 8.25')
ax1.set_ylim(-10, 12)

# Right: f2
ax2.plot(x, f2(x), color='red', linewidth=2)
ax2.axhline(0, color='black', lw=1.3, ls='--')
ax2.axvline(0, color='black', lw=1.3, ls='--')
ax2.grid(True, alpha=0.5)
ax2.set_xlabel('x')
ax2.set_title('f₂(x) = 0.7x³ − 3.7x² + 6.31x − 1.9')
ax2.set_ylim(-10, 10)

fig.suptitle('Graphical Estimation of Real Roots – Problem 4(a)', fontsize=16)
plt.tight_layout()
plt.savefig("problem4_plot.png", dpi=200, bbox_inches='tight')
plt.show()

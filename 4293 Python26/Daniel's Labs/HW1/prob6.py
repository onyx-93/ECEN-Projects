import numpy as np
import matplotlib.pyplot as plt


def f(x):
    """f(x) = -0.3x⁴ + 1.8x³ - 1.2x² + 2x"""
    return -0.3 * x**4 + 1.8 * x**3 - 1.2 * x**2 + 2 * x

def golden_section_search(xl, xu, epsilon_s):

    # Golden ratio constants
    phi = (1 + np.sqrt(5)) / 2          # ≈ 1.6180339887   
    r = 1 / phi                       # ≈ 0.6180339887  
    
    #iterates = []     # Storage for points evaluated
    #i = 0
    while xu - xl >= epsilon_s:  
        d = r * (xu - xl)         # Initial distance from boundaries
        x1 = xl + d
        x2 = xu - d
        f1 = f(x1)
        f2 = f(x2)
       # iterates.extend([x1, x2]) # Store points
        
        # Decide which subinterval to keep
        if f1 < f2:
            # Maximum is in left part → discard right of x1
            xu = x2
            x2 = x1
            x1 = xu   # New x1 based on updated xu

        else:
            # Maximum is in right part → discard left of x2
            xl = x1
            x1 = x2
            x2 = xl   # New x2 based on updated xl

        #i += 1
        #print('iteration =', i)
    
    x_max = (xl + xu) / 2
    return x_max#, f(x_max)#, iterates


def parabolic_interpol(x1, x2, x3):
    """
    Uses x1 < x2 < x3 naming exactly as in your original function.
    Performs n_iter iterations and returns the final best estimate (x2).
    """
    for i in range(5):
        f1 = f(x1)
        f2 = f(x2)
        f3 = f(x3)
        
        print( "\nx1 =", x1, "x2 =", x2, "x3 =", x3)

        # Parabolic interpolation formula for the vertex
        num = (x2 - x1)**2 * (f2 - f3) - (x2 - x3)**2 * (f2 - f1)
        den = (x2 - x1) * (f2 - f3) - (x2 - x3) * (f2 - f1)
            
        x4 = x2 - (0.5 * (num / den))    # new candidate point
        f4 = f(x4)
        
        # remove left side
        if x2 < x4 < x3:
            # yes
            if f4 < f2:
                #yes
                x1 = x2
                x2 = x4
            # no
            else:
                x3 = x4
                
        # remove right side
        elif x1 < x4 < x2:
            # yes
            if f4 < f2:
                #yes
                x3 = x2
                x2 = x4
            # no
            else:
                x1 = x4
                
        print(f"parabolic iteration {i+1}: x1 = {x1:.4f}, x2 = {x2:.4f}, x3 = {x3:.4f}, x4 = {x4:.4f}, \nf1 = {f1:.4f}, f2 = {f2:.4f}, f3 = {f3:.4f}, f4 = {f4:.4f}")

    return x2

if __name__ == "__main__":
    
    # Parameters for golden section search
    xl = -2
    xu = 4
    epsilon_s = 0.01          # 1% relative tolerance
      
    x_max = golden_section_search(xl, xu, epsilon_s)
    
    print(f"\nGolden section estimate of maximum at x = {x_max:.2f}")
    
    # parameter for parabolic interpolation
    x1 = 1.7
    x2 = 2
    x3 = 2.7
    x_max_parabolic = parabolic_interpol(x1, x2, x3)
    print(f"Parabolic interpolation estimate of maximum at x = {x_max_parabolic:.2f}")
    
    # plotting the function to visually estimate the root
    x_vals = np.linspace(-10, 10, 10000)
    plt.figure(figsize=(10, 6))
    plt.plot(x_vals, f(x_vals), label='f(x)', color='blue')
    plt.axhline(0, color='black', lw=1.3, ls='--')
    plt.axvline(0, color='black', lw=1.3, ls='--')
    plt.xlim(-5, 7.5)
    plt.ylim(-25, 30)
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title('Plot of f(x) to visually estimate the root')
    plt.grid()
    plt.show()
    
    

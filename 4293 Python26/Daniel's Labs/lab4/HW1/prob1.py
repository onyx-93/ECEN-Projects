import matplotlib.pyplot as plt
import numpy as np

#Porblem 1: Bisection method for root finding

# Step 1: define the range and number of points
theta = np.linspace(start=-1, stop=2, num=1000)

# Step 2: compute the function values
f_values = np.sin(theta) - theta**2

# Step 3: create the plot window / figure
plt.figure(figsize=(7, 7))               # optional: gives you control over size
plt.plot(theta, f_values)  # main plot command

# Step 4: make it nice and useful for finding roots
plt.axhline(y=0, color='black', linewidth=1.5)   # horizontal line at y=0
plt.axvline(x=0, color='black', linewidth=1.5)   # vertical line at θ=0
plt.grid(True)             # grid helps judge values
plt.xlabel('θ')
plt.ylabel('f(θ)')
plt.title('Plot of f(θ) = sin(θ) − θ²')
plt.ylim(-2, .4)          # set y-limits to focus on the area around the roots
plt.show()                 # actually display it


def f(x):
    return np.sin(x) - x**2

def bisection_method(xl, xu, TOL):
    i = 0
    while abs(xu - xl) >= TOL:
        xm = (xl + xu) / 2
        i += 1
        print('Iteration #', i)
        
        if f(xm) * f(xl) < 0: 
            xu = xm
        else: 
            xl = xm
    
    return xm

if __name__ == "__main__":
    xl = 0.5
    xu = 1.0
    TOL = 10**-8
    root = bisection_method(xl, xu, TOL)
    print(f"Approximate root: {root :.10f}")

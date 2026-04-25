def trapezoidal_rule(a, b, fa, fb):
    """Computes the integral using a single trapezoid."""
    return (b - a) * (fa + fb) / 2

# Calculations
i1 = trapezoidal_rule(0, 2, 0+2, 2+2) # f1(0)=2, f1(2)=4
i2 = trapezoidal_rule(0, 2, 0**3+1, 2**3+1) # f2(0)=1, f2(2)=9

print(f"Trapezoidal f1: {i1}") # Output: 6.0
print(f"Trapezoidal f2: {i2}") # Output: 10.0

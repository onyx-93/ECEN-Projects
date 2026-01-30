import math

print("This program solves a quadratic equation of the form:")
print("ax^2 + bx + c = 0\n")

# Get coefficients from the user
a = float(input("Enter coefficient a: "))
b = float(input("Enter coefficient b: "))
c = float(input("Enter coefficient c: "))

if a == 0:
    print('Coefficient a cannot be zero for a quadratic equation.')    
else:
    discriminant = b**2 - 4*a*c

    if discriminant < 0:
        print("No real roots exist.")

    elif discriminant == 0:
        x = -b / (2*a)
        print(f"One real root: x = {x:.5f}")

    else:
        x1 = (-b + math.sqrt(discriminant)) / (2*a)
        x2 = (-b - math.sqrt(discriminant)) / (2*a)
        print("The roots of the equation are:")
        print(f"x1 = {x1:.5f}")
        print(f"x2 = {x2:.5f}")
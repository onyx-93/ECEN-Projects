import numpy as np
import matplotlib.pyplot as plt

def y(t):
    return -156 - (1/8)*np.exp(t - 447) + 78*(np.exp(-t/500) + np.exp(t/500))

def second_derivative(f, h):
    def d2f(t):
        return (f(t + h) - 2*f(t) + f(t - h)) / h**2
    return d2f

h = 1e-2
y_dd = second_derivative(y, h)
t = np.linspace(0, 450, 500)

plt.figure()

plt.plot(t, y(t), label="Position y(t)")
plt.plot(t, y_dd(t), label="Acceleration y''(t)")

plt.xlabel("Time (s)")
plt.ylabel("Position (km)")
plt.title("Rocket Position and Acceleration")
plt.legend()
plt.grid()

plt.show()

t_vals = np.linspace(0, 450, 10000)
acc_vals = y_dd(t_vals)

max_acc = np.max(acc_vals) * 1000  # Convert from km/s^2 to m/s^2
t_max = t_vals[np.argmax(acc_vals)]


print(f"Maximum acceleration: {max_acc:.6f} m/s^2")
print(f"Occurs at t = {t_max:.6f} s")

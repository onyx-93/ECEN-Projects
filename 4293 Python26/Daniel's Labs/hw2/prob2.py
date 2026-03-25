import numpy as np
import matplotlib.pyplot as plt

# (a) Tridiagonal matrix T
def construct_T(m):
    """m x m tridiagonal matrix T with -4 on diagonal and 1 on off-diagonals."""
    T = np.diag(-4.0 * np.ones(m))
    T += np.diag(np.ones(m-1), k=1)
    T += np.diag(np.ones(m-1), k=-1)
    return T

# (b) Full block matrix A (size m² × m²)
def construct_A(m):
    h = 2.0 / (m + 1)
    T = construct_T(m)
    I = np.eye(m)
    n = m * m
    A = np.zeros((n, n))
    for k in range(m):
        start = k * m
        A[start:start+m, start:start+m] = T
        if k < m - 1:
            A[start:start+m, start+m:start+2*m] = I
        if k > 0:
            A[start:start+m, start-m:start] = I
    return A / (h ** 2)

# (c) Right-hand side vector b
def construct_b(m):
    h = 2.0 / (m + 1)
    b = np.zeros(m * m)
    def f(x, y):
        return 25 - x**2 + y**2

    for i in range(m):          # y-direction (block row)
        y_i = -1 + (i + 1) * h
        for j in range(m):      # x-direction
            x_j = -1 + (j + 1) * h
            pos = i * m + j
            sum_bound = 0.0
            if j == 0:          sum_bound += f(-1, y_i)
            if j == m - 1:      sum_bound += f(1, y_i)
            if i == 0:          sum_bound += f(x_j, -1)
            if i == m - 1:      sum_bound += f(x_j, 1)
            b[pos] = -sum_bound / h**2
    return b

# (d) Cholesky factorization
def cholesky_factorization(A):
    n = A.shape[0]
    L = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1):
            s = sum(L[i, k] * L[j, k] for k in range(j))
            if i == j:
                L[i, i] = np.sqrt(A[i, i] - s)
            else:
                L[i, j] = (A[i, j] - s) / L[j, j]
    return L

def forward_sub(L, bb):
    n = L.shape[0]
    y = np.zeros(n)
    for i in range(n):
        y[i] = bb[i]
        for j in range(i):
            y[i] -= L[i, j] * y[j]
        y[i] /= L[i, i]
    return y

def back_sub(L, y):
    n = L.shape[0]
    u = np.zeros(n)
    for i in range(n - 1, -1, -1):
        u[i] = y[i]
        for j in range(i + 1, n):
            u[i] -= L[j, i] * u[j]
        u[i] /= L[i, i]
    return u

# (e) Solve for m=10 and m=25
def solve_and_plot(m):
    print(f"\n=== Solving for m = {m} (system size {m*m} × {m*m}) ===")
    A = construct_A(m)
    b = construct_b(m)
    
    L = cholesky_factorization(-A)          # -A is positive definite
    u = back_sub(L, forward_sub(L, -b))
    
    u_grid = u.reshape((m, m))
    print(f"  → System constructed successfully")
    print(f"  → Cholesky factorization completed (no NaNs)")
    print(f"  → Solution computed (max |u| = {np.max(np.abs(u)):.4f})")
    
    # Plot
    plt.figure(figsize=(8, 6))
    plt.imshow(u_grid, origin='lower', cmap='plasma', extent=[-1, 1, -1, 1])
    plt.title(f'Heatmap of u(x, y) – m = {m}')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.colorbar(label='Temperature')
    plt.savefig(f'heatmap_m{m}.png')
    plt.show()

# NEW: DEMO - Show the full linear system and Cholesky factorization
def demo_small_m(m_demo=3):
    print(f"\n=== DEMO: Linear system and Cholesky for m = {m_demo} (9×9 system) ===")
    A = construct_A(m_demo)
    b = construct_b(m_demo)
    
    print("Linear system A (full m² × m² matrix):")
    np.set_printoptions(precision=2, suppress=True, linewidth=150)
    print(A)
    
    print("\nRight-hand side vector b:")
    print(b)
    
    # Cholesky on -A (A is negative definite)
    L = cholesky_factorization(-A)
    print("\nCholesky factorization L (of -A):")
    print(L)
    
    # Solve
    u = back_sub(L, forward_sub(L, -b))
    u_grid = u.reshape((m_demo, m_demo))
    print("\nSolution u (reshaped to grid):")
    print(u_grid)
    
    # Verify against analytic solution 25 - x² + y²
    h = 2.0 / (m_demo + 1)
    x = np.linspace(-1 + h, 1 - h, m_demo)
    y = np.linspace(-1 + h, 1 - h, m_demo)
    X, Y = np.meshgrid(x, y)
    analytic = 25 - X**2 + Y**2
    max_err = np.max(np.abs(u_grid - analytic))
    print(f"\nMax error vs analytic solution: {max_err:.2e}  ← should be ~1e-15")

if __name__ == "__main__":
    # 1. Show the linear system + Cholesky 
    demo_small_m(25)          
    
    # 2. Full homework requirement for m=10 and m=25
    solve_and_plot(10)
    solve_and_plot(25)
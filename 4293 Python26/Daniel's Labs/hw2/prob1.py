import numpy as np



def gaussian_elimination_partial_pivot(A, b):
    n = len(b)
    # Create the augmented matrix [A | b]
    Ab = np.hstack([A.astype(float), b.reshape(-1, 1).astype(float)])

    # --- Forward Elimination ---
    for i in range(n):
        # 1. Partial Pivoting: Find the row with the largest entry in current column
        pivot_row = np.argmax(np.abs(Ab[i:, i])) + i
        
        # Swap current row with the pivot row
        Ab[[i, pivot_row]] = Ab[[pivot_row, i]]
        
        if abs(Ab[i, i]) < 1e-12:
            raise ValueError("Matrix is singular or nearly singular!")

        # 2. Eliminate entries below the pivot
        for j in range(i + 1, n):
            factor = Ab[j, i] / Ab[i, i]
            Ab[j, i:] = Ab[j, i:] - factor * Ab[i, i:]

    # --- Back Substitution ---
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (Ab[i, -1] - np.dot(Ab[i, i+1:n], x[i+1:n])) / Ab[i, i]
        
    return x

if __name__ == "__main__":

    # 1. Input your circuit values
    R1 = 1000  # Ohms
    R2 = 1000
    R3 = 9000
    R4 = 10000
    v1 = 10.0   # Volts (Independent Source)

    # 2. Define the Conductance Matrix (A)
    # Row 0: KCL at node va
    # Row 1: KCL at node vb
    A = np.array([
        [-1/R1, (1/R1 + 1/R2 + 1/R4)],
        [(-1/R1 - 1/R3), 1/R1]
    ])

    # 3. Define the Constants Vector (b)
    # This represents known currents entering/leaving the nodes
    b = np.array([
        v1/R2 ,      # Node va has no source connected directly
        0   # Node vb receives current from v1 through R2
    ])

    # 4. Solve the linear system Ax = b
    # Result x will be [va, vb]
    try:
        x = np.linalg.solve(A, b)
        va, vb = x

        print(f"Results:")
        print("\nlinalg.solve approach")
        print("-"*30)
        print(f"Node Voltage va: {va:.2f} V")
        print(f"Node Voltage vb: {vb:.2f} V")
        print("-"*30)
    except np.linalg.LinAlgError:
        print("Error: The matrix is singular and cannot be solved (check your resistor values).")
    
    gaussian = gaussian_elimination_partial_pivot(A, b)
    
    print("\nGaussian Eliminatin approach")
    print("-"*30)
    print(f"Node Voltage va: {gaussian[0]:.2f} V")
    print(f"Node Voltage vb: {gaussian[1]:.2f} V")
    print("-"*30)
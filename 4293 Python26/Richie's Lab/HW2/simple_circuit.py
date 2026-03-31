# Ricardo Landeros Aranda | Oklahoma State University
# Spring 2026
# Homework 2 part 1 | ECEN 4293 Applied Numerical Methods in Python for Engineers
# This code was completed with the help of The following video: https://www.youtube.com/watch?v=DiZ0zSzZj1g
# As well as generative AI to check code syntax, logic, and results.
import numpy as np
import sys
import time


V1 = 10
R1 = 1e3
R2 = 1e3
R3 = 9e3
R4 = 10e3

A = np.array([[-(1/R3 + 1/R1), + 1/R1],
             [1/R1, -(1/R1 + 1/R4 + 1/R2)]], dtype=float)
b = np.array([0, -(V1/R2)], dtype=float)


def gauss_elimination(a_matrix, b_matrix):
     
    # Start with contingencies:

    if a_matrix.shape[0] != a_matrix.shape[1]:
        raise ValueError("\n\tSquare matrix not given, try a different matrix or check current matrix.\n")
        return
     
    # If our b matrix has more than 1 column we return

    if b_matrix.ndim != 1 or b_matrix.shape[0] != a_matrix.shape[0]:
        raise ValueError("\n\tConstant vector b size is incorrect or does not match matrix a given.\n")
        return
    
    # Initialization
    n = len(b_matrix)
    m = n - 1
    i = 0
    x = np.zeros(n)
    new_line = "\n"

    # Create augmented matrix through Numpy. Concatenating b matrix in the column direction into a matrix
    augmented_matrix = np.concatenate((a_matrix, b_matrix.reshape(-1, 1)), axis=1, dtype=float)
    print(f"\nThe initial augmented matrix is: {new_line}{augmented_matrix}\n")
    print("\nSolving for upper-triangular matrix:")

    while i < n:

        # Partial Pivoting step
        for p in range(i+1, n):
            if abs(augmented_matrix[i, i]) < abs(augmented_matrix[p, i]):
                augmented_matrix[[p, i]] = augmented_matrix[[i, p]]

        if augmented_matrix[i, i] == 0.0:
            raise ValueError("\n\tDivide by Zero error.\n")
            return
        
        for j in range(i+1, n):
            scaling_factor = augmented_matrix[j][i] / augmented_matrix[i][i]
            augmented_matrix[j] = augmented_matrix[j] - (scaling_factor * augmented_matrix[i])
            print(augmented_matrix) # See elimination

        i += 1
    # Back substitution to solve for x-matrix (unknown values)
    x[m] = augmented_matrix[m][n] / augmented_matrix[m][m]
    for k in range(n - 2, -1, -1):
        x[k] = augmented_matrix[k][n]


        for j in range(k + 1, n): # Here the video as an error since the it divided the terms and then subtracted
           x[k] -= augmented_matrix[k, j] * x[j] # The error was corrected now it subtracts the known terms in a_kj x_j
                                                 # From the right hand side and then it divides by the diagonal term.
        x[k] /= augmented_matrix[k, k]

    # Display solution
    print(f"\n\tSolution vector x for the matrices given: ")
    for answer in range(n):
        print(f"\n\tx{answer} is {x[answer]:.3f}")

gauss_elimination(A, b)

x = np.linalg.solve(A, b)

print(f"\n\tUsing np.linalg.solve(A, b), we get the following: {x}\n")
import os
from copy import deepcopy




def interior_point(C0, A0, b0, X0, eps0, alpha, max_iterations=1000):
    X = X0
    if any(x < 0 for x in X):
        return "The method is not applicable!", [], 0


    for _ in range(max_iterations):
        xi = X
        D = fill_D_matrix(X)
        A = fill_A_matrix(A0, b0)
        C = fill_C_matrix(C0, X)

        A_hat = multiply_two_matrices(A, D)
        C_hat = multiply_matrix_by_vector(D, C)

        P = calculate_P_matrix(A_hat)
        Cp = multiply_matrix_by_vector(P, C_hat)
        if not contains_negative(Cp):
            return "Solved!", X, sum(multiply_vector_by_vector(C0, X))
        v = abs(min(Cp))
        if v < eps0:
            return "Solved!", X, sum(multiply_vector_by_vector(C0, X))

        t1 = multiply_vector_by_number(Cp,alpha/v)
        X_hat = sum_vectors(identity_vector(len(Cp)), t1)

        X = multiply_matrix_by_vector(D, X_hat)
        if xi == X:
            return "Solved!", X, sum(multiply_vector_by_vector(C0, X))
    return "The problem does not have solution!", [], 0









def initial_solution_with_slack(A, b, X0):
    # Calculate initial slack variables
    slack_variables = [b[i] - sum(A[i][j] * X0[j] for j in range(len(X0))) for i in range(len(b))]
    # Combine initial solution and slack variables
    initial_solution = X0 + slack_variables
    return initial_solution


def fill_D_matrix(X0):
    D = []
    for i in range(len(X0)):
        D.append([0] * len(X0))
        D[i][i] = X0[i]
    return D

def fill_A_matrix(A, b):
    A = deepcopy(A)
    for i in range(len(A)):
        for j in range(len(A)):
            A[i].append(1 if i == j else 0)
    return A

def fill_C_matrix(C0, X):
    for i in range(len(C0), len(X)):
        C0.append(0)
    return C0

def multiply_two_matrices(A, B):
    # Get the number of rows and columns for the resulting matrix
    result_rows = len(A)
    result_cols = len(B[0])

    # Initialize the resulting matrix with zeros
    result = [[0 for _ in range(result_cols)] for _ in range(result_rows)]

    # Perform matrix multiplication
    for i in range(result_rows):
        for j in range(result_cols):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    return result

def multiply_matrix_by_vector(matrix, vector):
    # Get the number of rows in the matrix
    rows = len(matrix)

    # Initialize the resulting vector with zeros
    result = [0 for _ in range(rows)]

    # Perform matrix-vector multiplication
    for i in range(rows):
        for j in range(len(vector)):
            result[i] += matrix[i][j] * vector[j]

    return result

def multiply_vector_by_vector(vector1, vector2):
    # Ensure both vectors are of the same length
    if len(vector1) != len(vector2):
        raise ValueError("Vectors must be of the same length")

    # Initialize the resulting vector
    result = [0 for _ in range(len(vector1))]

    # Perform element-wise multiplication
    for i in range(len(vector1)):
        result[i] = vector1[i] * vector2[i]

    return result

def calculate_P_matrix(A):
    t1 = multiply_two_matrices(A, transpose_matrix(A))
    t2 = inverse_matrix(t1)
    t3 = multiply_two_matrices(transpose_matrix(A), t2)
    t4 = multiply_two_matrices(t3, A)
    t5 = subtract_matrices(identity_matrix(len(t4)), t4)
    return t5
def identity_matrix(dim):
    return [[1 if i == j else 0 for j in range(dim)] for i in range(dim)]

def transpose_matrix(matrix):
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]

def inverse_matrix(matrix):
    n = len(matrix)
    # Create an identity matrix of the same size
    identity = identity_matrix(n)

    # Append the identity matrix to the right of the original matrix
    for i in range(n):
        matrix[i] += identity[i]

    # Perform Gauss-Jordan elimination
    for i in range(n):
        # Make the diagonal contain all 1's
        factor = matrix[i][i]
        for j in range(2 * n):
            matrix[i][j] /= factor

        # Make the other elements in the current column 0
        for k in range(n):
            if k != i:
                factor = matrix[k][i]
                for j in range(2 * n):
                    matrix[k][j] -= factor * matrix[i][j]

    # Extract the inverse matrix from the augmented matrix
    inverse = [row[n:] for row in matrix]
    return inverse

def subtract_matrices(A, B):
    # Get the number of rows and columns
    rows = len(A)
    cols = len(A[0])

    # Initialize the resulting matrix with zeros
    result = [[0 for _ in range(cols)] for _ in range(rows)]

    # Perform matrix subtraction
    for i in range(rows):
        for j in range(cols):
            result[i][j] = A[i][j] - B[i][j]

    return result

def multiply_vector_by_number(vector, number):
    # Initialize the resulting vector
    result = [0 for _ in range(len(vector))]

    # Perform the multiplication
    for i in range(len(vector)):
        result[i] = vector[i] * number

    return result

def identity_vector(dim):
    return [1]*dim

def sum_vectors(vector1, vector2):
    # Initialize the resulting vector
    result = [0 for _ in range(len(vector1))]

    # Perform the subtraction
    for i in range(len(vector1)):
        result[i] = vector1[i] + vector2[i]

    return result

def contains_negative(A):
    for i in A:
        if i < 0:
            return True
    return False

for file in os.listdir('input'):
    with open(f'input/{file}', 'r') as f:
        strs = f.read().strip().split("\n")
        vars_number = int(strs[0])
        C0 = list(map(float, strs[1].strip().split()))
        equat_number = int(strs[2])
        A0 = []
        for i in range(3, equat_number+3):
            A0.append(list(map(float, strs[i].strip().split())))
        b0 = list(map(float, strs[equat_number+3].strip().split()))
        X0 = list(map(float, strs[-3].strip().split()))
        alpha = float(strs[-2])
        eps0 = float(strs[-1])
    with open(f'output/{file.strip(".txt")}.txt', 'w') as f:
        res = interior_point(C0, A0, b0, X0, eps0, alpha)
        if res[0] != "Solved!":
            f.write(res[0])
        else:
            x = list(map(lambda x: str(round(x, 5)), res[1]))
            f.write("Solution:\n")
            f.write(", ".join([f"x{i + 1} = {x[i]}" for i in range(len(x))]))
            f.write("\nz = ")
            f.write(str(round(res[2], 5)))
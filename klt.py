import numpy as np


def klt_transform(original_signal, siz):
    # Convert the 1D array to a 2D matrix of equal dimension
    matrix_2d = np.reshape(original_signal, (siz, siz))

    print("matrix", matrix_2d.shape)

    # Perform SVD
    U, Sigma, Vt = np.linalg.svd(matrix_2d)

    # Extract the eigenvectors from the U matrix
    eigenvectors = U
    print(eigenvectors, eigenvectors.shape)

    klt_matrix=eigenvectors.T@matrix_2d
    print(klt_matrix.ravel())

    return klt_matrix.ravel()

# Print the original matrix, singular values, and eigenvectors
'''print("Original Matrix:")
print(random_matrix)
print("\nSingular Values:")
print(Sigma)
print("\nEigenvectors:")
print(eigenvectors)

print("\nKLT Transform:")
print(klt_matrix)'''

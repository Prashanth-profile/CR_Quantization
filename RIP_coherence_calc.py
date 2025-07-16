import numpy as np
from itertools import combinations

def normalize_columns(A):
    """Normalize the columns of matrix A to have unit norm."""
    return A / np.linalg.norm(A, axis=0, keepdims=True)

def calculate_coherence(A):
    """
    Calculate the coherence of a matrix A.
    Coherence is the maximum absolute value of the inner products between distinct normalized columns.
    """
    # Normalize columns of A
    A_normalized = A / np.linalg.norm(A, axis=0)
    # Compute the Gram matrix
    G = np.dot(A_normalized.T, A_normalized)
    # Set diagonal elements to zero
    np.fill_diagonal(G, 0)
    # Return the maximum absolute value
    return np.max(np.abs(G))


def estimate_rip(A, k, num_samples=1000):
    """
    Estimate the Restricted Isometry Property (RIP) constant for a given matrix A.
    Args:
        A (numpy.ndarray): The sensing matrix (m x n).
        k (int): Sparsity level.
        num_samples (int): Number of random k-sparse vectors to test.
    Returns:
        float: Estimated RIP constant (delta_k).
    """
    m, n = A.shape
    delta_k = 0

    for _ in range(num_samples):
        # Randomly select k indices for the sparse vector
        indices = np.random.choice(n, k, replace=False)
        x = np.zeros(n)
        x[indices] = np.random.randn(k)  # Random non-zero entries

        # Compute Ax and the squared norms
        Ax = A @ x
        norm_Ax = np.linalg.norm(Ax) ** 2
        norm_x = np.linalg.norm(x) ** 2

        # Compute the distortion
        distortion = norm_Ax / norm_x
        delta_k = max(delta_k, abs(distortion - 1))

    return delta_k


# Example Usage
if __name__ == "__main__":
    # Create a random sensing matrix A
    m, n = 50, 100  # m rows, n columns
    A = np.random.randn(m, n)
    print("A", A)

    # Normalize the columns of A
    A = normalize_columns(A)
    print("Normalised A", A)

    # Calculate coherence
    coherence = calculate_coherence(A)
    print(f"Coherence: {coherence:.4f}")

    # Estimate RIP constant for sparsity level k
    k = 5  # Set sparsity level
    rip_constant = estimate_rip(A, k, num_samples=1000)
    print(f"Estimated RIP constant (delta_{k}): {rip_constant:.4f}")

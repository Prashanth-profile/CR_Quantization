import numpy as np
import cvxpy as cp
import matplotlib.pyplot as plt
import time

# Generate a sparse signal (only a few nonzero entries)
n = 1000  # Signal length
k = 50    # Sparsity (number of nonzero elements)
x = np.zeros(n)
#x[np.random.choice(n, k, replace=False)] = np.random.randn(k)*255
print("x", x)

# Convert the original signal to binary for BER calculation
x_binary = (x > 0).astype(int)  # Binary representation (e.g., threshold at zero)

# Create a random sensing matrix
m = 800  # Number of measurements (m << n)
Phi = np.random.randn(m, n) / np.sqrt(m)  # Random Gaussian matrix

# DFT representation of x

# Compute measurements
y = np.dot(Phi, x)

print("Size of approx matrix", y.size)

# Add Gaussian noise to the measurements
noise_std = 1  # Standard deviation of the noise
noise = np.random.normal(0, noise_std, size=y.shape)
y_noisy = y + noise
#y_noisy=y

# Measure computation time for pseudo-inverse reconstruction
start_time = time.time()
Phi_pseudo_inverse = np.linalg.pinv(Phi)  # Compute the pseudo-inverse
x_reconstructed_pseudo = np.dot(Phi_pseudo_inverse, y_noisy)  # Reconstruct the signal
print("Size of reconstructed signal CR", x_reconstructed_pseudo.size)
time_pseudo = time.time() - start_time

# Measure computation time for L1 optimization reconstruction
start_time = time.time()
z = cp.Variable(n)  # Reconstructed signal
objective = cp.Minimize(cp.norm1(z))  # Minimize L1-norm of z
constraints = [Phi @ z == y_noisy]  # Constraint with noisy measurements
problem = cp.Problem(objective, constraints)
problem.solve(solver=cp.SCS, verbose=False)  # Use the SCS solver
x_reconstructed_l1 = z.value  # Extract the reconstructed signal
print("size of reconstructed signal L1", x_reconstructed_l1.size)
time_l1 = time.time() - start_time

# Quantize both reconstructed signals to binary
x_reconstructed_pseudo_binary = (x_reconstructed_pseudo > 0).astype(int)
x_reconstructed_l1_binary = (x_reconstructed_l1 > 0).astype(int)

# Calculate BER for both methods
ber_pseudo = np.sum(x_binary != x_reconstructed_pseudo_binary) / len(x_binary)
ber_l1 = np.sum(x_binary != x_reconstructed_l1_binary) / len(x_binary)

# Calculate MSE for both methods
mse_pseudo = np.mean((x - x_reconstructed_pseudo) ** 2)
mse_l1 = np.mean((x - x_reconstructed_l1) ** 2)

# Display results
print(f"Pseudo-Inverse Reconstruction:")
print(f"  BER: {ber_pseudo:.4f}, MSE: {mse_pseudo:.4f}, Time: {time_pseudo:.4f} seconds")

print(f"L1 Optimization Reconstruction:")
print(f"  BER: {ber_l1:.4f}, MSE: {mse_l1:.4f}, Time: {time_l1:.4f} seconds")

# Plot the original signal and both reconstructions
plt.figure(figsize=(12, 9))

# Original signal
plt.subplot(3, 1, 1)
plt.stem(x, linefmt="b-", markerfmt="bo", basefmt="r-")
plt.title("Original Signal")
plt.xlabel("Index")
plt.ylabel("Amplitude")

# Pseudo-Inverse Reconstruction
plt.subplot(3, 1, 2)
plt.stem(x_reconstructed_pseudo, linefmt="g-", markerfmt="go", basefmt="r-")
plt.title("Reconstructed Signal using CR (Pseudo-Inverse)")
plt.xlabel("Index")
plt.ylabel("Amplitude")

# L1 Optimization Reconstruction
plt.subplot(3, 1, 3)
plt.stem(x_reconstructed_l1, linefmt="m-", markerfmt="mo", basefmt="r-")
plt.title("Reconstructed Signal (L1 Optimization)")
plt.xlabel("Index")
plt.ylabel("Amplitude")

plt.tight_layout()
plt.show()

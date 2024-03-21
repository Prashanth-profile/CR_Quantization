import numpy as np
import matplotlib.pyplot as plt
from skimage import exposure

def generate_non_uniform_signal(size):
    # Example of a non-uniformly distributed signal
    return np.concatenate((np.linspace(0, 1, size // 2), np.linspace(1, 0, size // 2)))

def add_unknown_noise(signal, noise_std_dev=0.1):
    noise = np.random.normal(0, noise_std_dev, len(signal))
    return signal + noise

# Parameters
signal_length = 100
noise_std_dev = 0.1

# Generate a non-uniform signal
original_signal = generate_non_uniform_signal(signal_length)

# Add unknown noise
noisy_signal = add_unknown_noise(original_signal, noise_std_dev=noise_std_dev)

# Apply histogram equalization
equalized_signal = exposure.equalize_hist(noisy_signal)

# Plot the results
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.plot(original_signal, label='Original Signal', linestyle='--', color='blue')
plt.plot(noisy_signal, label='Noisy Signal', marker='o', linestyle='None', color='red', alpha=0.7)
plt.title('Original and Noisy Signals')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(equalized_signal, label='Equalized Signal', color='green')
plt.title('Histogram Equalization for Uniformly Distributed Filtered Signal')
plt.legend()

plt.show()

import numpy as np
from scipy.fftpack import dct, idct
import matplotlib.pyplot as plt

def adaptive_dct_filter(input_signal, threshold_percentage=50):
    # Apply Discrete Cosine Transform (DCT)
    dct_coefficients = dct(input_signal, type=2)

    # Calculate adaptive threshold
    threshold = threshold_percentage / 100.0 * np.max(np.abs(dct_coefficients))

    # Modify coefficients using adaptive threshold
    dct_coefficients_filtered = dct_coefficients * (np.abs(dct_coefficients) > threshold)

    # Apply Inverse Discrete Cosine Transform (IDCT)
    filtered_signal = idct(dct_coefficients_filtered, type=2)

    return filtered_signal

# Example usage:
# Generate a sample signal
'''fs = 1000  # Sampling frequency
t = np.arange(0, 1, 1/fs)  # Time vector
f1, f2 = 5, 50  # Frequencies of the signal
input_signal = np.sin(2*np.pi*f1*t) + 0.5*np.sin(2*np.pi*f2*t)

# Apply DCT filtering
#filtered_signal = dct_filter(input_signal)

# Plot the original and filtered signals
plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.plot(t, input_signal, label='Original Signal')
plt.title('Original Signal')
plt.subplot(2, 1, 2)
plt.plot(t, filtered_signal, label='Filtered Signal')
plt.title('Filtered Signal')
plt.show()'''

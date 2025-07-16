import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

# Generate synthetic signal
Fs = 62  # Sampling frequency (Hz)
T = 1 / Fs  # Sampling interval
t_uniform = np.arange(0, 1, T)  # Uniform sampling times
print("Orig time indices", t_uniform, len(t_uniform))
f1, f2 = 10, 30  # Frequencies of the sinusoids (Hz)
signal = np.sin(2 * np.pi * f1 * t_uniform) + 0.5 * np.sin(2 * np.pi * f2 * t_uniform)

# Random sampling
np.random.seed(0)  # For reproducibility
t_random = t_uniform + np.random.uniform(-T / 2, T / 2, len(t_uniform))
t_random = np.sort(t_random)  # Ensure increasing time order
signal_random = np.interp(t_random, t_uniform, signal)  # Interpolate signal for random times

# Reduce the number of random samples
sample_fraction = 0.7  # Use 50% of the random samples
num_samples = int(len(t_random) * sample_fraction)
indices = np.sort(np.random.choice(len(t_random), num_samples, replace=False))
t_random_reduced = t_random[indices]
print("Randomized time indices", t_random_reduced, len(t_random_reduced))
signal_random_reduced = signal_random[indices]

# Interpolation onto uniform grid
signal_interpolated = np.interp(t_uniform, t_random_reduced, signal_random_reduced)
#print("interpolated", signal_interpolated, len(signal_interpolated))

# FFT for uniform sampling
fft_uniform = fft(signal)
freq_uniform = fftfreq(len(t_uniform), T)

# FFT for interpolated random sampling
fft_random = fft(signal_interpolated)

# Plot results
plt.figure(figsize=(12, 8))

# Original Signal
plt.subplot(3, 1, 1)
plt.plot(t_uniform, signal, label="Original Signal")
plt.scatter(t_uniform, signal, color="blue", label="Original Samples", s=10)
plt.scatter(t_random_reduced, signal_random_reduced, color="red", label="Reduced Random Samples", s=10)
plt.title("Original Signal and Reduced Random Samples")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.legend()

# FFT with uniform sampling
plt.subplot(3, 1, 2)
plt.stem(freq_uniform[:len(freq_uniform)//2], np.abs(fft_uniform[:len(freq_uniform)//2]), basefmt=" ", linefmt="C0-", markerfmt="C0o")
plt.title("FFT with Uniform Sampling")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Amplitude")

# FFT with reduced random sampling
plt.subplot(3, 1, 3)
plt.stem(freq_uniform[:len(freq_uniform)//2], np.abs(fft_random[:len(freq_uniform)//2]), basefmt=" ", linefmt="C1-", markerfmt="C1o")
plt.title("FFT with Reduced Random Sampling (Interpolated)")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Amplitude")

plt.tight_layout()
plt.show()

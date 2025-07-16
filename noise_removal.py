import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

'''# Generate a random variable with noise
x = [50.666, 48.335, 37.652, 40.685, 49.161, 55.556, 56.462, 66.53, 66.534, 79.038, 77.693, 77.901, 78.491, 91.122, 101.485, 104.146, 109.774, 99.834, 109.715, 82.134, 109.215, 107.394, 108.314, 103.003, 109.05, 104.564, 107.025, 110.0, 116.517, 123.881, 130.932, 135.712, 132.474, 132.148, 135.366, 139.558, 140.576, 142.728, 118.756, 117.384, 118.991, 149.788, 147.238, 317.632, 145.665, 53.621, 57.865, 75.079, 125.886, 123.332, 114.101, 117.856, 115.685, 314.21, 137.078, 133.558, 113.115, 130.133, 133.38, 127.788, 116.971, 113.828, 9.82, 129.071, 124.232, 121.441, 119.299, 109.535, 103.367, 108.401, 113.571, 102.452, 99.288, 89.503, 87.285, 74.247, 70.043, 67.837, 63.658, 60.987, 67.999, -0.0, 59.801, 72.219, 239.122, 230.003, 54.32, 48.0, 53.733, 11.039, 43.136, 37.005, 204.28, 211.465, 216.471, 217.0, 217.7, 220.399, 235.302, 282.927]
np.random.seed(0)
time = np.linspace(0, 10, 100)
#signal = np.sin(time) + np.random.normal(0, 0.2, size=100)'''


# Applying different noise removal methods

# Method 1: Averaging
def averagin(signal):
    averaged_signal = np.convolve(signal, np.ones(10) / 10, mode='same')

    return averaged_signal


# Method 2: Smoothing using moving average
def window_smoothening(signal, window_size):
    # window_size = 10
    smoothed_signal = np.convolve(signal, np.ones(window_size) / window_size, mode='same')
    return smoothed_signal


# Method 3: Gaussian filtering
def gaussian_filtering(signal, window):
    trunc=4
    sig=window/trunc
    from scipy.ndimage import gaussian_filter1d
    filtered_signal = gaussian_filter1d(signal, sigma=sig, truncate=trunc)

    return filtered_signal

def savgold_filter(signal, win_len):
    # Apply the Savitzky-Golay filter with a filter length of 1024
    from scipy.signal import savgol_filter
    filtered_y = savgol_filter(signal, window_length=win_len, polyorder=1)


    return filtered_y

def savgold_filter_ali(signal, win_len, ord):
    # Apply the Savitzky-Golay filter with a filter length of 1024
    from scipy.signal import savgol_filter
    filtered_y = savgol_filter(signal, window_length=win_len-1, polyorder=ord)


    return filtered_y

def butterworth_filter(signal_input):
    # Design a Butterworth filter
    order = 2  # filter order
    cutoff_frequency = 0.005  # cutoff frequency in Hz
    b, a = signal.butter(order, cutoff_frequency, 'low', analog=False, fs=0.1)

    # Apply the Butterworth filter
    filtered_signal = signal.filtfilt(b, a, signal_input)

    return filtered_signal

def chebyshev_filter(signal_input):
    # Design a Chebyshev Type I filter
    order=2
    ripple = 0.5  # maximum ripple in the passband in dB
    cutoff_frequency = 0.005  # cutoff frequency in Hz
    b, a = signal.cheby1(order, ripple, cutoff_frequency, 'low', analog=False, fs=0.1)

    # Apply the Chebyshev filter
    filtered_signal_cheby = signal.filtfilt(b, a, signal_input)

    return filtered_signal_cheby


x=[0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
print(gaussian_filtering(x, len(x)))
'''signal=x

# Plot the noisy signal
plt.figure(figsize=(10, 4))
plt.plot(time, signal, label='Noisy Signal')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.legend()
plt.title('Noisy Signal')
plt.show()
# Plot the original and denoised signals
plt.figure(figsize=(10, 12))

plt.subplot(4, 1, 1)
plt.plot(time, signal, label='Noisy Signal')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.legend()
plt.title('Noisy Signal')

averaged_signal = averagin(signal)
plt.subplot(4, 1, 2)
plt.plot(time, averaged_signal, label='Averaged Signal')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.legend()
plt.title('Averaged Signal')

smoothed_signal=window_smoothening(signal, 10)
plt.subplot(4, 1, 3)
plt.plot(time, smoothed_signal, label='Smoothed Signal')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.legend()
plt.title('Smoothed Signal')

filtered_signal=gaussian_filtering(signal)
plt.subplot(4, 1, 4)
plt.plot(time, filtered_signal, label='Filtered Signal')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.legend()
plt.title('Filtered Signal')

plt.tight_layout()
plt.show()'''

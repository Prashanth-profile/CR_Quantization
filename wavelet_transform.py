import numpy as np
import matplotlib.pyplot as plt
import pywt

def wavelet_transform_haar(random_signal, win):
    print(pywt.wavelist(kind='discrete'))
    wavelet = 'haar'  # You can choose other wavelets too
    #custom_wavelet = np.ones(1024) / 1024
    #custom_wavelet = pywt.Wavelet(custom_wavelet)
    #wavelet = custom_wavelet
    #level = pywt.dwt_max_level(len(random_signal), win)
    #print("Nr of useful levels", level)

    # Perform the DWT
    coeffs = pywt.dwt(random_signal, wavelet, mode='smooth')
    print("Coeffs", coeffs)

    #coeffs[-1] = np.zeros_like(coeffs[-1])
    #coeffs[-2] = np.zeros_like(coeffs[-2])

    # Apply a scaling filter to approximate coefficients
    filtered_coeffs = [coeffs[0]] + [np.zeros_like(c) for c in coeffs[1:]]
    reconstructed_signal = pywt.waverec(filtered_coeffs, wavelet, mode='smooth', axis=-1)

    #print("Filtered coeffs", filtered_coeffs)
    #reconstructed_signal = pywt.waverec(filtered_coeffs, wavelet)

    return reconstructed_signal

'''# Generate a random signal
np.random.seed(0)
signal_length = 512
random_signal = np.random.randn(signal_length)

# Choose a wavelet and level of decomposition
wavelet = 'haar'  # You can choose other wavelets too
level = 3

# Perform the DWT
coeffs = pywt.wavedec(random_signal, wavelet, level=level)

# Apply a scaling filter to approximate coefficients
filtered_coeffs = [coeffs[0]] + [np.zeros_like(c) for c in coeffs[1:]]
reconstructed_signal = pywt.waverec(filtered_coeffs, wavelet)

# Plot the original and filtered signals
plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.plot(random_signal, label='Original Signal')
plt.legend()
plt.title('Original Signal')

plt.subplot(2, 1, 2)
plt.plot(reconstructed_signal, label='Filtered Signal')
plt.legend()
plt.title('Filtered Signal')

plt.tight_layout()
plt.show()'''

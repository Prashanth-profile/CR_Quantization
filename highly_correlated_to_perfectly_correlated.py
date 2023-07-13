import pywt
import numpy as np


def wavelet_packet_denoise(signal, wavelet='db4', level=4, threshold='soft'):
    # Perform wavelet packet decomposition
    wp = pywt.WaveletPacket(data=signal, wavelet=wavelet, mode='symmetric', maxlevel=level)

    # Obtain the coefficients from the decomposition
    coefficients = wp.get_level(level, 'natural')

    # Apply thresholding to the coefficients
    coefficients_thresholded = pywt.threshold(coefficients.data, value=None, mode=threshold, substitute=0.0)

    # Reconstruct the denoised signal
    wp[level].data = coefficients_thresholded
    denoised_signal = wp.reconstruct(update=False)

    return denoised_signal


# Example usage
# Generate a noisy signal
np.random.seed(0)
signal = np.random.randn(1000) + 3.0  # Original signal with added Gaussian noise

# Denoise the signal using wavelet packet denoising
denoised_signal = wavelet_packet_denoise(signal, wavelet='db4', level=4, threshold='soft')

# Print the denoised signal
print(denoised_signal)

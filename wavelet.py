import pywt

# Define the input signal or image
input_data = [1, 2, 3, 4, 5, 6, 7, 8]

# Define the wavelet function
wavelet = 'sym2'  # Daubechies 4

# Perform wavelet transform
coeffs = pywt.wavedec(input_data, wavelet)
print("Coefficients", coeffs)

# Print the wavelet coefficients
print("Wavelet Coefficients:")
for i, coeff in enumerate(coeffs):
    print(f"Level {i + 1}: {coeff}")

# Perform inverse wavelet transform
reconstructed_data = pywt.waverec(coeffs, wavelet)

# Print the reconstructed data
print("\nReconstructed Data:")
print(reconstructed_data)

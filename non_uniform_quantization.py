import numpy as np
import matplotlib.pyplot as plt

def mu_law_companding(input_array, mu):
    compressed_array = np.sign(input_array) * (np.log(1 + mu * np.abs(input_array)) / np.log(1 + mu))
    quantized_array = ((compressed_array + 1) * 127.5).astype(np.uint8)
    scaled_array = quantized_array * 2
    #binary_array = np.unpackbits(quantized_array).reshape(-1, 8)
    return scaled_array

# Example usage

# Generate a random float array
float_array = np.random.rand(100) * 200 - 1

# Set the μ (mu) value for μ-law companding
mu = 255

# Perform μ-law companding and get the binary representation
binary_array = mu_law_companding(float_array, mu)

# Plotting the result and companding technique used
plt.figure(figsize=(10, 6))
plt.scatter(range(len(float_array)), float_array, color='b', label='Original')
#plt.scatter(range(len(float_array)), binary_array[:, 7], color='r', label='Companded')
plt.scatter(range(len(float_array)), binary_array, color='r', label='Companded')
plt.xlabel('Index')
plt.ylabel('Value')
plt.title('μ-law Companding (8-bit Binary)')
plt.legend()
plt.show()
import numpy as np

def normalize(vector):
    min_val = np.min(vector)
    max_val = np.max(vector)
    normalized_vector = (vector - min_val) / (max_val - min_val)
    return normalized_vector

def convert_to_binary(vector, threshold):
    binary_vector = np.where(vector >= threshold, 1, 0)
    return binary_vector

def adjust_correlation(vector1, vector2, target_correlation, threshold):
    correlation = np.corrcoef(vector1, vector2)[0, 1]
    iteration = 0
    while abs(correlation - target_correlation) > 0.01 and iteration < 100:
        if correlation < target_correlation:
            threshold += 0.01
        else:
            threshold -= 0.01
        binary_vector1 = convert_to_binary(vector1, threshold)
        binary_vector2 = convert_to_binary(vector2, threshold)
        correlation = np.corrcoef(binary_vector1, binary_vector2)[0, 1]
        iteration += 1
    return binary_vector1, binary_vector2

# Example usage

# Generate two correlated integer vectors
np.random.seed(0)
vector1 = np.random.randint(0, 100, size=100)
vector2 = 0.8 * vector1 + np.random.normal(0, 10, size=100)

# Normalize the integer vectors
normalized_vector1 = normalize(vector1)
normalized_vector2 = normalize(vector2)

# Set the desired correlation
target_correlation = 0.8

# Set the initial threshold value
initial_threshold = 0.5

# Convert to binary vectors and adjust correlation
binary_vector1, binary_vector2 = adjust_correlation(normalized_vector1, normalized_vector2, target_correlation, initial_threshold)

# Print the correlation between the binary vectors
binary_correlation = np.corrcoef(binary_vector1, binary_vector2)[0, 1]
print("Correlation between binary vectors:", binary_correlation)

# Print the binary vectors
print("Binary Vector 1:", binary_vector1)
print("Binary Vector 2:", binary_vector2)

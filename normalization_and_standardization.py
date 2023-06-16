import numpy as np

# Example vectors
vector_1 = np.array([5, 10, 15, 20, 25])
vector_2 = np.array([2, 4, 6, 8, 10])

# Min-Max Scaling (Normalization)
def min_max_scaling(vector):
    min_val = np.min(vector)
    max_val = np.max(vector)
    scaled_vector = (vector - min_val) / (max_val - min_val)
    return scaled_vector

vector_1_normalized = min_max_scaling(vector_1)
vector_2_normalized = min_max_scaling(vector_2)
print("Min-Max Scaling (Normalization):")
print("Vector 1 normalized:", vector_1_normalized)
print("Vector 2 normalized:", vector_2_normalized)

# Z-Score Normalization
def z_score_normalization(vector):
    mean_val = np.mean(vector)
    std_val = np.std(vector)
    normalized_vector = (vector - mean_val) / std_val
    return normalized_vector

vector_1_normalized = z_score_normalization(vector_1)
vector_2_normalized = z_score_normalization(vector_2)
print("\nZ-Score Normalization:")
print("Vector 1 normalized:", vector_1_normalized)
print("Vector 2 normalized:", vector_2_normalized)

# Mean Centering (Standardization)
def mean_centering(vector):
    mean_val = np.mean(vector)
    centered_vector = vector - mean_val
    return centered_vector

vector_1_centered = mean_centering(vector_1)
vector_2_centered = mean_centering(vector_2)
print("\nMean Centering (Standardization):")
print("Vector 1 centered:", vector_1_centered)
print("Vector 2 centered:", vector_2_centered)

# Variance Scaling (Standardization)
def variance_scaling(vector):
    std_val = np.std(vector)
    scaled_vector = vector / std_val
    return scaled_vector

vector_1_scaled = variance_scaling(vector_1)
vector_2_scaled = variance_scaling(vector_2)
print("\nVariance Scaling (Standardization):")
print("Vector 1 scaled:", vector_1_scaled)
print("Vector 2 scaled:", vector_2_scaled)

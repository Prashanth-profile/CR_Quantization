import numpy as np

def calculate_correlation(array1, array2):
    # Calculate the correlation coefficient between two arrays
    correlation_matrix = np.corrcoef(array1, array2)
    correlation_coefficient = correlation_matrix[0, 1]
    print(correlation_coefficient)
    return correlation_coefficient

reference_array = [1, 1, 1, 0, 1, 0]
array1 = [1, 0, 0, 0, 1, 0]
array2 = [1, 1, 1, 0, 0, 0]

correlation1 = calculate_correlation(reference_array, array1)
correlation2 = calculate_correlation(reference_array, array2)

if correlation1 > correlation2:
    print("Array 1 has the highest correlation.")
elif correlation1 < correlation2:
    print("Array 2 has the highest correlation.")
else:
    print("Both arrays have the same correlation.")

import numpy as np
from collections import Counter
import math


def calculate_entropy(arr):
    total_elements = len(arr)
    value_counts = Counter(arr)
    #print(value_counts)
    entropy = 0.0

    for value, count in value_counts.items():
        probability = count / total_elements
        entropy -= probability * math.log2(probability)

    return entropy


# Example integer array
integer_array = np.array([1, 2, 3, 4, 1, 2, 2, 3, 4, 4, 4])

# Calculate entropy
entropy = calculate_entropy(integer_array)
print("Entropy:", entropy)

import numpy as np

def convert_to_divisible_by_5(arr):
    int_array = np.round(arr / 5) * 5
    int_array = np.clip(int_array, 0, 255).astype(int)
    return int_array

# Example usage
float_array = np.array([12.3, 45.6, 78.9, 133.7])
int_array = convert_to_divisible_by_5(float_array)

print(int_array)


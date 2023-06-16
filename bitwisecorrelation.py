import numpy as np
import sinewave

def normalize_binary_array(binary_array):
    normalized_array = 2 * binary_array - 1
    return normalized_array

def calculate_correlation(array1, array2):
    if len(array1) != len(array2):
        raise ValueError("Array lengths must be equal")

    #normalized_array1 = normalize_binary_array(array1)
    #normalized_array2 = normalize_binary_array(array2)

    normalized_array1 = array1
    normalized_array2 = array2

    print("normalised array", normalized_array1.flatten())
    print("normalised array 2", normalized_array2.flatten())

    correlation = np.corrcoef(normalized_array1.flatten(), normalized_array2.flatten())
    print(correlation)
    return abs(correlation[0,1])

def calculate_correlation_array(input_array1, input_array2):
    correlation_array = []

    for i in range(2, len(input_array1) + 1):
        correlation = calculate_correlation(input_array1[0:i], input_array2[0:i])
        #print("correlation", correlation)
        correlation_array.append(correlation)

    return correlation_array

# Example usage:

def maincall(array1, array2, bitsize):

    binary_array1 = np.array([list(format(x, 'b').zfill(bitsize)) for x in array1], dtype=np.uint8)
    binary_array2 = np.array([list(format(x, 'b').zfill(bitsize)) for x in array2], dtype=np.uint8)

    # Print binary array
    print("SDR1",binary_array1)
    print("SDR2",binary_array2)

    # Calculate correlation array as a function of length of input arrays
    correlation_array = calculate_correlation_array(binary_array1, binary_array2)

    #print("Correlation array:", correlation_array)

    return correlation_array

def maincall_onebit(array1, array2, bitsize):

    binary_array1 = np.array([list(format(x, 'b').zfill(bitsize)) for x in array1], dtype=np.uint8)
    binary_array2 = np.array([list(format(x, 'b').zfill(bitsize)) for x in array2], dtype=np.uint8)

    # Print binary array
    print("SDR1 binary array",binary_array1.flatten())
    print("SDR2 binary array",binary_array2.flatten())

    # Calculate correlation array as a function of length of input arrays
    correlation_array = calculate_correlation_array(binary_array1.flatten(), binary_array2.flatten())

    print("Correlation array:", correlation_array, " of length ", len(correlation_array))

    return correlation_array

array1 = [255]
array2 = [134]

bitwisecorr=maincall_onebit(array1, array2, 8)
print(bitwisecorr)
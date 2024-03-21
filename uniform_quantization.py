import numpy as np
import math

def convert_to_divisible_by_5(arr):
    int_array = np.round(arr / 5) * 5
    int_array = np.clip(int_array, 0, 255).astype(int)
    return int_array

def uniform_quantization(complete_data, min, Quant_Range, max):
    result = np.zeros(len(complete_data))
    for i in range(len(complete_data)):
        result[i] = round(((complete_data[i] - min) * ((2 ** Quant_Range) - 1)) / (max - min))
    return result

def uniform_quantization_window(complete_data, Quant_Range, window_size, clipping):
    #normalised=np.zeros(len(complete_data))
    result = np.empty(len(complete_data))
    #print("Length of complete data", len(complete_data))
    #print("Window size", window_size)
    for i in range(0, len(complete_data), window_size):
        #print("i", i)
        if clipping==False:
            minimum_window = np.min(complete_data[i:i+window_size])
            maximum_window = np.max(complete_data[i:i+window_size])
        else:
            intervalsize = np.std(complete_data[i:i+window_size])

            minimum_window = np.min(complete_data[i:i+window_size]) + (intervalsize/(2**Quant_Range-1))
            maximum_window = np.max(complete_data[i:i+window_size]) - (intervalsize/(2**Quant_Range+1))

        #print("Max and min values are", maximum_window, minimum_window)

        #intervalsize=(maximum_window-minimum_window)/ (2 ** Quant_Range)


        #print("minimum", minimum_window, "maximum value", maximum_window, "at",np.argmax(complete_data[i:i+window_size]), " and ", np.argmin(complete_data[i:i+window_size]), "respectively")
        for j in range(0, window_size):
            #print("i+j", i+j)
            if minimum_window >= complete_data[i+j]:
                result[i+j] = 0

            elif maximum_window <= complete_data[i+j]:
                result[i+j] = (2**Quant_Range) - 1

            else:
                #normalised[i+j] = int(((complete_data[i+j] - minimum_window) * ((2 ** Quant_Range) - 1)) / (maximum_window - minimum_window))
                result[i+j]=np.round(((complete_data[i+j] - minimum_window) * ((2 ** Quant_Range) - 1)) / (maximum_window - minimum_window))
    return result


def uniform_quantization_window_clipped(complete_data, Quant_Range, window_size):
    #normalised=np.zeros(len(complete_data))
    result = np.zeros(len(complete_data))
    #print("Length of complete data", len(complete_data))
    #print("Window size", window_size)
    for i in range(0, len(complete_data), window_size):
        #print("i", i)
        minimum_window = np.min(complete_data[i:i+window_size])
        maximum_window = np.max(complete_data[i:i+window_size])

        #print("Max and min values are", maximum_window, minimum_window)

        intervalsize=(maximum_window-minimum_window)/ (2 ** Quant_Range)

        minimum_window=minimum_window+(intervalsize*4)
        maximum_window=maximum_window-(intervalsize*4)


        #print("minimum", minimum_window, "maximum value", maximum_window, "at",np.argmax(complete_data[i:i+window_size]), " and ", np.argmin(complete_data[i:i+window_size]), "respectively")
        for j in range(0, window_size):
            #print("i+j", i+j)
            if minimum_window >= complete_data[i+j]:
                result[i+j] = 0

            elif maximum_window <= complete_data[i+j]:
                result[i+j] = (2**Quant_Range) - 1

            else:
                #normalised[i+j] = int(((complete_data[i+j] - minimum_window) * ((2 ** Quant_Range) - 1)) / (maximum_window - minimum_window))
                result[i+j]=int(((complete_data[i+j] - minimum_window) * ((2 ** Quant_Range) - 1)) / (maximum_window - minimum_window))
    return result

def uniform_dynamic_quantization(arr, num_levels):
    quantized_arr = np.zeros_like(arr, dtype=int)

    # Calculate the range of values in the input array
    arr_min2 = np.min(arr)
    arr_max2 = np.max(arr)

    #arr_min2=arr_min+((arr_max-arr_min)/4)
    #arr_max2=arr_max-((arr_max-arr_min)/4)

    #arr_min2=arr_min-((arr_max-arr_min)/4)
    #arr_max2=arr_max+((arr_max-arr_min)/4)

    print("Min and max are", arr_min2, arr_max2)

    arr_range = arr_max2 - arr_min2

    # Calculate the interval size for each quantization level
    interval = arr_range / (num_levels)

    # Generate the ranges variable dynamically
    ranges = []
    for i in range(num_levels):
        lower = arr_min2 + (i * interval)
        upper = lower + interval
        ranges.append((lower, upper))
    #print("Range for", math.log2(num_levels)," quantization", ranges)

    # Perform quantization on each value in the array
    for i in range(len(arr)):
        if arr_min2 > arr[i]:
            quantized_arr[i] = 0

        elif arr_max2 < arr[i]:
            quantized_arr[i] = num_levels-1

        else:
            for j, (lower, upper) in enumerate(ranges):
                if lower <= arr[i] <= upper:
                    quantized_arr[i] = j
                    break
    #ranges.clear()

    #signed_quantized_array=

    return quantized_arr

############## Obtained from GPT
def quantize(arr1, arr2, num_bits):
    max_val = np.max(np.abs([arr1, arr2]))
    q_step = max_val / ((2**num_bits) - 1)
    arr1_quantized = np.round(arr1 / q_step) * q_step
    arr2_quantized = np.round(arr2 / q_step) * q_step
    return arr1_quantized, arr2_quantized


''''# Example usage
original_array = np.array([0, 2.6, 4.2, 6.8, 10])
num_levels = 4
quantized_array = uniform_dynamic_quantization(original_array, num_levels)

print("Original Array:", original_array)
print("Quantized Array:", quantized_array)'''

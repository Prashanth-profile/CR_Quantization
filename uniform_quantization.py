import numpy as np


def uniform_quantization(complete_data, min, Quant_Range, max):
    result = np.zeros(len(complete_data))
    for i in range(len(complete_data)):
        result[i] = round(((complete_data[i] - min) * ((2 ** Quant_Range) - 1)) / (max - min))
    return result

def uniform_quantization_window(complete_data, Quant_Range, window_size):
    result=np.zeros(len(complete_data))
    for i in range(0, len(complete_data)-window_size, window_size):
        #print("i", i)
        minimum_window=np.min(complete_data[i:i+window_size])
        maximum_window=np.max(complete_data[i:i+window_size])
        #print("minimum", minimum_window, "maximum value", maximum_window)
        for j in range(0, window_size):
            #print("i+j", i+j)
            result[i+j] = round(((complete_data[i+j] - minimum_window) * ((2 ** Quant_Range) - 1)) / (maximum_window - minimum_window))
    return result
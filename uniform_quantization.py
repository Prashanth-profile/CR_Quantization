import numpy as np


def uniform_quantization(complete_data, min, Quant_Range, max):
    result = np.zeros(len(complete_data))
    for i in range(len(complete_data)):
        result[i] = round(((complete_data[i] - min) * ((2 ** Quant_Range) - 1)) / (max - min))
    return result

import numpy as np
import math



def complete_correlation(min_length, data1, data2):
    number_of_samples = range(min_length)
    corr_coeff = np.zeros(len(number_of_samples))
    for i in range(1, len(number_of_samples) + 1):
        corr_coefficient = np.corrcoef(data1[0:i], data2[0:i])
        corr_coeff[i - 1] = abs(corr_coefficient[0, 1])

    #corr_coeff = np.nan_to_num(corr_coeff)
    return corr_coeff, number_of_samples

def correlation_non_overlapping_window(min_length, data1, data2, window_size):
    number_of_samples = range(0, min_length-window_size, window_size)
    corr_coeff = np.zeros(len(number_of_samples))
    for i in range(0, min_length-window_size, window_size):
        corr_coefficient = np.corrcoef(data1[i:i+window_size], data2[i:i+window_size])
        corr_coeff[int(i/window_size)] = abs(corr_coefficient[0, 1])
        #if np.isnan(abs(corr_coefficient[0, 1])):
            #print("data1 with Nan",data1[i:i+window_size])
            #print("data2 with Nan", data2[i:i + window_size])
    corr_coeff = np.nan_to_num(corr_coeff)
    return corr_coeff, number_of_samples


def correlation_overlapping_window(min_length, data1, data2, window_size):
    number_of_samples = range(0, min_length-window_size)
    corr_coeff = np.zeros(len(number_of_samples))
    for i in range(0, min_length-window_size):
        corr_coefficient = np.corrcoef(data1[i:i + window_size], data2[i:i + window_size])
        corr_coeff[i] = abs(corr_coefficient[0, 1])

    corr_coeff = np.nan_to_num(corr_coeff)
    return corr_coeff, number_of_samples
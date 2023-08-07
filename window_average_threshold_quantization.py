# Python program to calculate
# simple moving averages using pandas
import statistics

import numpy as np
import pandas as pd

#arr = [1, 2, 3, 7, 9]
#window_size=3

def window_average(arr, window_size):
    i = 0
    # Initialize an empty list to store moving averages
    moving_averages = []
    threshold_detection=[]
    # Loop through the array t o
    # consider every window of size window_size
    print("Original array is", arr)
    for i in range(0, len(arr), window_size):
        # Calculate the average of current window
        window_average = np.sum(arr[i:i + window_size]) / window_size
        threshold_detection_bit = [0 if x < window_average else 1 for x in arr[i:i + window_size]]
        #print("Result at index", i, "is ", threshold_detection_bit)
        # Store the average of current
        # window in moving average list
        moving_averages.append(window_average)
        threshold_detection.append(threshold_detection_bit)
        # Shift window to right by one position
        i += 1

    #print(moving_averages)
    '''print("After threshold detection", np.asarray(threshold_detection))

    l = []
    for item in threshold_detection:
        l.append(item[0])

    print("After concatenation", list(np.asarray(threshold_detection).flat))'''

    return list(np.asarray(threshold_detection).flat)

def window_average_meanmedian(arr, window_size, mean_medianbar):

    # Initialize an empty list to store moving averages
    binary_array = []
    for i in range(0, len(arr), window_size):
        # Calculate the average of current window
        if mean_medianbar==True:
            window_average = statistics.mean(arr[i:i + window_size])
        else:
            window_average = statistics.median(arr[i:i + window_size])

        for f, ind in zip(arr[i:i + window_size], range(0, len(arr[i:i + window_size]))) :
            if (f >= window_average):
                binary_array.append(1)
            elif f < window_average:
                binary_array.append(0)
    print("binary array", binary_array)
    return binary_array
    #return np.asarray(threshold_detection).flat

def float_to_binary_lossyquantization_onebit(float_array, min_length, window_size, mean_medianbar, alpha):

    binary_array = []
    #window_size=len(float_array)
    for i in range(0, len(float_array), window_size):
        # Calculate the average of current window
        if mean_medianbar==True:
            window_average = statistics.mean(float_array[i:i + window_size])
        else:
            window_average = statistics.median(float_array[i:i + window_size])
        window_var=np.var(float_array[i:i + window_size])

        threshold1=window_average+(window_var*alpha)
        threshold2=window_average-(window_var*alpha)
        print("threshold values are", threshold1, threshold2)
        for f, ind in zip(float_array[i:i + window_size], range(0, len(float_array[i:i + window_size]))) :
            if (f > threshold1):
                binary_array.append(1)
            elif f < threshold2:
                binary_array.append(0)
            else:
                continue
            if len(binary_array) == min_length:
                print("Number of trials", ind)
                break
    print("binary array", binary_array)
    return binary_array


'''arr=[1, 2, 3.5, 4, 5, 6]
print(np.var(arr), np.mean(arr))
print("array", arr)
arr2=float_to_binary_lossyquantization_onebit(arr, 6, False, 0.1)
print(arr2)'''
# Python program to calculate
# simple moving averages using pandas
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
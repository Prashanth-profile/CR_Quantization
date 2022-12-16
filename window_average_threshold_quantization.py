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
    while i < len(arr) - window_size + 1:
        # Calculate the average of current window
        window_average = round(np.sum(arr[
                                      i:i + window_size]) / window_size, 2)
        threshold_detection_bits = [0 if arr_ < window_average else 1 for arr_ in
                                         arr]
        # Store the average of current
        # window in moving average list
        moving_averages.append(window_average)
        threshold_detection.append(threshold_detection_bits)
        # Shift window to right by one position
        i += 1

    #print(moving_averages)
    #print(threshold_detection_bits)

    return threshold_detection_bits
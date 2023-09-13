import matplotlib.pyplot as plt2
import matplotlib.pyplot as plt3
import matplotlib.pyplot as plt4

import hash_encrypt
import normalization_and_standardization
import plot_RSSI
import plot_CFO
import plot_PO
import math
import numpy as np
import enum
import window_average_threshold_quantization
import stringify
import string_to_bytearray
import erroranderror_distribution
import uniform_quantization
import binary_count
import bintogrey
import matplotlib.pyplot as plt
import reedsolomon_codec
import sionna
import correlation_calculation
import plot_correlation
import lossy_quantization
import lossless_quantization
import plot_error
import bitwisecorrelation
import plot_histogram
import threading
import int2byte_conversion
import simple_plot
import linear_regression
import save_to_bin
import noise_removal
import kalman_filter
import confidence_interval
import calculate_entropy
import cr_rate_plot
import float_to_bytearray


class correlation_mode(enum.Enum):
    BITWISE_CORRELATION = False
    INTEGER_CORRELATION = False
    FIND_NUMBER_OF_ERRORS = True


min_length = 16384
# Choose index 12 for lower noise representation and 17 for higher noise and 16 for higher noise in gray code
ind = 0

# Set font size
fontsz = 40

#########This variable is the window size: This is used in both lossy and lossless quantization

#######################################CFO##############################################
# Read the text file
with open('C:/Users/prashanth/Desktop/CFO_SC_212_SDR1.txt', 'r') as fin:
    data_read_SDR1 = fin.read()
    last_char_SDR1 = data_read_SDR1[-1]
    if last_char_SDR1 == '\n':
        data_read_SDR1 = data_read_SDR1[:-1]
with open('C:/Users/prashanth/Desktop/CFO_SC_212_SDR2.txt', 'r') as fin:
    data_read_SDR2 = fin.read()
    last_char_SDR2 = data_read_SDR2[-1]
    if last_char_SDR2 == '\n':
        data_read_SDR2 = data_read_SDR2[:-1]

# average = mean(data)
# print(average)
data_read_SDR1 = data_read_SDR1.replace(',', '.')
data_read_SDR2 = data_read_SDR2.replace(',', '.')

# Split the data based on escape character \n
list_of_strings_SDR1 = data_read_SDR1.split('\n')
list_of_strings_SDR2 = data_read_SDR2.split('\n')

# Convert string to float
list_of_floats_SDR1 = [float(x) for x in list_of_strings_SDR1]
list_of_floats_SDR2 = [float(x) for x in list_of_strings_SDR2]
list_of_floats_SDR1 = list(map(lambda x: x * -1 if x < 0 else x, list_of_floats_SDR1))
list_of_floats_SDR2 = list(map(lambda x: x * -1 if x < 0 else x, list_of_floats_SDR2))

print("Raw sample values \n", list_of_floats_SDR1[ind:ind + min_length], " and \n",
      list_of_floats_SDR2[ind:ind + min_length])

min_l = 1024
window_size = 1024

#SDR1_1_norm = noise_removal.gaussian_filtering(list_of_floats_SDR1[ind:ind + min_l])
#SDR2_1_norm = noise_removal.gaussian_filtering(list_of_floats_SDR2[ind:ind + min_l])

SDR1_1_norm = list_of_floats_SDR1[ind:ind + min_l]
SDR2_1_norm = list_of_floats_SDR2[ind:ind + min_l]


SDR1_bytes=float_to_bytearray.float_array_to_64bitbyte_array(SDR1_1_norm)
SDR2_bytes=float_to_bytearray.float_array_to_64bitbyte_array(SDR2_1_norm)

num_errors, error_dist = erroranderror_distribution.error_distribution(SDR1_bytes, SDR2_bytes)

print("Size of array", len(SDR1_bytes)*8)
print("errors", num_errors)
print("Percentage error", num_errors/(len(SDR1_bytes)*8))
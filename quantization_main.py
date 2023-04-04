import matplotlib.pyplot as plt2
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

##### Make sure appropriate values is choosen. Setting more than one value to True can cause unexpected behavior
class Quantization(enum.Enum):
    UNIFORM= False
    WINDOW_THRESHOLD=False
    GREY_CODE=False
    #Set MEAN_MEDIANBAR to True of False only after setting LOSSY_QUANTIZATION or WINDOW_THRESHOLD to True. Otherwise, it really is not useful
    LOSSY_QUANTIZATION = True
    MEAN_MEDIANBAR=False

min_length=128
time=range(min_length)
ind=0

#########This variable is the window size over which mean/median is chosen
window_size=8

#######################################CFO##############################################
#Read the text file
with open('C:/Users/prashanth/Desktop/CFO_SC_212_SDR1.txt', 'r') as fin:
    data_read_SDR1 = fin.read()
    last_char_SDR1 = data_read_SDR1[-1]
    if last_char_SDR1 == '\n':
        print("last next line character detected in first sample file")
        data_read_SDR1 = data_read_SDR1[:-1]
with open('C:/Users/prashanth/Desktop/CFO_SC_212_SDR2.txt', 'r') as fin:
    data_read_SDR2 = fin.read()
    last_char_SDR2 = data_read_SDR2[-1]
    if last_char_SDR2 == '\n':
        print("last next line character detected in second sample file")
        data_read_SDR2 = data_read_SDR2[:-1]

# average = mean(data)
# print(average)
data_read_SDR1 = data_read_SDR1.replace(',', '.')
data_read_SDR2 = data_read_SDR2.replace(',', '.')

#Split the data based on escape character \n
list_of_strings_SDR1 = data_read_SDR1.split('\n')
list_of_strings_SDR2 = data_read_SDR2.split('\n')

#Convert string to float
list_of_floats_SDR1 = [float(x) for x in list_of_strings_SDR1]
list_of_floats_SDR2 = [float(x) for x in list_of_strings_SDR2]
list_of_floats_SDR1 = list(map(lambda x: x*-1 if x < 0 else x, list_of_floats_SDR1))
list_of_floats_SDR2 = list(map(lambda x: x*-1 if x < 0 else x, list_of_floats_SDR2))

print("Number of elements", len(list_of_floats_SDR1))

if Quantization.WINDOW_THRESHOLD.value==True:
    threshold_quantized_bits_SDR1 = window_average_threshold_quantization.window_average_meanmedian(list_of_floats_SDR1[0:min_length], window_size, Quantization.MEAN_MEDIANBAR.value)
    threshold_quantized_bits_SDR2 = window_average_threshold_quantization.window_average_meanmedian(list_of_floats_SDR2[0:min_length], window_size, Quantization.MEAN_MEDIANBAR.value)

    SDR1_string = stringify.stringify(threshold_quantized_bits_SDR1)
    SDR2_string = stringify.stringify(threshold_quantized_bits_SDR2)

    print("One bit non lossy quantization achieved using MEAN_MEDIANBAR", Quantization.MEAN_MEDIANBAR.value)

if Quantization.LOSSY_QUANTIZATION.value==True:
    alpha=0.001
    lossquantizedbits_SDR1 = window_average_threshold_quantization.float_to_binary_lossyquantization_onebit(list_of_floats_SDR1, window_size, Quantization.MEAN_MEDIANBAR.value, alpha)
    lossquantizedbits_SDR2 = window_average_threshold_quantization.float_to_binary_lossyquantization_onebit(list_of_floats_SDR2, window_size, Quantization.MEAN_MEDIANBAR.value, alpha)

    SDR1_string = stringify.stringify(lossquantizedbits_SDR1)
    SDR2_string = stringify.stringify(lossquantizedbits_SDR2)

print("SDR1 string", SDR1_string, "of length ", len(SDR1_string))


SDR1_bytes=string_to_bytearray.string_to_bytearray_conversion(8, SDR1_string[0:min_length])
SDR2_bytes=string_to_bytearray.string_to_bytearray_conversion(8, SDR2_string[0:min_length])

print("Result of Threshold detection based quantization for SDR1", SDR1_bytes)
print("Result of Threshold detection based quantization for SDR2", SDR2_bytes)

###################       BYTE ARRAY EXAMPLE   #################################
# Example usage:
arr1 = b'\x01\x02\x03\x04\x05'
arr2 = b'\x02\x02\x02\x04\x04'
###################       BYTE ARRAY EXAMPLE   #################################


num_errors, error_dist = erroranderror_distribution.error_distribution(SDR1_bytes, SDR2_bytes)
erroranderror_distribution.plot_error_distribution(error_dist)

# Print the total number of errors and distribution
print("Total number of errors: ", num_errors)
print("Distribution of errors: ", error_dist)
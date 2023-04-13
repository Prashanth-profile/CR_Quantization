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
import uniform_quantization
import binary_count
import bintogrey
import matplotlib.pyplot as plt
import reedsolomon_codec
import sionna

##### Make sure appropriate values is choosen. Setting more than one value to True can cause unexpected behavior
class Quantization(enum.Enum):
    UNIFORM= False
    WINDOW_THRESHOLD=True
    GREY_CODE=False
    #Set MEAN_MEDIANBAR to True of False only after setting LOSSY_QUANTIZATION or WINDOW_THRESHOLD to True. Otherwise, it really is not useful
    LOSSY_QUANTIZATION = False
    MEAN_MEDIANBAR=False

min_length=128
time=range(min_length)
ind=0

#########This variable is the window size: This is used in both lossy and lossless quantization
Quant_Range=2
window_size=8

#######################################CFO##############################################
#Read the text file
with open('C:/Users/prashanth/Desktop/RSSI_SC_212_SDR1.txt', 'r') as fin:
    data_read_SDR1 = fin.read()
    last_char_SDR1 = data_read_SDR1[-1]
    if last_char_SDR1 == '\n':
        print("last next line character detected in first sample file")
        data_read_SDR1 = data_read_SDR1[:-1]
with open('C:/Users/prashanth/Desktop/RSSI_SC_212_SDR2.txt', 'r') as fin:
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

    SDR1_bytes = string_to_bytearray.string_to_bytearray_conversion(8, SDR1_string[0:min_length])
    SDR2_bytes = string_to_bytearray.string_to_bytearray_conversion(8, SDR2_string[0:min_length])

    print("Results of byte array conversion for WTQ", SDR1_bytes, "of length", len(SDR1_bytes))
    print("Results of byte array conversion for WTQ", SDR2_bytes, "of length", len(SDR2_bytes))

    min_len = round(min_length / 8)
    num_errors, error_dist = erroranderror_distribution.error_distribution(SDR1_bytes[0:min_len], SDR2_bytes[0:min_len])

if Quantization.LOSSY_QUANTIZATION.value==True:
    alpha=0.001
    lossquantizedbits_SDR1 = window_average_threshold_quantization.float_to_binary_lossyquantization_onebit(list_of_floats_SDR1, window_size, Quantization.MEAN_MEDIANBAR.value, alpha)
    lossquantizedbits_SDR2 = window_average_threshold_quantization.float_to_binary_lossyquantization_onebit(list_of_floats_SDR2, window_size, Quantization.MEAN_MEDIANBAR.value, alpha)

    print("Length of lossy quantization", len(lossquantizedbits_SDR1), len(lossquantizedbits_SDR2))
    SDR1_string = stringify.stringify(lossquantizedbits_SDR1)
    SDR2_string = stringify.stringify(lossquantizedbits_SDR2)

    print("SDR1 string", SDR1_string, "of length ", len(SDR1_string))
    print("SDR1 string", SDR2_string, "of length ", len(SDR2_string))


    SDR1_bytes=string_to_bytearray.string_to_bytearray_conversion(8, SDR1_string)
    SDR2_bytes=string_to_bytearray.string_to_bytearray_conversion(8, SDR2_string)

    print("Results of byte array conversion for lossy quantization", SDR1_bytes, "of length", len(SDR1_bytes))
    print("Results of byte array conversion for lossy quantization", SDR2_bytes, "of length", len(SDR2_bytes))

    min_len = 16
    num_errors, error_dist = erroranderror_distribution.error_distribution(SDR1_bytes[0:min_len], SDR2_bytes[0:min_len])

###################       BYTE ARRAY EXAMPLE   #################################
# Example usage:
arr1 = b'\x01\x02\x03\x04\x05'
arr2 = b'\x02\x02\x02\x04\x04'
###################       BYTE ARRAY EXAMPLE   #################################

#num_errors, error_dist = erroranderror_distribution.error_distribution(SDR1_bytes, SDR2_bytes)
#erroranderror_distribution.plot_error_distribution(error_dist)

# Print the total number of errors and distribution
#print("Total number of errors: ", num_errors)
#print("Distribution of errors: ", error_dist)

if Quantization.UNIFORM.value==True:
    uniform_quantized_bytes_SDR1 = uniform_quantization.uniform_quantization_window(list_of_floats_SDR1, Quant_Range, window_size)
    uniform_quantized_bytes_SDR2 = uniform_quantization.uniform_quantization_window(list_of_floats_SDR2, Quant_Range, window_size)

    print("Result of uniform quantization in integer for SDR1", uniform_quantized_bytes_SDR1.astype(int), "with length ", len(uniform_quantized_bytes_SDR1.astype(int)))
    print("Result of uniform quantization in integer for SDR2", uniform_quantized_bytes_SDR2.astype(int), "with length ", len(uniform_quantized_bytes_SDR2.astype(int)))

    if Quantization.GREY_CODE.value==True:
        uniform_graycode_SDR1 = bintogrey.array_conversion_togray(uniform_quantized_bytes_SDR1.astype(int))
        uniform_graycode_SDR2 = bintogrey.array_conversion_togray(uniform_quantized_bytes_SDR2.astype(int))
        #uniform_graycode_SDR2=uniform_quantized_bytes_SDR2

        print("Result of gray code in integer for SDR1", uniform_graycode_SDR1.astype(int),
              "with length ", len(uniform_graycode_SDR1.astype(int)))
        print("Result of gray code in integer for SDR2", uniform_graycode_SDR2.astype(int),
              "with length ", len(uniform_graycode_SDR2.astype(int)))

        SDR1_bincount = binary_count.intarray2binarray(uniform_graycode_SDR1[0:round(min_length)].astype(int),Quant_Range)
        SDR2_bincount = binary_count.intarray2binarray(uniform_graycode_SDR2[0:round(min_length)].astype(int),Quant_Range)
    else:
        SDR1_bincount = binary_count.intarray2binarray(uniform_quantized_bytes_SDR1[0:round(min_length)].astype(int),Quant_Range)
        SDR2_bincount = binary_count.intarray2binarray(uniform_quantized_bytes_SDR2[0:round(min_length)].astype(int),Quant_Range)

    SDR1_string = stringify.stringify(SDR1_bincount.astype(int))
    SDR2_string = stringify.stringify(SDR2_bincount.astype(int))

    SDR1_bytes=string_to_bytearray.string_to_bytearray_conversion(8, SDR1_string)
    SDR2_bytes=string_to_bytearray.string_to_bytearray_conversion(8, SDR2_string)

    print("Results of byte array conversion for uniform quantization", SDR1_bytes, "of length", len(SDR1_bytes))
    print("Results of byte array conversion for uniform quantization", SDR2_bytes, "of length", len(SDR2_bytes))

    num_errors, error_dist = erroranderror_distribution.error_distribution(SDR1_bytes, SDR2_bytes)

#min_len=min(len(SDR1_bytes), len(SDR2_bytes))
#num_errors, error_dist = erroranderror_distribution.error_distribution(SDR1_bytes[0:min_len], SDR2_bytes[0:min_len])
print("Number of errors", num_errors)
erroranderror_distribution.plot_error_distribution(error_dist)
plt.plot(range(len(error_dist)), error_dist)
plt.xlabel('Bit Position')
plt.ylabel('Percentage of Errors')
plt.title('Cumulative Distribution of Errors')
plt.show()


'''################################# REED SOLOMON ENCODING AND DECODING ####################################

#Initialize RS encoding parameters in bytes
segment_size=8
parity_size=8
print("Length", len(SDR1_bytes), len(SDR2_bytes))
number_of_segments=round(len(SDR1_bytes)/(segment_size))
print("Number of segments", number_of_segments)

RS_encode = reedsolomon_codec.RS_encoding(SDR1_bytes, segment_size, parity_size, number_of_segments)

print("RS encoding ", RS_encode, " with parity byte length ", len(RS_encode))
# RS decoding for uniformly quantized binary codes and grey codes
RS_decode = reedsolomon_codec.RS_decoding(SDR2_bytes, RS_encode, segment_size, parity_size, number_of_segments)
print("decoded bytes  ", RS_decode, " with byte length ", len(RS_decode))
print("Decoding status without gray codes ", RS_decode == SDR1_bytes)
################################# REED SOLOMON ENCODING AND DECODING ENDS  ####################################'''

print("Total number of errors: ", num_errors)
print("Distribution of errors: ", error_dist)
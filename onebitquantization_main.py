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
import lossless_quantization
import lossy_quantization
import save_to_bin
import noise_removal
import hash_encrypt

##### Make sure appropriate values is choosen. Setting more than one value to True can cause unexpected behavior

min_length=1024
time=range(min_length)
ind=0

#########This variable is the window size: This is used in both lossy and lossless quantization
window_size=32

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

old_error_dist = []
remind=len(list_of_floats_SDR1)%min_length

####Lossy Quantization starts
#MEAN
alpha = 0.001
mean_medbar=True

#SDR1_1_norm=list_of_floats_SDR1
#SDR2_1_norm=list_of_floats_SDR2

SDR1_1_norm=noise_removal.gaussian_filtering(list_of_floats_SDR1)
SDR2_1_norm=noise_removal.gaussian_filtering(list_of_floats_SDR2)

#SDR1_1_norm=noise_removal.window_smoothening(list_of_floats_SDR1, 17)
#SDR2_1_norm=noise_removal.window_smoothening(list_of_floats_SDR2, 17)

SDR1_bytes, SDR2_bytes=lossy_quantization.lossy_quantization(SDR1_1_norm, SDR2_1_norm, min_length, window_size, True, alpha)
print("After 1 bit lossy mean ", SDR1_bytes, SDR2_bytes)
num_errors, error_dist = erroranderror_distribution.error_distribution(SDR1_bytes[0:64],SDR2_bytes[0:64])
print("Number of errors lossy mean", num_errors)
erroranderror_distribution.plot_error_distribution(error_dist)
#hash_encrypt.save_to_bin(SDR1_bytes)

print("Raw samples SDR1", SDR1_1_norm)
print("Raw samples SDR2", SDR2_1_norm)


#MEDIAN
SDR1_bytes, SDR2_bytes=lossy_quantization.lossy_quantization(SDR1_1_norm, SDR2_1_norm, min_length, window_size, False, alpha)
print("After 1 bit lossy median ", SDR1_bytes, SDR2_bytes)
num_errors, error_dist = erroranderror_distribution.error_distribution(SDR1_bytes[0:64],SDR2_bytes[0:64])
print("Number of errors lossy median", num_errors)
erroranderror_distribution.plot_error_distribution(error_dist)

######Lossy Quantization Ends

###### Lossless quantization starts
######1 bit Quanzization starts
#MEAN
SDR1_mebytes, SDR2_mebytes=lossless_quantization.one_bit_quantization(SDR1_1_norm, SDR2_1_norm, min_length, window_size, True)
print("After 1 bit mean ", SDR1_mebytes, SDR2_mebytes)
num_errors, error_dist = erroranderror_distribution.error_distribution(SDR1_mebytes[0:64],SDR2_mebytes[0:64])
print("Number of errors mean", num_errors)
erroranderror_distribution.plot_error_distribution(error_dist)
#hash_encrypt.save_to_bin(SDR1_mebytes)



#MEDIAN
SDR1_mdbytes, SDR2_mdbytes=lossless_quantization.one_bit_quantization(SDR1_1_norm, SDR2_1_norm, min_length, window_size, False)
print("After 1 bit median ", SDR1_mdbytes, SDR2_mdbytes)
num_errors, error_dist = erroranderror_distribution.error_distribution(SDR1_mdbytes[0:64],SDR2_mdbytes[0:64])
print("Number of errors median", num_errors)
erroranderror_distribution.plot_error_distribution(error_dist)

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import scipy.stats as stats
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import enum
import os
import binary_count
import bintogrey
import bitstringtobyte
import correlation_calculation
import plot_RSSI
import plot_commonbits
import plot_correlation
import reedsolomon_codec
import string_to_bytearray
import stringify
import uniform_quantization
import window_average_threshold_quantization
import math


def doubleto8bit(x, a):
    s = np.sign(x)
    x = abs(x)

    if x == a:
        return 0
    b = np.floor(np.log2(x) + 1) - 8
    m = s * round(x / 2 ** b)

    y = m * 2 ** b
    return y

class Quantization(enum.Enum):
    UNIFORM= True
    WINDOW_THRESHOLD=True

print("Uniform quantization flag set to ", Quantization.UNIFORM.value)


###############################          Reading from text file START        ########################################

#Read the text file
with open('C:/Users/prashanth/Desktop/CFO_SC_212_SDR1.txt', 'r+') as fin:
    data_read_SDR1 = fin.read()
    last_char_SDR1 = data_read_SDR1[-1]
    if last_char_SDR1 == '\n':
        print("last next line character detected in first sample file")
        data_read_SDR1 = data_read_SDR1[:-1]
with open('C:/Users/prashanth/Desktop/CFO_SC_212_SDR2.txt', 'r+') as fin:
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

###############################          Reading from text file END        ########################################

############################            Convert string to float START          #########################################
list_of_floats_SDR1 = [float(x) for x in list_of_strings_SDR1]
list_of_floats_SDR2 = [float(x) for x in list_of_strings_SDR2]
list_of_floats_SDR1 = list(map(lambda x: x*-1 if x < 0 else x, list_of_floats_SDR1))
list_of_floats_SDR2 = list(map(lambda x: x*-1 if x < 0 else x, list_of_floats_SDR2))


############################            Convert string to float END          #########################################
#print("RSSI values of SDR1", list_of_floats_SDR1)
#print("RSSI values of SDR2", list_of_floats_SDR2)

#######################        Calculate mean
average_SDR1 = np.mean(list_of_floats_SDR1)
average_SDR2 = np.mean(list_of_floats_SDR2)

########################       Calculate variance
var_SDR1 = np.var(list_of_floats_SDR1)
var_SDR2 = np.var(list_of_floats_SDR2)

########################       Calculate max and min
max_SDR1 = np.max(list_of_floats_SDR1)
min_SDR1 = np.min(list_of_floats_SDR1)
max_SDR2 = np.max(list_of_floats_SDR2)
min_SDR2 = np.min(list_of_floats_SDR2)

#######################       Specify quantization range (3bits, 4bits,.....)
Quant_Range=2

print("Max, Min, Avg, Var of SDR1", max_SDR1, min_SDR1, average_SDR1, var_SDR1)
print("Max, Min, Avg, Var of SDR2", max_SDR2, min_SDR2, average_SDR2, var_SDR2)

print("Number of entries from SDR1", len(list_of_floats_SDR1))
print("Number of entries from SDR2", len(list_of_floats_SDR2))

min_length = 128
window_size=8

##########################         Perform Uniform quantization
#uniform_quantized_bytes_SDR1 = uniform_quantization.uniform_quantization(list_of_floats_SDR1, min_SDR1, Quant_Range, max_SDR1)
#uniform_quantized_bytes_SDR2 = uniform_quantization.uniform_quantization(list_of_floats_SDR2, min_SDR2, Quant_Range, max_SDR2)
uniform_quantized_bytes_SDR1 = uniform_quantization.uniform_quantization_window(list_of_floats_SDR1, Quant_Range, window_size)
uniform_quantized_bytes_SDR2 = uniform_quantization.uniform_quantization_window(list_of_floats_SDR2, Quant_Range, window_size)
print("After quantization, sizes are", len(list_of_floats_SDR1), len(list_of_floats_SDR2))

if min_length%window_size!=0:
    print("Window size not matching length of the samples. Enter valid window_size")
    exit()

print("Min length = ", min_length)
time = list(range(min_length))

###########################         Quantization based on threshold detection
if Quantization.WINDOW_THRESHOLD.value==True:
    threshold_quantized_bits_SDR1 = window_average_threshold_quantization.window_average(list_of_floats_SDR1[0:min_length], window_size)
    threshold_quantized_bits_SDR2 = window_average_threshold_quantization.window_average(list_of_floats_SDR2[0:min_length], window_size)

###########################         Convert Quantized bits into string
if Quantization.WINDOW_THRESHOLD.value==True:
    SDR1_string = stringify.stringify(threshold_quantized_bits_SDR1)
    SDR2_string = stringify.stringify(threshold_quantized_bits_SDR2)

##########################          Bit string into byte array conversion
if Quantization.WINDOW_THRESHOLD.value==True:
    SDR1_bytes=string_to_bytearray.string_to_bytearray_conversion(8, SDR1_string)
    SDR2_bytes=string_to_bytearray.string_to_bytearray_conversion(8, SDR2_string)
    print("Result of Threshold detection based quantization for SDR1", list(SDR1_bytes))
    print("Result of Threshold detection based quantization for SDR2", list(SDR2_bytes))

fig, (ax1, ax5) = plt.subplots(2, 1)

###########################        Plot RSSI values
plot_RSSI.plot_RSSI(time, list_of_floats_SDR1[0:min_length], list_of_floats_SDR2[0:min_length], ax1)

if Quantization.UNIFORM.value==True:
    print("secret key of SDR1=", len(uniform_quantized_bytes_SDR1[0:min_length]))
    print("secret key of SDR2=", len(uniform_quantized_bytes_SDR2[0:min_length]))
    print("Result of uniform quantization for SDR1", uniform_quantized_bytes_SDR1.astype(int))
    print("Result of uniform quantization for SDR2", uniform_quantized_bytes_SDR2.astype(int))
if Quantization.WINDOW_THRESHOLD.value==True:
    print("Threshold Quantized bits of SDR1", threshold_quantized_bits_SDR1)
    print("Threshold Quantized bits of SDR2", threshold_quantized_bits_SDR2)

#################################      INTEGER BYTE TO GRAY CODE CONVERSION       ############################################
if Quantization.UNIFORM.value==True:
    uniform_graycode_SDR1 = bintogrey.array_conversion_togray(uniform_quantized_bytes_SDR1.astype(int))
    uniform_graycode_SDR2 = bintogrey.array_conversion_togray(uniform_quantized_bytes_SDR2.astype(int))
    print("Result of uniform quantization gray code conversion for SDR1", uniform_graycode_SDR1)
    print("Result of uniform quantization gray code conversion for SDR2", uniform_graycode_SDR2)

##############################     CORRELATION PLOT START       ##############################################################################

''''#fig, (ax2, ax3) = plt.subplots(2, 1)
#Calculate correlation coefficient of samples over certain range
if Quantization.UNIFORM.value==True:
    corr_coeff, number_of_samples=correlation_calculation.complete_correlation(min_length, uniform_quantized_bytes_SDR1.astype(int), uniform_quantized_bytes_SDR2.astype(int))
    plot_correlation.correlation_plot(number_of_samples, corr_coeff, ax2, 'r-')

if Quantization.WINDOW_THRESHOLD.value==True:
    corr_coeff, number_of_samples=correlation_calculation.complete_correlation(min_length, list(SDR1_bytes), list(SDR2_bytes))
    plot_correlation.correlation_plot(number_of_samples, corr_coeff, ax2, 'b-')'''

''''#Calculate correlation coefficient of samples over certain non overlapping window range
if Quantization.UNIFORM.value==True:
    corr_coeff, number_of_samples=correlation_calculation.correlation_non_overlapping_window(min_length, uniform_quantized_bytes_SDR1.astype(int), uniform_quantized_bytes_SDR2.astype(int), window_size)
    plot_correlation.correlation_plot(number_of_samples, corr_coeff, ax3, 'r-')
    print("Uniform", corr_coeff)

if Quantization.WINDOW_THRESHOLD.value==True:
    corr_coeff, number_of_samples=correlation_calculation.correlation_non_overlapping_window(min_length, list(SDR1_bytes), list(SDR2_bytes), window_size)
    plot_correlation.correlation_plot(number_of_samples, corr_coeff, ax3, 'b-')
    print("Threshold", corr_coeff)

#Calculate correlation coefficient of samples over certain overlapping window range
if Quantization.UNIFORM.value==True:
    corr_coeff, number_of_samples=correlation_calculation.correlation_overlapping_window(min_length, uniform_quantized_bytes_SDR1.astype(int), uniform_quantized_bytes_SDR2.astype(int), window_size)
    plot_correlation.correlation_plot(number_of_samples, corr_coeff, ax4, 'r-')

if Quantization.WINDOW_THRESHOLD.value==True:
    corr_coeff, number_of_samples=correlation_calculation.correlation_overlapping_window(min_length, list(SDR1_bytes), list(SDR2_bytes), window_size)
    plot_correlation.correlation_plot(number_of_samples, corr_coeff, ax4, 'b-')'''

##############################     CORRELATION PLOT END       ###################################################################################


#Binary Count
if Quantization.UNIFORM.value==True:
    min_length=128

    #Convert integer array into binary array (floating point)
    SDR1_bytes=string_to_bytearray.string_to_bytearray_conversion(8, SDR1_string)
    SDR2_bytes=string_to_bytearray.string_to_bytearray_conversion(8, SDR2_string)

    #Enable For binary codes
    SDR1_bincount=binary_count.intarray2binarray(uniform_quantized_bytes_SDR1[0:round(min_length)].astype(int), Quant_Range)
    SDR2_bincount=binary_count.intarray2binarray(uniform_quantized_bytes_SDR2[0:round(min_length)].astype(int), Quant_Range)

    #Generate an array of binary integer: 1 if SDR1_bincount(i)==SDR2_bincount(i) and 0 otherwise
    equal_bit_array_uniquant=binary_count.bitcount_window(SDR1_bincount, SDR2_bincount, 1)
    print("Number of bits equal to each other for uniform quantization are", sum(equal_bit_array_uniquant), "for ", min_length*Quant_Range, "total bits")
    print("Length of same bits array for uniform quantization", len(equal_bit_array_uniquant))
    sum_bitarray_uniquant = []
    #Sum over every window_size results. This will give us sum of common bits every window_size bits
    for i in range(0, len(equal_bit_array_uniquant), window_size):
        sum_perwindow = sum(equal_bit_array_uniquant[i:i + window_size])
        sum_bitarray_uniquant.append(sum_perwindow)
    plot_commonbits.plot_equalbits(sum_bitarray_uniquant, ax5, 'c-')

if Quantization.WINDOW_THRESHOLD.value==True:
    min_length = 128
    min_thresh_len=min_length
    #min_thresh_len=min(len(threshold_quantized_bits_SDR1[0:min_thresh_len]), len(threshold_quantized_bits_SDR2[0:min_thresh_len]))
    equal_bit_array_threshold=binary_count.bitcount_window(threshold_quantized_bits_SDR1[0:min_thresh_len], threshold_quantized_bits_SDR2[0:min_thresh_len], 1)
    print("equal", equal_bit_array_threshold, len(threshold_quantized_bits_SDR1[0:min_thresh_len]), len(threshold_quantized_bits_SDR2[0:min_thresh_len]), len(equal_bit_array_threshold), min_thresh_len)
    print("Number of bits equal to each other are for threshold based quantization", sum(equal_bit_array_threshold), "for ", min_thresh_len, "total bits")
    #print("Length of same bits array for threshold quantization", len(equal_bit_array_threshold))
    sum_bitarray_threshold=[]
    # Sum over every window_size results. This will give us sum of common bits every window_size bits
    for i in range(0, len(equal_bit_array_threshold), window_size):
        sum_perwindow=sum(equal_bit_array_threshold[i:i+window_size])
        sum_bitarray_threshold.append(sum_perwindow)
    plot_commonbits.plot_equalbits(sum_bitarray_threshold, ax5, 'm-')

'''ax5.vlines(number_of_samples ,0, corr_coeff, colors='k', linestyles='-', lw=6)
ax5=sns.histplot(corr_coeff,
                  bins=50,
                  kde=True,
                  color='red')'''
#ax5.set(xlabel='Normal Distribution', ylabel='Frequency')
#Reed Solomon encoding
#min_length=128


############################################      REED SOLOMON CODE START     ###################################################################
#Size of message length in bytes
segment_size=1

#Size of parity in bytes
parity_size=2

#Number of smaller message segments
number_of_segments=int((min_length*Quant_Range)/(8*segment_size))
print("Number of segments", number_of_segments)

# Enable For Gray Codes
SDR1_bincount = binary_count.intarray2binarray(uniform_graycode_SDR1[0:round(min_length)], Quant_Range)
SDR2_bincount = binary_count.intarray2binarray(uniform_graycode_SDR2[0:round(min_length)], Quant_Range)
print("SDR1 binary array", SDR1_bincount)
print("SDR2 binary array", SDR2_bincount)

greycode_stringSDR1 = stringify.stringify(SDR1_bincount.astype(int))
greycode_stringSDR2 = stringify.stringify(SDR2_bincount.astype(int))
print("greycode string for SDR1", greycode_stringSDR1)
print("greycode string for SDR2", greycode_stringSDR2)

greycodeSDR1_bytes = string_to_bytearray.string_to_bytearray_conversion(8, greycode_stringSDR1)
greycodeSDR2_bytes = string_to_bytearray.string_to_bytearray_conversion(8, greycode_stringSDR2)
print("greycode SDR1", greycodeSDR1_bytes, "of length", len(greycodeSDR1_bytes))
print("greycode SDR2", greycodeSDR2_bytes, "of length", len(greycodeSDR2_bytes))

#RS encoding for uniformly quantized binary codes
#RS_encode=reedsolomon_codec.RS_encoding(list(uniform_quantized_bytes_SDR1[0:min_length].astype(int)), segment_size, parity_size, number_of_segments)

#RS encoding for grey codes
RS_encode = reedsolomon_codec.RS_encoding(list(greycodeSDR1_bytes[0:segment_size*number_of_segments]), segment_size, parity_size, number_of_segments)
print("RS encoding", list(RS_encode), " with parity byte length ", len(RS_encode))

#RS decoding for uniformly quantized binary codes
#RS_decode=reedsolomon_codec.RS_decoding(list(uniform_quantized_bytes_SDR2[0:min_length].astype(int)), RS_encode, segment_size, parity_size, number_of_segments)

#RS decoding for grey codes
RS_decode = reedsolomon_codec.RS_decoding(list(greycodeSDR2_bytes[0:segment_size*number_of_segments]), RS_encode, segment_size, parity_size, number_of_segments)
print("decoded bytes", list(RS_decode), " with byte length ", len(RS_decode))

print("Original", list(greycodeSDR1_bytes))
print("Target", list(greycodeSDR2_bytes))

print("Decoding status ", RS_decode==list(greycodeSDR1_bytes[0:segment_size*number_of_segments]))

############################################      REED SOLOMON CODE END     ###################################################################

#print("Number of unequal elements", min_length-sum(binary_count.bitcount_window(list(uniform_quantized_bytes_SDR1[0:min_length].astype(int)), list(uniform_quantized_bytes_SDR2[0:min_length].astype(int)), 1)))
plt.tight_layout()
plt.show()

nzeros=np.count_nonzero(SDR1_bincount==0)
print("Number of 0's", nzeros, "and number of 1's", 128*(Quant_Range)-nzeros, "for SDR1, in UQ")
nzeros=np.count_nonzero(SDR2_bincount==0)
print("Number of 0's", nzeros, "and number of 1's", 128*(Quant_Range)-nzeros, "for SDR2, in UQ")

threshold_quantized_bits_SDR1=np.array(threshold_quantized_bits_SDR1)
nzeros=np.count_nonzero(threshold_quantized_bits_SDR1==0)
print("Number of 0's", nzeros, "and number of 1's", 128-nzeros, "for SDR1, in TQ")
threshold_quantized_bits_SDR2=np.array(threshold_quantized_bits_SDR2)
nzeros=np.count_nonzero(threshold_quantized_bits_SDR2==0)
print("Number of 0's", nzeros, "and number of 1's", 128-nzeros, "for SDR2, in TQ")



# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import scipy.stats as stats
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import enum

import binary_count
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

#Read the text file
with open('C:/Users/prashanth/Desktop/Logs SC 1302/Logs 2sec 2/CFO_SC_132_SDR1.txt', 'r') as fin:
    data_read_SDR1 = fin.read()
with open('C:/Users/prashanth/Desktop/Logs SC 1302/Logs 2sec 2/CFO_SC_132_SDR2.txt', 'r') as fin:
    data_read_SDR2 = fin.read()

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
list_of_floats_SDR1 = list(map(lambda x: x*-1 if x > 0 else x, list_of_floats_SDR1))
list_of_floats_SDR2 = list(map(lambda x: x*-1 if x > 0 else x, list_of_floats_SDR2))

#print("RSSI values of SDR1", list_of_floats_SDR1)
#print("RSSI values of SDR2", list_of_floats_SDR2)

#Calculate mean
average_SDR1 = np.mean(list_of_floats_SDR1)
average_SDR2 = np.mean(list_of_floats_SDR2)

#Calculate variance
var_SDR1 = np.var(list_of_floats_SDR1)
var_SDR2 = np.var(list_of_floats_SDR2)

#Calculate max and min
max_SDR1 = np.max(list_of_floats_SDR1)
min_SDR1 = np.min(list_of_floats_SDR1)
max_SDR2 = np.max(list_of_floats_SDR2)
min_SDR2 = np.min(list_of_floats_SDR2)

#Specify quantization range (3bits, 4bits,.....)
Quant_Range=2

print("Max, Min, Avg, Var of SDR1", max_SDR1, min_SDR1, average_SDR1, var_SDR1)
print("Max, Min, Avg, Var of SDR2", max_SDR2, min_SDR2, average_SDR2, var_SDR2)

print("Number of entries from SDR1", len(list_of_floats_SDR1))
print("Number of entries from SDR2", len(list_of_floats_SDR2))

min_length = 128
window_size=8

#Perform Uniform quantization
#uniform_quantized_bits_SDR1 = uniform_quantization.uniform_quantization(list_of_floats_SDR1, min_SDR1, Quant_Range, max_SDR1)
#uniform_quantized_bits_SDR2 = uniform_quantization.uniform_quantization(list_of_floats_SDR2, min_SDR2, Quant_Range, max_SDR2)
uniform_quantized_bits_SDR1 = uniform_quantization.uniform_quantization_window(list_of_floats_SDR1, Quant_Range, window_size)
uniform_quantized_bits_SDR2 = uniform_quantization.uniform_quantization_window(list_of_floats_SDR2, Quant_Range, window_size)
print("After quantization, sizes are", len(list_of_floats_SDR1), len(list_of_floats_SDR2))

#quantized_bits_SDR1[np.where(quantized_bits_SDR1==0)] =1
#quantized_bits_SDR2[np.where(quantized_bits_SDR2==0)] =1
#Number of samples to work with
#min_length = min(len(list_of_floats_SDR1), len(list_of_floats_SDR2))

if min_length%window_size!=0:
    print("Window size not matching length of the samples. Enter valid window_size")
    exit()

print("Min length = ", min_length)
time = list(range(min_length))

#Quantization based on threshold detection
#threshold_quantized_bits_SDR1=[0 if list_of_floats_SDR1_ < average_SDR1 else 1 for list_of_floats_SDR1_ in list_of_floats_SDR1]
#threshold_quantized_bits_SDR2=[0 if list_of_floats_SDR2_ < average_SDR2 else 1 for list_of_floats_SDR2_ in list_of_floats_SDR2]
if Quantization.WINDOW_THRESHOLD.value==True:
    threshold_quantized_bits_SDR1 = window_average_threshold_quantization.window_average(list_of_floats_SDR1[0:min_length], window_size)
    threshold_quantized_bits_SDR2 = window_average_threshold_quantization.window_average(list_of_floats_SDR2[0:min_length], window_size)

#Convert Quantized bits into string
if Quantization.WINDOW_THRESHOLD.value==True:
    SDR1_string = stringify.stringify(threshold_quantized_bits_SDR1)
    SDR2_string = stringify.stringify(threshold_quantized_bits_SDR2)

#Bit string into byte array conversion
#SDR1_bytes=bitstringtobyte.bitstring_to_bytes(SDR1_string, Quant_Range)
#SDR2_bytes=bitstringtobyte.bitstring_to_bytes(SDR2_string, Quant_Range)
if Quantization.WINDOW_THRESHOLD.value==True:
    SDR1_bytes=string_to_bytearray.string_to_bytearray_conversion(Quant_Range, SDR1_string)
    SDR2_bytes=string_to_bytearray.string_to_bytearray_conversion(Quant_Range, SDR2_string)

fig, (ax1, ax4, ax5) = plt.subplots(3, 1)

#Plot RSSI values
plot_RSSI.plot_RSSI(time, list_of_floats_SDR1[0:min_length], list_of_floats_SDR2[0:min_length], ax1)

if Quantization.UNIFORM.value==True:
    print("secret key of SDR1=", len(uniform_quantized_bits_SDR1[0:min_length]))
    print("secret key of SDR2=", len(uniform_quantized_bits_SDR2[0:min_length]))
    print("Result of uniform quantization for SDR1", uniform_quantized_bits_SDR1.astype(int))
    print("Result of uniform quantization for SDR2", uniform_quantized_bits_SDR2.astype(int))
if Quantization.WINDOW_THRESHOLD.value==True:
    print("Threshold Quantized bits of SDR1", threshold_quantized_bits_SDR1)
    print("Threshold Quantized bits of SDR2", threshold_quantized_bits_SDR2)
    print("Result of Threshold detection based quantization for SDR1", list(SDR1_bytes))
    print("Result of Threshold detection based quantization for SDR2", list(SDR2_bytes))

''''#fig, (ax2, ax3) = plt.subplots(2, 1)
#Calculate correlation coefficient of samples over certain range
if Quantization.UNIFORM.value==True:
    corr_coeff, number_of_samples=correlation_calculation.complete_correlation(min_length, uniform_quantized_bits_SDR1.astype(int), uniform_quantized_bits_SDR2.astype(int))
    plot_correlation.correlation_plot(number_of_samples, corr_coeff, ax2, 'r-')

if Quantization.WINDOW_THRESHOLD.value==True:
    corr_coeff, number_of_samples=correlation_calculation.complete_correlation(min_length, list(SDR1_bytes), list(SDR2_bytes))
    plot_correlation.correlation_plot(number_of_samples, corr_coeff, ax2, 'b-')'''

''''#Calculate correlation coefficient of samples over certain non overlapping window range
if Quantization.UNIFORM.value==True:
    corr_coeff, number_of_samples=correlation_calculation.correlation_non_overlapping_window(min_length, uniform_quantized_bits_SDR1.astype(int), uniform_quantized_bits_SDR2.astype(int), window_size)
    plot_correlation.correlation_plot(number_of_samples, corr_coeff, ax3, 'r-')
    print("Uniform", corr_coeff)

if Quantization.WINDOW_THRESHOLD.value==True:
    corr_coeff, number_of_samples=correlation_calculation.correlation_non_overlapping_window(min_length, list(SDR1_bytes), list(SDR2_bytes), window_size)
    plot_correlation.correlation_plot(number_of_samples, corr_coeff, ax3, 'b-')
    print("Threshold", corr_coeff)'''

#Calculate correlation coefficient of samples over certain overlapping window range
if Quantization.UNIFORM.value==True:
    corr_coeff, number_of_samples=correlation_calculation.correlation_overlapping_window(min_length, uniform_quantized_bits_SDR1.astype(int), uniform_quantized_bits_SDR2.astype(int), window_size)
    plot_correlation.correlation_plot(number_of_samples, corr_coeff, ax4, 'r-')

if Quantization.WINDOW_THRESHOLD.value==True:
    corr_coeff, number_of_samples=correlation_calculation.correlation_overlapping_window(min_length, list(SDR1_bytes), list(SDR2_bytes), window_size)
    plot_correlation.correlation_plot(number_of_samples, corr_coeff, ax4, 'b-')


#Binary Count
min_length=128/Quant_Range
SDR1_bincount=binary_count.intarray2binarray(uniform_quantized_bits_SDR1[0:round(min_length)].astype(int), Quant_Range)
SDR2_bincount=binary_count.intarray2binarray(uniform_quantized_bits_SDR2[0:round(min_length)].astype(int), Quant_Range)
print("SDR1 binary array", SDR1_bincount)
print("SDR2 binary array", SDR2_bincount)
equal_bit_array_uniquant=binary_count.bitcount_window(SDR1_bincount, SDR2_bincount, window_size)
print("Number of bits equal to each other for uniform quantization are", sum(equal_bit_array_uniquant), "for ", min_length*Quant_Range, "total bits")
print("Length of same bits array for uniform quantization", len(equal_bit_array_uniquant))
if Quantization.UNIFORM.value==True:
    plot_commonbits.plot_equalbits(equal_bit_array_uniquant, ax5, 'c-')

if Quantization.WINDOW_THRESHOLD.value==True:
    min_length = 128
    min_thresh_len=min_length
    #min_thresh_len=min(len(threshold_quantized_bits_SDR1[0:min_thresh_len]), len(threshold_quantized_bits_SDR2[0:min_thresh_len]))
    equal_bit_array_threshold=binary_count.bitcount_window(threshold_quantized_bits_SDR1[0:min_thresh_len], threshold_quantized_bits_SDR2[0:min_thresh_len], 1)
    print("equal", equal_bit_array_threshold, len(threshold_quantized_bits_SDR1[0:min_thresh_len]), len(threshold_quantized_bits_SDR2[0:min_thresh_len]), len(equal_bit_array_threshold), min_thresh_len)
    #print("Number of bits equal to each other are for threshold based quantization", equal_bit_array_threshold, "for ", min_thresh_len*Quant_Range, "total bits")
    #print("Length of same bits array for threshold quantization", len(equal_bit_array_threshold))
    sum_bitarray_threshold=[]
    for i in range(0, len(equal_bit_array_threshold), window_size):
        sum_perwindow=sum(equal_bit_array_threshold[i:i+window_size])
        sum_bitarray_threshold.append(sum_perwindow)
    if Quantization.WINDOW_THRESHOLD.value==True:
        plot_commonbits.plot_equalbits(sum_bitarray_threshold, ax5, 'm-')

'''ax5.vlines(number_of_samples ,0, corr_coeff, colors='k', linestyles='-', lw=6)
ax5=sns.histplot(corr_coeff,
                  bins=50,
                  kde=True,
                  color='red')'''
#ax5.set(xlabel='Normal Distribution', ylabel='Frequency')
#Reed Solomon encoding
#min_length=128
'''RS_encode=reedsolomon_codec.RS_encoding(list(uniform_quantized_bits_SDR1[0:min_length].astype(int)))
print("RS encoding", RS_encode[0:min_length])

#Reed Solomon decoding
RS_decode=reedsolomon_codec.RS_decoding(list(uniform_quantized_bits_SDR1[0:min_length].astype(int)), RS_encode)
print("decoded bytes", list(RS_decode[0:min_length]))
print("Original", list(uniform_quantized_bits_SDR1[0:min_length].astype(int)))
print("Target", list(uniform_quantized_bits_SDR2[0:min_length].astype(int)))

print("Decoding status ", RS_decode[0:min_length]==list(uniform_quantized_bits_SDR1[0:min_length].astype(int)))

print("Number of unequal elements", min_length-sum(binary_count.bitcount_window(list(uniform_quantized_bits_SDR1[0:min_length].astype(int)), list(uniform_quantized_bits_SDR2[0:min_length].astype(int)), 1)))'''
plt.tight_layout()
plt.show()

nzeros=np.count_nonzero(SDR1_bincount==0)
print("Number of 0's", nzeros, "and number of 1's", 128-nzeros)




# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import bitstringtobyte
import correlation_calculation
import plot_RSSI
import plot_correlation
import reedsolomon_codec
import string_to_bytearray
import stringify
import uniform_quantization


def doubleto8bit(x, a):
    s = np.sign(x)
    x = abs(x)

    if x == a:
        return 0
    b = np.floor(np.log2(x) + 1) - 8
    m = s * round(x / 2 ** b)

    y = m * 2 ** b
    return y

#Read the text file
with open('C:/Users/Prashanth/Desktop/CFO_sdr1.txt', 'r') as fin:
    data_read_SDR1 = fin.read()
with open('C:/Users/Prashanth/Desktop/CFO_sdr2.txt', 'r') as fin:
    data_read_SDR2 = fin.read()

# average = mean(data)
# print(average)
data_read_SDR1 = data_read_SDR1.replace(',', '.')
data_read_SDR2 = data_read_SDR2.replace(',', '.')

#Split the data based on escape character \n
list_of_strings_SDR1 = data_read_SDR1.split('\n')
list_of_strings_SDR2 = data_read_SDR2.split('\n')

#Convert string to float
list_of_floats_SDR1 = np.abs([float(x) for x in list_of_strings_SDR1])
list_of_floats_SDR2 = np.abs([float(x) for x in list_of_strings_SDR2])

print("RSSI values of SDR1", list_of_floats_SDR1)
print("RSSI values of SDR2", list_of_floats_SDR2)

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
Quant_Range=4

print("Max, Min, Avg, Var of SDR1", max_SDR1, min_SDR1, average_SDR1, var_SDR1)
print("Max, Min, Avg, Var of SDR2", max_SDR2, min_SDR2, average_SDR2, var_SDR2)

print("Number of entries from SDR1", len(list_of_floats_SDR1))
print("Number of entries from SDR2", len(list_of_floats_SDR2))

#Perform Uniform quantization
uniform_quantized_bits_SDR1 = uniform_quantization.uniform_quantization(list_of_floats_SDR1, min_SDR1, Quant_Range, max_SDR1)
uniform_quantized_bits_SDR2 = uniform_quantization.uniform_quantization(list_of_floats_SDR2, min_SDR2, Quant_Range, max_SDR2)
#quantized_bits_SDR1[np.where(quantized_bits_SDR1==0)] =1
#quantized_bits_SDR2[np.where(quantized_bits_SDR2==0)] =1
#Number of samples to work with
#min_length = min(len(list_of_floats_SDR1), len(list_of_floats_SDR2))
min_length = 128
window_size=8

if min_length%window_size!=0:
    print("Window size not matching length of the samples. Enter valid window_size")
    exit()

print("Min length =", min_length)
print("secret key of SDR1=", uniform_quantized_bits_SDR1[0:min_length])
print("secret key of SDR2=", uniform_quantized_bits_SDR2[0:min_length])
time = list(range(min_length))

#Quantization based on threshold detection
threshold_quantized_bits_SDR1=[0 if list_of_floats_SDR1_ < average_SDR1 else 1 for list_of_floats_SDR1_ in list_of_floats_SDR1]
threshold_quantized_bits_SDR2=[0 if list_of_floats_SDR2_ < average_SDR2 else 1 for list_of_floats_SDR2_ in list_of_floats_SDR2]
print("Quantized bits of SDR1", threshold_quantized_bits_SDR1)
print("Quantized bits of SDR2", threshold_quantized_bits_SDR2)

#Convert Quantized bits into string
SDR1_string=stringify.stringify(threshold_quantized_bits_SDR1)
SDR2_string=stringify.stringify(threshold_quantized_bits_SDR2)

#Bit string into byte array conversion
#SDR1_bytes=bitstringtobyte.bitstring_to_bytes(SDR1_string)
#SDR2_bytes=bitstringtobyte.bitstring_to_bytes(SDR2_string)

SDR1_bytes=string_to_bytearray.string_to_bytearray_conversion(Quant_Range,SDR1_string)
SDR2_bytes=string_to_bytearray.string_to_bytearray_conversion(Quant_Range, SDR2_string)

fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1)

#Plot RSSI values
plot_RSSI.plot_RSSI(time, list_of_floats_SDR1[0:min_length], list_of_floats_SDR2[0:min_length], ax1)

print("Result of uniform quantization", uniform_quantized_bits_SDR1.astype(int))
print("Result of Threshold detection based quantization", list(SDR1_bytes))

#fig, (ax2, ax3) = plt.subplots(2, 1)
#Calculate correlation coefficient of samples over certain range
corr_coeff, number_of_samples=correlation_calculation.complete_correlation(min_length, uniform_quantized_bits_SDR1.astype(int), uniform_quantized_bits_SDR2.astype(int))
plot_correlation.correlation_plot(number_of_samples, corr_coeff, ax2, 'r-')

corr_coeff, number_of_samples=correlation_calculation.complete_correlation(min_length, list(SDR1_bytes), list(SDR2_bytes))
plot_correlation.correlation_plot(number_of_samples, corr_coeff, ax2, 'b-')

#Calculate correlation coefficient of samples over certain non overlapping window range
corr_coeff, number_of_samples=correlation_calculation.correlation_non_overlapping_window(min_length, uniform_quantized_bits_SDR1.astype(int), uniform_quantized_bits_SDR2.astype(int), window_size)
plot_correlation.correlation_plot(number_of_samples, corr_coeff, ax3, 'r-')
print("Uniform",corr_coeff)

corr_coeff, number_of_samples=correlation_calculation.correlation_non_overlapping_window(min_length, list(SDR1_bytes), list(SDR2_bytes), window_size)
plot_correlation.correlation_plot(number_of_samples, corr_coeff, ax3, 'b-')
print("Threshold", corr_coeff)

#Calculate correlation coefficient of samples over certain overlapping window range
corr_coeff, number_of_samples=correlation_calculation.correlation_overlapping_window(min_length, uniform_quantized_bits_SDR1.astype(int), uniform_quantized_bits_SDR2.astype(int), window_size)
plot_correlation.correlation_plot(number_of_samples, corr_coeff, ax4, 'r-')

corr_coeff, number_of_samples=correlation_calculation.correlation_overlapping_window(min_length, list(SDR1_bytes), list(SDR2_bytes), window_size)
plot_correlation.correlation_plot(number_of_samples, corr_coeff, ax4, 'b-')

#Reed Solomon encoding
RS_encode=reedsolomon_codec.RS_encoding(list(uniform_quantized_bits_SDR1.astype(int)))
print("RS encoding", RS_encode)

#Reed SOlomon decoding
RS_decode=reedsolomon_codec.RS_decoding(list(uniform_quantized_bits_SDR1.astype(int)), RS_encode)
print("decoded bytes", RS_decode)
print("Original", list(uniform_quantized_bits_SDR2.astype(int)))

print("Decoding status", RS_decode==list(uniform_quantized_bits_SDR2.astype(int)))

plt.show()
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import plot_RSSI
import plot_correlation
import reedsolomon_codec


def doubleto8bit(x, a):
    s = np.sign(x)
    x = abs(x)

    if x == a:
        return 0
    b = np.floor(np.log2(x) + 1) - 8
    m = s * round(x / 2 ** b)

    y = m * 2 ** b
    return y


with open('C:/Users/Prashanth/Desktop/writefile.txt', 'r') as fin:
    data_read_SDR1 = fin.read()
with open('C:/Users/Prashanth/Desktop/writefile2.txt', 'r') as fin:
    data_read_SDR2 = fin.read()

# average = mean(data)
# print(average)
data_read_SDR1 = data_read_SDR1.replace(',', '.')
data_read_SDR2 = data_read_SDR2.replace(',', '.')

list_of_strings_SDR1 = data_read_SDR1.split('\n')
list_of_strings_SDR2 = data_read_SDR2.split('\n')

list_of_floats_SDR1 = [float(x) for x in list_of_strings_SDR1]
list_of_floats_SDR2 = [float(x) for x in list_of_strings_SDR2]

quantized_bits_SDR1 = np.zeros(len(list_of_floats_SDR1))
quantized_bits_SDR2 = np.zeros(len(list_of_floats_SDR2))

average_SDR1 = np.mean(list_of_floats_SDR1)
average_SDR2 = np.mean(list_of_floats_SDR2)

var_SDR1 = np.var(list_of_floats_SDR1)
var_SDR2 = np.var(list_of_floats_SDR2)

max_SDR1 = np.max(list_of_floats_SDR1)
min_SDR1 = np.min(list_of_floats_SDR1)
max_SDR2 = np.max(list_of_floats_SDR2)
min_SDR2 = np.min(list_of_floats_SDR2)

Quant_Range=4

print("Max, Min, Avg, Var of SDR1", max_SDR1, min_SDR1, average_SDR1, var_SDR1)
print("Max, Min, Avg, Var of SDR2", max_SDR2, min_SDR2, average_SDR2, var_SDR2)

print("Number of entries from SDR1", len(list_of_floats_SDR1))
print("Number of entries from SDR2", len(list_of_floats_SDR2))

for i in range(len(list_of_floats_SDR1)):
    quantized_bits_SDR1[i] = round(((list_of_floats_SDR1[i] - min_SDR1) * ((2**Quant_Range)-1)) / (max_SDR1 - min_SDR1))
for j in range(len(list_of_floats_SDR2)):
    quantized_bits_SDR2[j] = round(((list_of_floats_SDR2[j] - min_SDR2) * ((2**Quant_Range)-1)) / (max_SDR2 - min_SDR2))

min_length = min(len(list_of_floats_SDR1), len(list_of_floats_SDR2))
#min_length = 1000
print("Min length =", min_length)
print("secret key of SDR1=", quantized_bits_SDR1[0:min_length])
print("secret key of SDR2=", quantized_bits_SDR2[0:min_length])
time = list(range(min_length))

unequal_count = 0
for i, j in zip(quantized_bits_SDR1[0:min_length], quantized_bits_SDR2[0:min_length]):
    if i != j:
        unequal_count = unequal_count + 1

print("Number of unequal bits", unequal_count)

fig, (ax1, ax2) = plt.subplots(2, 1)

#plot_RSSI.plot_RSSI(time, list_of_floats_SDR1[0:min_length], list_of_floats_SDR2[0:min_length], ax1)

#fig, (ax2, ax3) = plt.subplots(2, 1)

number_of_samples=range(min_length)
corr_coeff=np.zeros(len(number_of_samples))
for i in range(1, len(number_of_samples)):
    corr_coefficient=np.corrcoef(quantized_bits_SDR1[0:i], quantized_bits_SDR2[0:i])
    corr_coeff[i]=corr_coefficient[0,1]

#plot_correlation.correlation_plot(number_of_samples, corr_coeff, ax2)
print("Quantised bits", list(quantized_bits_SDR1.astype(int)))
RS_encode=reedsolomon_codec.RS_encoding(list(quantized_bits_SDR1.astype(int)))
print("RS encoding", RS_encode)

RS_decode=reedsolomon_codec.RS_decoding(list(quantized_bits_SDR1.astype(int)), RS_encode)
print("decoded bytes", RS_decode)
print("Original", list(quantized_bits_SDR1.astype(int)))

print("Decoding status", RS_decode==list(quantized_bits_SDR1.astype(int)))

#plt.show()
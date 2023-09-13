import matplotlib.pyplot as plt2
import matplotlib.pyplot as plt3
import matplotlib.pyplot as plt4
import matplotlib.pyplot as plt5

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
import wavelet_transform

class Common_Source:
    def __init__(self, list_of_float):
        self.raw_samples=list_of_float

class Category_CR:
    def __init__(self):
        self.entropy=[]
        self.CR_rate=[]
        self.error_bits=[]
        self.error_bits_gray=[]
        self.floor_diff=[]


with open('C:/Users/prashanth/Desktop/RSSI_SC_212_SDR1.txt', 'r') as fin:
    data_read_SDR1 = fin.read()
    last_char_SDR1 = data_read_SDR1[-1]
    if last_char_SDR1 == '\n':
        data_read_SDR1 = data_read_SDR1[:-1]
with open('C:/Users/prashanth/Desktop/RSSI_SC_212_SDR2.txt', 'r') as fin:
    data_read_SDR2 = fin.read()
    last_char_SDR2 = data_read_SDR2[-1]
    if last_char_SDR2 == '\n':
        data_read_SDR2 = data_read_SDR2[:-1]


# average = mean(data)
# print(average)
RSSI_data_read_SDR1 = data_read_SDR1.replace(',', '.')
RSSI_data_read_SDR2 = data_read_SDR2.replace(',', '.')

# Split the data based on escape character \n
list_of_strings_SDR1 = RSSI_data_read_SDR1.split('\n')
list_of_strings_SDR2 = RSSI_data_read_SDR2.split('\n')

# Convert string to float
list_of_floats_SDR1 = [float(x) for x in list_of_strings_SDR1]
list_of_floats_SDR2 = [float(x) for x in list_of_strings_SDR2]
list_of_floats_SDR1 = list(map(lambda x: x * -1 if x < 0 else x, list_of_floats_SDR1))
list_of_floats_SDR2 = list(map(lambda x: x * -1 if x < 0 else x, list_of_floats_SDR2))

RSSI_SDR1=Common_Source(list_of_floats_SDR1)
RSSI_SDR2=Common_Source(list_of_floats_SDR2)


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
RSSI_data_read_SDR1 = data_read_SDR1.replace(',', '.')
RSSI_data_read_SDR2 = data_read_SDR2.replace(',', '.')

# Split the data based on escape character \n
list_of_strings_SDR1 = RSSI_data_read_SDR1.split('\n')
list_of_strings_SDR2 = RSSI_data_read_SDR2.split('\n')

# Convert string to float
list_of_floats_SDR1 = [float(x) for x in list_of_strings_SDR1]
list_of_floats_SDR2 = [float(x) for x in list_of_strings_SDR2]
list_of_floats_SDR1 = list(map(lambda x: x * -1 if x < 0 else x, list_of_floats_SDR1))
list_of_floats_SDR2 = list(map(lambda x: x * -1 if x < 0 else x, list_of_floats_SDR2))

CFO_SDR1=Common_Source(list_of_floats_SDR1)
CFO_SDR2=Common_Source(list_of_floats_SDR2)

min_length=16

#Change this for size of kernel and window
min_l = min_length
window_size = min_l
# Plot Original
time = range(min_l)
xlab = "Freq Raw Sample in Hz"
#plot_CFO.plot_CFO(time, list_of_floats_SDR1[ind:ind + min_l], list_of_floats_SDR2[ind:ind + min_l], ax2, xlab)
fontsz=40
fig3, axis3 = plt3.subplots()
plt3.rcParams.update({'font.family': 'Times New Roman', 'font.size': fontsz, })
plt3.grid()
#plt3.plot(range(2, 32), label='Ideal CR capacity', color='red')
count=0
win=min_l

Savgol=Category_CR()

maxQuantrange=4

num_rows = maxQuantrange-1
num_columns = int(min_length/min_l)

quan_size = []
mode = 0

SDR1_1_norm = noise_removal.savgold_filter(CFO_SDR1.raw_samples[0:0 + min_l], win)
SDR2_1_norm = noise_removal.savgold_filter(CFO_SDR2.raw_samples[0:0 + min_l], win)

#SDR1_1_norm = CFO_SDR1.raw_samples[0:0 + min_l]
#SDR2_1_norm = CFO_SDR2.raw_samples[0:0 + min_l]

j = 0
labelarray = []
count = 0
Quantseteps = 8

Quant_Range = Quantseteps
SDR1_2gbytes, SDR2_2gbytes = lossless_quantization.multi_bit_quantization_corrplot(SDR1_1_norm,
                                                                                   SDR2_1_norm,
                                                                                   min_l,
                                                                                   window_size,
                                                                                   Quant_Range,
                                                                                   True, False)


SDR1_2bytes, SDR2_2bytes = lossless_quantization.multi_bit_quantization_corrplot(SDR1_1_norm,
                                                                                 SDR2_1_norm,
                                                                                 min_l,
                                                                                 window_size,
                                                                                 Quant_Range,
                                                                                 False, False)



SDR1_2, SDR2_2 = int2byte_conversion.intarray_to_bytearray(SDR1_2gbytes, SDR2_2gbytes, Quant_Range)
#plot_histogram.create_histogram(SDR2_2, 4, ax4)
num_errors, error_dist = erroranderror_distribution.error_distribution(SDR1_2gbytes, SDR2_2gbytes)
num_errors_norm, error_dist_norm = erroranderror_distribution.error_distribution(SDR1_2bytes, SDR2_2bytes)

floor_diff=[abs(x - y) for x, y in zip(SDR1_2, SDR2_2)]

Savgol.error_bits_gray.append(num_errors)
Savgol.error_bits.append(num_errors_norm)
Savgol.entropy.append(calculate_entropy.calculate_entropy(SDR1_2))
Savgol.CR_rate.append((calculate_entropy.calculate_entropy(SDR1_2)) * abs(1 - 2 * (num_errors / (Quant_Range * min_l))))


label = f'{Quant_Range}'
labelarray.append(label)


mark='D'
mark_cap='^'

#############REED SOLOMON CODE BEGINS HERE

SDR1_bincount = binary_count.intarray2binarray(SDR1_2, Quant_Range)
SDR2_bincount = binary_count.intarray2binarray(SDR2_2, Quant_Range)
print("SDR1 binary array", SDR1_bincount, len(SDR1_bincount))
print("SDR2 binary array", SDR2_bincount, len(SDR2_bincount))

greycode_stringSDR1 = stringify.stringify(SDR1_bincount.astype(int))
greycode_stringSDR2 = stringify.stringify(SDR2_bincount.astype(int))
print("greycode string for SDR1", greycode_stringSDR1, " of length", len(greycode_stringSDR1))
print("greycode string for SDR2", greycode_stringSDR2, " of length", len(greycode_stringSDR2))

greycodeSDR1_bytes = string_to_bytearray.string_to_bytearray_conversion(8, greycode_stringSDR1)
greycodeSDR2_bytes = string_to_bytearray.string_to_bytearray_conversion(8, greycode_stringSDR2)
print("greycode SDR1", greycodeSDR1_bytes, "of length", len(greycodeSDR1_bytes))
print("greycode SDR2", greycodeSDR2_bytes, "of length", len(greycodeSDR2_bytes))



segment_size=16
parity_size=8

number_of_segments=1

RS_encode = reedsolomon_codec.RS_encoding(list(greycodeSDR1_bytes[0:segment_size * number_of_segments]), segment_size,
                                          parity_size, number_of_segments)
print("RS encoding for gray coding is ", list(RS_encode), " with parity byte length ", len(RS_encode))
# RS Decode
RS_decode = reedsolomon_codec.RS_decoding(list(greycodeSDR2_bytes[0:segment_size * number_of_segments]), RS_encode,
                                          segment_size, parity_size, number_of_segments)
print("Decoding status with gray codes ", RS_decode == list(greycodeSDR1_bytes[0:segment_size * number_of_segments]))
print("decoded bytes with gray codes ", list(RS_decode), " with byte length ", len(RS_decode))


#SDR1_bincount = binary_count.intarray2binarray(SDR1_2, Quant_Range)
SDR2_bincount = binary_count.intarray2binarray(RS_decode, Quant_Range)


# Create a simple bar plot
x = range(0, len(SDR1_bincount))
plt3.plot(x, [int(x) for x in SDR1_bincount], label="SDR1")
plt3.plot(x, [int(x) for x in SDR2_bincount], label="SDR2")

# Label the x-axis
plt3.xlabel('Index')

# Label the y-axis
plt3.ylabel('Key bits')

# Set the title of the plot
plt3.title('Array containing 1s and 0s')
plt3.legend()

# Show the plot
plt3.show()


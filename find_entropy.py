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
#import kalman_filter
import confidence_interval
import calculate_entropy
import cr_rate_plot
import wavelet_transform
import os
import histogram_equalization
import kltransform
import dct
import matplotlib.pyplot as plt3

print(os.environ['PATH'])
class Common_Source:
    def __init__(self, list_of_float):
        self.raw_samples=list_of_float

class Category_CR:
    def __init__(self):
        self.entropy=[]
        self.CR_rate=[]
        self.error_bits_gray=[]
        self.floor_diff=[]
        self.cost_func=[]
        self.avg_cost=[]

#### Read 8 bits
with open('C:/Users/prashanth/Desktop/SDR1_RSSI_8bit.txt', 'r') as fin:
    data_read_SDR1 = fin.read()
    last_char_SDR1 = data_read_SDR1[-1]
    if last_char_SDR1 == '\n':
        data_read_SDR1 = data_read_SDR1[:-1]
with open('C:/Users/prashanth/Desktop/SDR2_RSSI_8bit.txt', 'r') as fin:
    data_read_SDR2 = fin.read()
    last_char_SDR2 = data_read_SDR2[-1]
    if last_char_SDR2 == '\n':
        data_read_SDR2 = data_read_SDR2[:-1]

RSSI_data_read_SDR1 = data_read_SDR1.replace(',', '.')
RSSI_data_read_SDR2 = data_read_SDR2.replace(',', '.')

# Split the data based on escape character \n
list_of_strings_SDR1 = RSSI_data_read_SDR1.split('\n')
list_of_strings_SDR2 = RSSI_data_read_SDR2.split('\n')

# Convert string to float
list_of_int_SDR1 = [int(x) for x in list_of_strings_SDR1]
list_of_int_SDR2 = [int(x) for x in list_of_strings_SDR2]
new_list1, new_list2 = zip(*[
    (a, b) for a, b in zip(list_of_int_SDR1, list_of_int_SDR2) if a <= 0
])
list_of_int_SDR1 = list(new_list1)
list_of_int_SDR2 = list(new_list2)

RSSI_8bit_SDR1=Common_Source(list_of_int_SDR1)
RSSI_8bit_SDR2=Common_Source(list_of_int_SDR2)

min_length=262144

rep_unit=18
n=2**rep_unit

block_length=min_length/n

#Change this for size of kernel and window
min_l = int(min_length/block_length)
print("Number of blocks", min_l)
window_size = min_l
ind=0

sample_entropy=[]
for ind in range(0, min_length, min_l):
    sample_entropy.append(calculate_entropy.calculate_entropy(RSSI_8bit_SDR1.raw_samples[ind:ind + min_l]))
    #SDR1_1_norm = np.array(RSSI_8bit_SDR1.raw_samples[ind:ind + min_l]).round(decimals=3)
    #sample_entropy.append(calculate_entropy.calculate_entropy(SDR1_1_norm))

print("Entropy", sample_entropy)
print("Mean of entropy", np.mean(sample_entropy))
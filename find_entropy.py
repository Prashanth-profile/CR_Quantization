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
list_of_int_SDR1 = [np.int8(x) for x in list_of_strings_SDR1]
list_of_int_SDR2 = [np.int8(x) for x in list_of_strings_SDR2]
new_list1, new_list2 = zip(*[
    (a, b) for a, b in zip(list_of_int_SDR1, list_of_int_SDR2) if a <= 0
])
list_of_int_SDR1 = list(new_list1)
list_of_int_SDR2 = list(new_list2)

RSSI_8bit_SDR1=Common_Source(list_of_int_SDR1)
RSSI_8bit_SDR2=Common_Source(list_of_int_SDR2)

min_length=262144

rep_unit=16
n=2**rep_unit

block_length=min_length/n

#Change this for size of kernel and window
min_l = int(min_length/block_length)
print("Number of blocks", min_l)
window_size = min_l
ind=0
quant=16
sample_entropy_obs=[]
sample_entropy_fil=[]
nr2entropy=[]
quantentropy=[]
for ind in range(0, min_length, min_l):
    #Obs_sample=np.array(dct.adaptive_dct_filter(RSSI_8bit_SDR1.raw_samples[ind:ind + min_l]).round(decimals=3))
    Obs_sample = RSSI_8bit_SDR1.raw_samples[ind:ind + min_l]
    Obs_sample = [np.int8(x) for x in Obs_sample]
    #Obs_sample=np.array(Obs_sample).round(decimals=5)
    sample_entropy_obs.append(calculate_entropy.calculate_entropy(Obs_sample))
    SDR1_1_norm = dct.adaptive_dct_filter_window(Obs_sample, 2) #32bit DCT
    SDR2_1_norm_2 = dct.adaptive_dct_filter(RSSI_8bit_SDR2.raw_samples[ind:ind + min_l])
    #SDR1_1_norm = np.array(SDR1_1_norm).round(decimals=5)
    #MSB
    #SDR1_1_norm = (np.array(SDR1_1_norm).astype(np.int16) >> 8).astype(np.int8)
    #SDR2_1_norm = (np.array(SDR2_1_norm_2).astype(np.int16) >> 8).astype(np.int8)
    #LSB
    #SDR1_1_norm = np.array(SDR1_1_norm).astype(np.int8)
    #SDR2_1_norm = np.array(SDR2_1_norm_2).astype(np.int8)
    #Part 3 LSB
    SDR1_1_norm = [np.int16(x) for x in SDR1_1_norm]
    SDR2_1_norm = [np.int16(x) for x in SDR2_1_norm_2]
    print("Filtered out 1", calculate_entropy.calculate_entropy(SDR1_1_norm))
    #print("Filtered out 2", SDR2_1_norm)
    # SDR2_1_norm = dct.adaptive_dct_filter_window(list_of_floats_SDR2[ind:ind + min_l], int(min_l/2))
    #SDR1_1_norm = np.array(RSSI_8bit_SDR1.raw_samples[ind:ind + min_l]).round(decimals=3)
    sample_entropy_fil.append(calculate_entropy.calculate_entropy(SDR1_1_norm))

    SDR1_2gbytes, SDR2_2gbytes = lossless_quantization.multi_bit_quantization_corrplot(SDR1_1_norm,
                                                                                       SDR2_1_norm,
                                                                                       min_l,
                                                                                       min_l,
                                                                                       quant,
                                                                                       True, False)

    SDR1_2, SDR2_2 = int2byte_conversion.intarray_to_bytearray(SDR1_2gbytes, SDR2_2gbytes, quant)

    num_errors, error_dist = erroranderror_distribution.error_distribution(SDR1_2gbytes, SDR2_2gbytes, quant)

    quantentropy.append(calculate_entropy.calculate_entropy(SDR1_2gbytes))
    print("Entropy Quant", calculate_entropy.calculate_entropy(SDR1_2gbytes))
    SDR1_2, SDR2_2 = int2byte_conversion.intarray_to_bytearray(SDR1_2gbytes, SDR2_2gbytes, quant)
    entropy=(calculate_entropy.calculate_entropy(SDR1_2))* abs(1 - (2 * (num_errors / (quant * min_l))))
    nr2entropy.append(entropy)
    print("CR rate", entropy)

print("Entropy of observation", sample_entropy_obs)
print("Entropy of filter", sample_entropy_fil)
print("Mean of entropy of obs. and fil.", np.mean(sample_entropy_obs), np.mean(sample_entropy_fil))
print("Mean Cr rate", np.mean(nr2entropy))
print("Quant entropy", np.mean(quantentropy))
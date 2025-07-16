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
import confidence_interval
import calculate_entropy
import cr_rate_plot
import wavelet_transform
import os
import histogram_equalization
import kltransform
import dct
import random
import seeded_mt19937
import timeit
from collections import Counter
import conditionalprob_pcr

import matplotlib.pyplot as plt


def find_duplicates(lst):
    seen = set()
    duplicates = set()

    for item in lst:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)

    return list(duplicates)

def mark_repeating(lst):
    counts = Counter(lst)
    return [1 if counts[item] > 1 else 0 for item in lst]

print(os.environ['PATH'])
class Common_Source:
    def __init__(self, list_of_float):
        self.raw_samples=list_of_float


#################################### Legitimate parties ####################################################

with open('C:/Users/prashanth/Desktop/CFO_SC_805_SDR1.txt', 'r') as fin:
    data_read_SDR1 = fin.read()
    last_char_SDR1 = data_read_SDR1[-1]
    if last_char_SDR1 == '\n':
        data_read_SDR1 = data_read_SDR1[:-1]
with open('C:/Users/prashanth/Desktop/CFO_SC_805_SDR2.txt', 'r') as fin:
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

min_length=8192
#Change this for size of kernel and window
min_l = 256
window_size = min_l
# Plot Original
time = range(min_l)
xlab = "Freq Raw Sample in Hz"
#plot_CFO.plot_CFO(time, list_of_floats_SDR1[ind:ind + min_l], list_of_floats_SDR2[ind:ind + min_l], ax2, xlab)
fontsz=40
#plt3.rcParams.update(plt.rcParamsDefault)
plt.rcParams['text.usetex'] = True
fig3, axis3 = plt.subplots()
plt.rcParams.update({'font.family': 'Times New Roman', 'font.size': fontsz, })
plt.grid()

win=min_l

maxQuantrange = 8

quan_size = []
source_entropy=[]
mode = 0

SDR1_2_histeq=[]
SDR2_2_histeq=[]

pdf_error_dist=np.zeros(min_l*8)

start_time = timeit.default_timer()

SDR1_1_norm = noise_removal.savgold_filter(CFO_SDR1.raw_samples[0:min_length], win-1)
SDR2_1_norm = noise_removal.savgold_filter(CFO_SDR2.raw_samples[0:min_length], win-1)

SDR1_quantized=[]
SDR2_quantized=[]

num_sequences=int(min_length/min_l)

for k in range(0, num_sequences):
    SDR1_2gbytes, SDR2_2gbytes = lossless_quantization.multi_bit_quantization_corrplot(SDR1_1_norm[k:k+min_l],
                                                                                   SDR2_1_norm[k:k+min_l],
                                                                                   min_l,
                                                                                   window_size,
                                                                                   maxQuantrange,
                                                                                   True, False)

    SDR1_2, SDR2_2 = int2byte_conversion.intarray_to_bytearray(SDR1_2gbytes, SDR2_2gbytes, maxQuantrange)

    SDR1_bincount = binary_count.intarray2binarray(SDR1_2, maxQuantrange)
    SDR2_bincount = binary_count.intarray2binarray(SDR2_2, maxQuantrange)

    greycode_stringSDR1 = stringify.stringify(SDR1_bincount.astype(int))
    greycode_stringSDR2 = stringify.stringify(SDR2_bincount.astype(int))
    print("greycode string for SDR1", greycode_stringSDR1, " of length", len(greycode_stringSDR1))
    # print("greycode string for SDR2", greycode_stringSDR2, " of length", len(greycode_stringSDR2))

    greycodeSDR1_bytes = string_to_bytearray.string_to_bytearray_conversion(maxQuantrange, greycode_stringSDR1)
    random.Random(4).shuffle(greycodeSDR1_bytes)

    SDR1_quantized.append(greycodeSDR1_bytes)

print("After", SDR1_quantized, len(np.array(SDR1_quantized).reshape(-1)))

print("Gray code bytes", len(SDR1_quantized))

np.array(SDR1_quantized).reshape(-1)

np.array(SDR1_quantized).reshape(num_sequences, 256)


# Calculate the conditional probabilities
conditional_probabilities = conditionalprob_pcr.calculate_conditional_probabilities(num_sequences, 256, SDR1_quantized)

conditional_entropy = conditionalprob_pcr.compute_conditional_entropy(conditional_probabilities)

print("Conditional entropy of CR", conditional_entropy)

# Print the probabilities
print("Conditional Probabilities of Each Sequence:")
for i, prob in enumerate(conditional_probabilities):
    print(f"Sequence {i + 1}: {prob:.6f}")

# Plot the conditional probabilities
plt.figure(figsize=(10, 6))
plt.bar(range(1, num_sequences + 1), conditional_probabilities, color='b', alpha=0.7, label='seeded MT')
plt.xlabel("Sequence Index")
plt.ylabel("Conditional Probability")
plt.title("Conditional Probability of seededMT")
plt.xticks(range(1, num_sequences + 1, 2))  # Show every 2nd sequence index for readability
plt.ylim(0, 1.1)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()









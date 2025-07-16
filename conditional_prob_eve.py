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
import matplotlib.pyplot as plt2


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

with open('C:/Users/prashanth/Desktop/CFO_SC_286_SDR1.txt', 'r') as fin:
    data_read_SDR1 = fin.read()
    last_char_SDR1 = data_read_SDR1[-1]
    if last_char_SDR1 == '\n':
        data_read_SDR1 = data_read_SDR1[:-1]
with open('C:/Users/prashanth/Desktop/CFO_SC_286_SDR2.txt', 'r') as fin:
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

min_length=4096
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

########################################## Eavesdropper ################################################################
with open('C:/Users/prashanth/Desktop/EveAl_CFO_286_SDR3.txt', 'r') as fin:
    data_read_SDR1 = fin.read()
    last_char_SDR1 = data_read_SDR1[-1]
    if last_char_SDR1 == '\n':
        data_read_SDR1 = data_read_SDR1[:-1]
with open('C:/Users/prashanth/Desktop/EveBob_CFO_286_SDR3.txt', 'r') as fin:
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

CFO_SDR1_eve=Common_Source(list_of_floats_SDR1)
CFO_SDR2_eve=Common_Source(list_of_floats_SDR2)

min_length=4096
#Change this for size of kernel and window
min_l = 256
window_size = min_l
# Plot Original
time = range(min_l)
xlab = "Freq Raw Sample in Hz"
#plot_CFO.plot_CFO(time, list_of_floats_SDR1[ind:ind + min_l], list_of_floats_SDR2[ind:ind + min_l], ax2, xlab)

win=min_l

maxQuantrange = 8

Eve_SDR1_1_norm = noise_removal.savgold_filter(CFO_SDR1_eve.raw_samples[0:min_length], win-1)
Eve_SDR2_1_norm = noise_removal.savgold_filter(CFO_SDR2_eve.raw_samples[0:min_length], win-1)

Eve_SDR1_quantized=[]
Eve_SDR2_quantized=[]
#########################################################################################################################

for k in range(0, num_sequences):
    #Legit
    SDR1_2gbytes, SDR2_2gbytes = lossless_quantization.multi_bit_quantization_corrplot(SDR1_1_norm[k:k+min_l],
                                                                                   SDR2_1_norm[k:k+min_l],
                                                                                   min_l,
                                                                                   window_size,
                                                                                   maxQuantrange,
                                                                                   True, False)
    #Eve
    Eve_SDR1_2gbytes, Eve_SDR2_2gbytes = lossless_quantization.multi_bit_quantization_corrplot(Eve_SDR1_1_norm[k:k+min_l],
                                                                                   Eve_SDR2_1_norm[k:k+min_l],
                                                                                   min_l,
                                                                                   window_size,
                                                                                   maxQuantrange,
                                                                                   True, False)

    #Legit
    SDR1_2, SDR2_2 = int2byte_conversion.intarray_to_bytearray(SDR1_2gbytes, SDR2_2gbytes, maxQuantrange)

    #Eve
    Eve_SDR1_2, Eve_SDR2_2 = int2byte_conversion.intarray_to_bytearray(Eve_SDR1_2gbytes, Eve_SDR2_2gbytes, maxQuantrange)

    #Legit
    SDR1_bincount = binary_count.intarray2binarray(SDR1_2, maxQuantrange)
    SDR2_bincount = binary_count.intarray2binarray(SDR2_2, maxQuantrange)

    #Eve
    Eve_SDR1_bincount = binary_count.intarray2binarray(SDR1_2, maxQuantrange)
    Eve_SDR2_bincount = binary_count.intarray2binarray(SDR2_2, maxQuantrange)

    #Legit
    greycode_stringSDR1 = stringify.stringify(SDR1_bincount.astype(int))
    greycode_stringSDR2 = stringify.stringify(SDR2_bincount.astype(int))
    #print("greycode string for SDR1", greycode_stringSDR1, " of length", len(greycode_stringSDR1))
    # print("greycode string for SDR2", greycode_stringSDR2, " of length", len(greycode_stringSDR2))

    #Eve
    Eve_greycode_stringSDR1 = stringify.stringify(Eve_SDR1_bincount.astype(int))
    Eve_greycode_stringSDR2 = stringify.stringify(Eve_SDR2_bincount.astype(int))

    #Legit
    greycodeSDR1_bytes = string_to_bytearray.string_to_bytearray_conversion(maxQuantrange, greycode_stringSDR1)
    greycodeSDR2_bytes = string_to_bytearray.string_to_bytearray_conversion(maxQuantrange, greycode_stringSDR2)
    number_of_segments=16
    segment_size=int(min_l*8/(8*number_of_segments))
    parity_size=32

    #Legit
    RS_encode = reedsolomon_codec.RS_encoding(list(greycodeSDR1_bytes[0:segment_size * number_of_segments]),
                                              segment_size,
                                              parity_size, number_of_segments)
    # print("RS encoding for gray coding is ", list(RS_encode), " with parity byte length ", len(RS_encode))
    RS_decode = reedsolomon_codec.RS_decoding(list(greycodeSDR2_bytes[0:segment_size * number_of_segments]), RS_encode,
                                              segment_size, parity_size, number_of_segments)
    random.Random(4).shuffle(greycodeSDR1_bytes)
    greycodeSDR2_bytes=list(RS_decode)
    random.Random(4).shuffle(greycodeSDR2_bytes)
    #print("Legit ALice", greycodeSDR1_bytes)
    #print("Legit Bob", greycodeSDR2_bytes)

    #Eve
    Eve_greycodeSDR1_bytes = string_to_bytearray.string_to_bytearray_conversion(maxQuantrange, Eve_greycode_stringSDR1)
    RS_decode = reedsolomon_codec.RS_decoding(list(Eve_greycodeSDR1_bytes[0:segment_size * number_of_segments]), RS_encode,
                                              segment_size, parity_size, number_of_segments)
    Eve_greycodeSDR1_bytes = list(RS_decode)
    random.Random(4).shuffle(Eve_greycodeSDR1_bytes)
    #print("Eavesdropper", Eve_greycodeSDR1_bytes)

    #Legit
    SDR1_quantized.append(greycodeSDR1_bytes)
    SDR2_quantized.append(greycodeSDR2_bytes)

    #Eve
    Eve_SDR1_quantized.append(Eve_greycodeSDR1_bytes)

#print("After", SDR1_quantized, len(np.array(SDR1_quantized).reshape(-1)))

#print("Gray code bytes", len(SDR1_quantized))

#Legit
np.array(SDR1_quantized).reshape(-1)
np.array(SDR1_quantized).reshape(num_sequences, min_l)
np.array(SDR2_quantized).reshape(-1)
np.array(SDR2_quantized).reshape(num_sequences, min_l)

#Eve
np.array(Eve_SDR1_quantized).reshape(-1)
np.array(Eve_SDR1_quantized).reshape(num_sequences, min_l)

#Legit
print("SDR1",SDR1_quantized, '\n', "SDR2", SDR2_quantized)
conditional_probabilities = conditionalprob_pcr.calculate_conditional_probabilities_priori(num_sequences, min_l, SDR1_quantized, SDR2_quantized)
conditional_entropy = conditionalprob_pcr.compute_conditional_entropy(conditional_probabilities)
print("Conditional entropy of CR", conditional_entropy)

for i, prob in enumerate(conditional_probabilities):
    print(f"Legit Sequence {i + 1}: {prob:.6f}")



#Eve
# Calculate the conditional probabilities
eve_conditional_probabilities = conditionalprob_pcr.calculate_conditional_probabilities_priori(num_sequences, min_l, SDR1_quantized, Eve_SDR1_quantized)
eve_conditional_entropy = conditionalprob_pcr.compute_conditional_entropy(eve_conditional_probabilities)

print("Conditional entropy of CR at evesdropper", eve_conditional_entropy)

# Print the probabilities
print("Conditional Probabilities of Each Sequence:")
for i, prob in enumerate(eve_conditional_probabilities):
    print(f"Eavesdropper Sequence {i + 1}: {prob:.6f}")

# Plot the conditional probabilities
plt.figure(figsize=(10, 6))
plt.bar(range(1, num_sequences + 1), eve_conditional_probabilities, color='b', alpha=0.7, label='Eve entropy')
plt.xlabel("Sequence Index")
plt.ylabel("Conditional Probability")
plt.title("Conditional Probability at eve")
plt.xticks(range(1, num_sequences + 1, 2))  # Show every 2nd sequence index for readability
plt.ylim(0, 1.1)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()


plt2.figure(figsize=(10, 6))
plt2.bar(range(1, num_sequences + 1), conditional_probabilities, color='r', alpha=0.7, label='Legit entropy')
plt2.xlabel("Sequence Index")
plt2.ylabel("Conditional Probability")
plt2.title("Conditional Probability for legitimate devices")
plt2.xticks(range(1, num_sequences + 1, 2))  # Show every 2nd sequence index for readability
plt2.ylim(0, 1.1)
plt2.grid(axis='y', linestyle='--', alpha=0.7)
plt2.show()









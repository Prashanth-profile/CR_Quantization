import random

import matplotlib.pyplot as plt2
import numpy as np

import dct
import plot_RSSI
import plot_CFO
import plot_PO
import math
import correlation_calculation
import plot_correlation
import noise_removal
import wavelet_transform
import lossless_quantization
import int2byte_conversion
import erroranderror_distribution
import calculate_entropy
import binary_count
import stringify
import string_to_bytearray
import reedsolomon_codec
import save_to_bin
from scipy import fftpack, ndimage
import hash_encrypt

plt2.rcParams.update(plt2.rcParamsDefault)
plt2.rcParams['text.usetex'] = True
plt2.rcParams.update({'font.family': 'Times New Roman', 'font.size': 40, })
fig2, ax11 = plt2.subplots()
ax11.grid(True)
plt2.xlabel('Normalised Frequency')
plt2.ylabel('Amplitude')


class Category_CR:
    def __init__(self):
        self.entropy=[]
        self.CR_rate=[]
        #self.error_bits=[]
        self.error_bits_gray=[]
        self.floor_diff=[]
        self.cost_func=[]
        self.avg_cost=[]

fontsz=50
min_length=65536
min_l=65536
time=range(min_length)
ind=0

Savgol=Category_CR()

with open('C:/Users/prashanth/Desktop/SDR1_RSSI_32bit.txt', 'r') as fin:
    data_read_SDR1 = fin.read()
    last_char_SDR1 = data_read_SDR1[-1]
    if last_char_SDR1 == '\n':
        print("last next line character detected in first sample file")
        data_read_SDR1 = data_read_SDR1[:-1]
with open('C:/Users/prashanth/Desktop/SDR2_RSSI_32bit.txt', 'r') as fin:
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
list_of_floats_SDR1 = [np.float32(x) for x in list_of_strings_SDR1]
list_of_floats_SDR2 = [np.float32(x) for x in list_of_strings_SDR2]
new_list1, new_list2 = zip(*[
    (a, b) for a, b in zip(list_of_floats_SDR1, list_of_floats_SDR2) if a <= 0
])
#list_of_int_SDR1 = list(map(lambda x: x * -1 if x < 0 else x, list_of_int_SDR1))
list_of_floats_SDR1 = list(new_list1)
list_of_floats_SDR2 = list(new_list2)
list_of_floats_SDR1 = list(map(lambda x: x*-1 if x < 0 else x, list_of_floats_SDR1))
list_of_floats_SDR2 = list(map(lambda x: x*-1 if x < 0 else x, list_of_floats_SDR2))


#SDR1_1_norm=noise_removal.savgold_filter(list_of_floats_SDR1[ind:ind+min_length], min_l)
#SDR2_1_norm=noise_removal.savgold_filter(list_of_floats_SDR2[ind:ind+min_length], min_l)

#SDR1_1_norm=noise_removal.window_smoothening(list_of_floats_SDR1[ind:ind+min_length], 2046)
#SDR2_1_norm=noise_removal.window_smoothening(list_of_floats_SDR2[ind:ind+min_length], 2046)

#SDR1_1_norm = wavelet_transform.wavelet_transform_haar(list_of_floats_SDR1[ind:ind+min_length], min_l)
#SDR2_1_norm = wavelet_transform.wavelet_transform_haar(list_of_floats_SDR2[ind:ind+min_length], min_l)

#SDR1_1_norm=list_of_floats_SDR1[ind:ind+min_length]
#SDR2_1_norm=list_of_floats_SDR2[ind:ind+min_length]

#SDR1_1_norm=noise_removal.savgold_filter_ali(list_of_floats_SDR1[ind:ind+min_length], 9,5)
#SDR2_1_norm=noise_removal.savgold_filter_ali(list_of_floats_SDR2[ind:ind+min_length], 9,5)


j = 0
labelarray = []
count = 0
Quantseteps = 16

file_path = r'C:\Users\prashanth\Desktop\multibyte_array_postscrambling.bin'

Quant_Range = Quantseteps

raw_data=bytearray()
#for ind in range(0, min_length, min_l):
SDR1_1_norm_1 = dct.adaptive_dct_filter(list_of_floats_SDR1[ind:ind + min_l])
SDR2_1_norm_2 = dct.adaptive_dct_filter(list_of_floats_SDR2[ind:ind + min_l])

#SDR1_1_norm_1 = dct.adaptive_dct_filter_window(list_of_floats_SDR1[ind:ind + min_l], int(min_l/2)) #32bit DCT
#SDR2_1_norm_2 = dct.adaptive_dct_filter_window(list_of_floats_SDR2[ind:ind + min_l], int(min_l/2))


#SDR1_1_norm_1= noise_removal.savgold_filter(list_of_floats_SDR1[ind:ind + min_l], min_l)
#SDR2_1_norm_2=noise_removal.savgold_filter(list_of_floats_SDR2[ind:ind+min_l], min_l)

print("Entropy RPE", calculate_entropy.calculate_entropy(list_of_floats_SDR1[ind:ind + min_l]))

SDR1_1_norm = [np.float32(x) for x in SDR1_1_norm_1]
SDR2_1_norm = [np.float32(x) for x in SDR2_1_norm_2]

#SDR1_1_norm = np.array(SDR1_1_norm_1).round(decimals=3)
#SDR2_1_norm = np.array(SDR2_1_norm_2).round(decimals=3)

print("Entropy NR1", calculate_entropy.calculate_entropy(SDR1_1_norm))

SDR1_2gbytes, SDR2_2gbytes = lossless_quantization.multi_bit_quantization_corrplot(SDR1_1_norm,
                                                                                   SDR2_1_norm,
                                                                                   min_l,
                                                                                   min_l,
                                                                                   Quant_Range,
                                                                                   True, False)

print("Entropy Quant", calculate_entropy.calculate_entropy(SDR1_2gbytes))
SDR1_2, SDR2_2 = int2byte_conversion.intarray_to_bytearray(SDR1_2gbytes, SDR2_2gbytes, Quant_Range)
print("Entropy NR2", calculate_entropy.calculate_entropy(SDR1_2))
#plot_histogram.create_histogram(SDR2_2, 4, ax4)
num_errors, error_dist = erroranderror_distribution.error_distribution(SDR1_2gbytes, SDR2_2gbytes, Quant_Range)

#random.Random(4).shuffle(SDR1_2)
#Savgol.error_bits_gray.append(num_errors)
#Savgol.entropy.append(calculate_entropy.calculate_entropy(SDR1_2))
#Savgol.CR_rate.append((calculate_entropy.calculate_entropy(SDR1_2)) * abs(1 - (2 * (num_errors / (Quant_Range * min_l)))))

#greycodeSDR1_bytes=np.array(np.array(SDR1_2), dtype=np.uint16)
#greycodeSDR2_bytes = np.array(np.array(SDR2_2), dtype=np.uint16)
#############REED SOLOMON CODE BEGINS HERE

SDR1_bincount = binary_count.intarray2binarray(SDR1_2, Quant_Range)
SDR2_bincount = binary_count.intarray2binarray(SDR2_2, Quant_Range)

print("Entropy NR222222", calculate_entropy.calculate_entropy(SDR1_bincount))

#random.Random(4).shuffle(SDR1_bincount)
#random.Random(4).shuffle(SDR2_bincount)

greycode_stringSDR1 = stringify.stringify(SDR1_bincount.astype(np.uint16))
greycode_stringSDR2 = stringify.stringify(SDR2_bincount.astype(np.uint16))
#print("greycode string for SDR1", greycode_stringSDR1, " of length", len(greycode_stringSDR1))
#print("greycode string for SDR2", greycode_stringSDR2, " of length", len(greycode_stringSDR2))

greycodeSDR1_bytes = string_to_bytearray.string_to_bytearray_conversion(8, greycode_stringSDR1)
greycodeSDR2_bytes = string_to_bytearray.string_to_bytearray_conversion(8, greycode_stringSDR2)
    #print("greycode SDR1", greycodeSDR1_bytes, "of length", len(greycodeSDR1_bytes))
    #print("greycode SDR2", greycodeSDR2_bytes, "of length", len(greycodeSDR2_bytes))

random.Random(4).shuffle(greycodeSDR1_bytes)
#raw_data.append(greycodeSDR1_bytes.astype(np.uint16).tobytes())
raw_data=greycodeSDR1_bytes
with open(file_path, "wb") as f:
    f.write(bytearray(greycodeSDR1_bytes))

    raw_data=np.array(raw_data, dtype=np.uint8)

    #print("raw data", raw_data)


#arr = np.array(raw_data, dtype=np.uint8)
# Flatten into 1D vector
#flat_arr = arr.flatten()  # or arr.ravel()


# Convert to binary bytearray
#binary_vector = bytearray(flat_arr)

#random.Random(250).shuffle(binary_vector)
#raw_data=list(binary_vector)

#print("First row", binary_vector)   # bytearray of first row

#sampling_rate = 1
#mean_value = np.mean(greycodeSDR1_bytes)
#fft_result = np.fft.fft(np.array(greycodeSDR1_bytes-mean_value), norm="forward")
#fftData = np.fft.fftshift(fft_result)
#print(np.abs(fftData))
# Frequency axis
#sampling_rate = 1  # Assuming unit sampling rate for simplicity
#frequencies = np.fft.fftfreq(len(greycodeSDR1_bytes), d=1/sampling_rate)
#freq = np.fft.fftshift(frequencies)

#normaliser=max(fftData)
#plt2.plot(freq, np.abs(fftData), label='Before Randomization')
#plt2.specgram(greycodeSDR1_bytes)
#random.Random(4).shuffle(greycodeSDR1_bytes)
#plt2.specgram(greycodeSDR1_bytes)
#mean_value = np.mean(greycodeSDR1_bytes)
#fft_result = np.fft.fft(np.array(greycodeSDR1_bytes-mean_value), norm="forward")
#fftData = np.fft.fftshift(fft_result)
#normaliser=max(fftData)
#max_fft=max(np.abs(fftData))
#plt2.plot(freq, np.abs(fftData), label='After Randomization')


# Displaying the plot
#plt.show()
#plt2.legend()
plt2.show()


# Displaying the plot
#plt.show()




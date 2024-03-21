import random

import matplotlib.pyplot as plt2
import numpy as np

import plot_RSSI
import plot_CFO
import plot_PO
import math
import correlation_calculation
import plot_correlation
import noise_removal
import lossless_quantization
import int2byte_conversion
import erroranderror_distribution
import calculate_entropy
import binary_count
import stringify
import string_to_bytearray
import reedsolomon_codec
import save_to_bin

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
min_length=32768
min_l=min_length
time=range(min_length)
ind=0

Savgol=Category_CR()

with open('C:/Users/prashanth/Desktop/CFO_SC_212_SDR1.txt', 'r') as fin:
    data_read_SDR1 = fin.read()
    last_char_SDR1 = data_read_SDR1[-1]
    if last_char_SDR1 == '\n':
        print("last next line character detected in first sample file")
        data_read_SDR1 = data_read_SDR1[:-1]
with open('C:/Users/prashanth/Desktop/CFO_SC_212_SDR2.txt', 'r') as fin:
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
list_of_floats_SDR1 = [float(x) for x in list_of_strings_SDR1]
list_of_floats_SDR2 = [float(x) for x in list_of_strings_SDR2]
list_of_floats_SDR1 = list(map(lambda x: x*-1 if x < 0 else x, list_of_floats_SDR1))
list_of_floats_SDR2 = list(map(lambda x: x*-1 if x < 0 else x, list_of_floats_SDR2))


SDR1_1_norm=noise_removal.savgold_filter(list_of_floats_SDR1[ind:ind+min_length], min_l)
SDR2_1_norm=noise_removal.savgold_filter(list_of_floats_SDR2[ind:ind+min_length], min_l)

j = 0
labelarray = []
count = 0
Quantseteps = 8

Quant_Range = Quantseteps

SDR1_2gbytes, SDR2_2gbytes = lossless_quantization.multi_bit_quantization_corrplot(SDR1_1_norm,
                                                                                   SDR2_1_norm,
                                                                                   min_l,
                                                                                   min_l,
                                                                                   Quant_Range,
                                                                                   True, False)



SDR1_2, SDR2_2 = int2byte_conversion.intarray_to_bytearray(SDR1_2gbytes, SDR2_2gbytes, Quant_Range)
#plot_histogram.create_histogram(SDR2_2, 4, ax4)
num_errors, error_dist = erroranderror_distribution.error_distribution(SDR1_2gbytes, SDR2_2gbytes)

Savgol.error_bits_gray.append(num_errors)
Savgol.entropy.append(calculate_entropy.calculate_entropy(SDR1_2))
Savgol.CR_rate.append((calculate_entropy.calculate_entropy(SDR1_2)) * abs(1 - 2 * (num_errors / (Quant_Range * min_l))))


#############REED SOLOMON CODE BEGINS HERE

SDR1_bincount = binary_count.intarray2binarray(SDR1_2, Quant_Range)
SDR2_bincount = binary_count.intarray2binarray(SDR2_2, Quant_Range)

greycode_stringSDR1 = stringify.stringify(SDR1_bincount.astype(int))
greycode_stringSDR2 = stringify.stringify(SDR2_bincount.astype(int))
print("greycode string for SDR1", greycode_stringSDR1, " of length", len(greycode_stringSDR1))
print("greycode string for SDR2", greycode_stringSDR2, " of length", len(greycode_stringSDR2))

greycodeSDR1_bytes = string_to_bytearray.string_to_bytearray_conversion(8, greycode_stringSDR1)
greycodeSDR2_bytes = string_to_bytearray.string_to_bytearray_conversion(8, greycode_stringSDR2)
print("greycode SDR1", greycodeSDR1_bytes, "of length", len(greycodeSDR1_bytes))
print("greycode SDR2", greycodeSDR2_bytes, "of length", len(greycodeSDR2_bytes))

number_of_segments=256
segment_size=int(min_length*Quant_Range/(8*number_of_segments))
parity_size=1

parity_complete=0
# RS Decode
while parity_size <= int(32*(min_length*Quant_Range)/(8*number_of_segments)):
    try:
        RS_encode = reedsolomon_codec.RS_encoding(list(greycodeSDR1_bytes[0:segment_size * number_of_segments]),
                                                  segment_size,
                                                  parity_size, number_of_segments)
        print("RS encoding for gray coding is ", list(RS_encode), " with parity byte length ", len(RS_encode))
        RS_decode = reedsolomon_codec.RS_decoding(list(greycodeSDR2_bytes[0:segment_size * number_of_segments]), RS_encode,
                                              segment_size, parity_size, number_of_segments)
    except:
        parity_size = parity_size+1
        print("parity size", parity_size)

    else:
        print("Size of parity", parity_size)
        break

print("Size of complete parity", len(RS_encode))
print("Decoding status with gray codes ", RS_decode == list(greycodeSDR1_bytes[0:segment_size * number_of_segments]))
print("decoded bytes with gray codes ", list(RS_decode), " with byte length ", len(RS_decode))


SDR1_bincount = binary_count.intarray2binarray(SDR1_2, Quant_Range)
SDR2_bincount = binary_count.intarray2binarray(list(RS_decode), 8)
print("SDR1 CR", list(greycodeSDR1_bytes))
print("SDR2 CR", list(RS_decode))

file_path = r'C:\Users\prashanth\Desktop\1byte_array_prescrambling.bin'
save_to_bin.save_byte_array(bytearray(greycodeSDR1_bytes), file_path)


random.shuffle(greycodeSDR1_bytes)
file_path = r'C:\Users\prashanth\Desktop\1byte_array_postscrambling.bin'
save_to_bin.save_byte_array(bytearray(greycodeSDR1_bytes), file_path)


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
min_length=8192
min_l=256
time=range(min_length)
ind=0

Savgol=Category_CR()

with open('C:/Users/prashanth/Desktop/SDR1_RSSI_8bit.txt', 'r') as fin:
    data_read_SDR1 = fin.read()
    last_char_SDR1 = data_read_SDR1[-1]
    if last_char_SDR1 == '\n':
        print("last next line character detected in first sample file")
        data_read_SDR1 = data_read_SDR1[:-1]
with open('C:/Users/prashanth/Desktop/SDR2_RSSI_8bit.txt', 'r') as fin:
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
new_list1, new_list2 = zip(*[
    (a, b) for a, b in zip(list_of_floats_SDR1, list_of_floats_SDR2) if a <= 0
])
#list_of_int_SDR1 = list(map(lambda x: x * -1 if x < 0 else x, list_of_int_SDR1))
list_of_floats_SDR1 = list(new_list1)
list_of_floats_SDR2 = list(new_list2)
#list_of_floats_SDR1 = list(map(lambda x: x*-1 if x < 0 else x, list_of_floats_SDR1))
#list_of_floats_SDR2 = list(map(lambda x: x*-1 if x < 0 else x, list_of_floats_SDR2))


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

SDR1_1_norm=dct.adaptive_dct_filter(list_of_floats_SDR1[ind:ind+min_length])
SDR2_1_norm=dct.adaptive_dct_filter(list_of_floats_SDR2[ind:ind+min_length])

j = 0
labelarray = []
count = 0
Quantseteps = 1

Quant_Range = Quantseteps

SDR1_2gbytes, SDR2_2gbytes = lossless_quantization.multi_bit_quantization_corrplot(SDR1_1_norm,
                                                                                   SDR2_1_norm,
                                                                                   min_length,
                                                                                   min_l,
                                                                                   Quant_Range,
                                                                                   True, False)



SDR1_2, SDR2_2 = int2byte_conversion.intarray_to_bytearray(SDR1_2gbytes, SDR2_2gbytes, Quant_Range)
#plot_histogram.create_histogram(SDR2_2, 4, ax4)
num_errors, error_dist = erroranderror_distribution.error_distribution(SDR1_2gbytes, SDR2_2gbytes, Quant_Range)

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

number_of_segments=2
segment_size=int(min_length*Quant_Range/(8*number_of_segments))
parity_size=1

parity_complete=0
# RS Decode
while parity_size <= int(32*(min_length*Quant_Range)/(8*number_of_segments)):
    try:
        RS_encode = reedsolomon_codec.RS_encoding(list(greycodeSDR1_bytes[0:segment_size * number_of_segments]),
                                                  segment_size,
                                                  parity_size, number_of_segments)
        #print("RS encoding for gray coding is ", list(RS_encode), " with parity byte length ", len(RS_encode))
        RS_decode = reedsolomon_codec.RS_decoding(list(greycodeSDR2_bytes[0:segment_size * number_of_segments]), RS_encode,
                                              segment_size, parity_size, number_of_segments)
    except:
        parity_size = parity_size+1
        #print("parity size", parity_size)

    else:
        print("Size of parity", parity_size)
        break

print("Size of complete parity", len(RS_encode))
print("Decoding status with gray codes ", list(RS_decode) == list(greycodeSDR1_bytes))
print("decoded bytes with gray codes \n", list(RS_decode), " with byte length ", len(RS_decode))
print("Original \n", list(greycodeSDR1_bytes), " with byte length ", len(greycodeSDR1_bytes))


#SDR1_bincount = binary_count.intarray2binarray(SDR1_2, Quant_Range)
#SDR2_bincount = binary_count.intarray2binarray(list(RS_decode), 8)
#print("SDR1 CR", SDR1_bincount)
#print("SDR2 CR", SDR2_bincount)

#file_path = r'C:\Users\prashanth\Desktop\multibyte_array_prescrambling.bin'
#save_to_bin.save_byte_array(bytearray(greycodeSDR1_bytes), file_path)


import matplotlib.pyplot as plt
plt.rcParams['text.usetex'] = True
plt.rcParams.update({'font.family': 'Times New Roman', 'font.size': 50, })

import matplotlib.pyplot as plt2
plt2.rcParams['text.usetex'] = True
plt2.rcParams.update({'font.family': 'Times New Roman', 'font.size': 50, })


# Plotting
#plt.plot(array2, label='Array 2')

minimumsize=min(len(SDR1_bincount), len(SDR2_bincount))

#plt.plot(list(greycodeSDR1_bytes), label='Before shuffling')
mean_value = np.mean(greycodeSDR1_bytes[0:256])
fft_result = np.fft.fft(np.array(greycodeSDR1_bytes[0:256]-mean_value), norm="forward")
fftData = np.fft.fftshift(fft_result)
print(np.abs(fftData))
# Frequency axis
sampling_rate = 1  # Assuming unit sampling rate for simplicity
#frequencies = np.fft.fftfreq(min_length, d=1/sampling_rate)
spec_len=256
frequencies = np.fft.fftfreq(spec_len, d=1/sampling_rate)
freq = np.fft.fftshift(frequencies)

maxfft=1
plt2.plot(freq, np.abs(fftData)/(maxfft), label='Before Shuffling $K_A^I$')


greycode_stringSDR1 = stringify.stringify(SDR1_bincount.astype(int))
greycodeSDR1_bytes = string_to_bytearray.string_to_bytearray_conversion(8, greycode_stringSDR1)
print("gray code SDR1 bytes", greycodeSDR1_bytes)
raw_data=greycodeSDR1_bytes[0:256]

after_PA=[]
for ind in range(0, 256, 64):
    print("Length", len(bytearray(greycodeSDR1_bytes[ind:ind+96])))
    shaoutput=list(hash_encrypt.encrypt_bytes(bytearray(greycodeSDR1_bytes[ind:ind+64])))
    print("shaoutput", len(shaoutput), shaoutput)
    after_PA.extend(shaoutput)
print("Size of PA", len(after_PA))
mean_value = np.mean(after_PA)
fft_result = np.fft.fft(np.array(after_PA-mean_value), norm="forward")
fftData = np.fft.fftshift(fft_result)
#plt2.plot(freq, np.abs(fftData)/(maxfft), label='After SHA512')


#random.Random(4).shuffle(raw_data)
#random.Random(4).shuffle(SDR2_bincount[0:minimumsize])

#np.savetxt('my_list.txt', SDR2_bincount[0:minimumsize], fmt='%d')  # Use '%d' for integers, '%f' for floats

#plt.plot(list(greycodeSDR1_bytes), label='After Shuffling')
#plt2.specgram(greycodeSDR1_bytes)
mean_value = np.mean(raw_data)
fft_result = np.fft.fft(np.array(raw_data-mean_value), norm="forward")
fftData = np.fft.fftshift(fft_result)
plt2.plot(freq, np.abs(fftData)/(maxfft), label='After Shuffling $K_A^R$')

'''mean_value = np.mean(greycodeSDR1_bytes)
fft_result = np.fft.fft(np.array(greycodeSDR1_bytes-mean_value))
fftData = np.fft.fftshift(fft_result)
print(np.abs(fftData))
# Frequency axis
sampling_rate = 1  # Assuming unit sampling rate for simplicity
frequencies = np.fft.fftfreq(min_length, d=1/sampling_rate)
freq = np.fft.fftshift(frequencies)

maxfft=max(fftData)
plt2.plot(freq, np.abs(fftData), label='Before Shuffling')
#plt2.specgram(greycodeSDR1_bytes)
random.Random(4).shuffle(greycodeSDR1_bytes)
#plt2.specgram(greycodeSDR1_bytes)
mean_value = np.mean(greycodeSDR1_bytes)
fft_result = np.fft.fft(np.array(greycodeSDR1_bytes-mean_value))
fftData = np.fft.fftshift(fft_result)

# Frequency axis
#sampling_rate = 1  # Assuming unit sampling rate for simplicity
#frequencies = np.fft.fftfreq(min_length, d=1/sampling_rate)

plt2.plot(freq, np.abs(fftData), label='After Shuffling')
#plt2.plot(greycodeSDR1_bytes, label='After shuffling', color='beige')

# Adding labels and title
plt2.xlabel('Normalised frequency')
plt2.ylabel('Power')
#plt.title('Plot of two arrays')

plt.xlabel('Index')
plt.ylabel('Value')

plt2.xlabel('Normalised frequency')
plt2.ylabel('Amplitude')
# Adding legend
plt.legend()'''

# Displaying the plot
#plt.show()
plt2.xlabel('Normalised frequency')
plt2.ylabel('Amplitude')
plt2.legend()
plt2.show()

#mat=np.reshape(SDR1_bincount.astype(int), (-1, 64))
#print(np.size(np.reshape(SDR1_bincount.astype(int), (-1, 64))))
#file_path = r'C:\Users\prashanth\Desktop\CRforAlINC1MB.txt'
#np.savetxt(file_path, mat, fmt='%d')


#mat=np.reshape(SDR2_bincount.astype(int), (-1, 64))
#print(np.size(np.reshape(SDR2_bincount.astype(int), (-1, 64))))
#file_path = r'C:\Users\prashanth\Desktop\CRforNCBoB1MB.txt'
#np.savetxt(file_path, mat, fmt='%d')



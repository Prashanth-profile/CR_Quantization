import random

import matplotlib.pyplot as plt2
import matplotlib.pyplot as plt
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
from scipy.signal import find_peaks

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
min_length=512
min_l=512
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



j = 0
labelarray = []
count = 0
Quantseteps = 8

file_path = r'C:\Users\prashanth\Desktop\multibyte_array_postscrambling.bin'

Quant_Range = Quantseteps

raw_data=bytearray()
#for ind in range(0, min_length, min_l):
SDR1_1_norm = dct.adaptive_dct_filter(list_of_floats_SDR1[ind:ind + min_l])
SDR2_1_norm = dct.adaptive_dct_filter(list_of_floats_SDR2[ind:ind + min_l])

SDR1_2gbytes, SDR2_2gbytes = lossless_quantization.multi_bit_quantization_corrplot(SDR1_1_norm,
                                                                                   SDR2_1_norm,
                                                                                   min_l,
                                                                                   min_l,
                                                                                   Quant_Range,
                                                                                   True, False)



SDR1_2_dct, SDR2_2_dct = int2byte_conversion.intarray_to_bytearray(SDR1_2gbytes, SDR2_2gbytes, Quant_Range)
num_errors, error_dist = erroranderror_distribution.error_distribution(SDR1_2gbytes, SDR2_2gbytes, Quant_Range)

SDR1_bincount_dct = binary_count.intarray2binarray(SDR1_2_dct, Quant_Range)
SDR2_bincount_dct = binary_count.intarray2binarray(SDR2_2_dct, Quant_Range)

greycode_stringSDR1_dct = stringify.stringify(SDR1_bincount_dct.astype(np.uint16))
greycode_stringSDR2_dct = stringify.stringify(SDR2_bincount_dct.astype(np.uint16))
#print("greycode string for SDR1", greycode_stringSDR1, " of length", len(greycode_stringSDR1))
#print("greycode string for SDR2", greycode_stringSDR2, " of length", len(greycode_stringSDR2))

greycodeSDR1_bytes_dct = string_to_bytearray.string_to_bytearray_conversion(8, greycode_stringSDR1_dct)
greycodeSDR2_bytes_dct = string_to_bytearray.string_to_bytearray_conversion(8, greycode_stringSDR2_dct)

#######################Savgol filter
SDR1_1_norm_sg = noise_removal.savgold_filter(list_of_floats_SDR1[ind:ind + min_l], min_l)
SDR2_1_norm_sg=noise_removal.savgold_filter(list_of_floats_SDR2[ind:ind+min_l], min_l)

#SDR1_1_norm = np.array(SDR1_1_norm_1).round(decimals=3)
#SDR2_1_norm = np.array(SDR2_1_norm_2).round(decimals=3)

SDR1_2gbytes_sg, SDR2_2gbytes_sg = lossless_quantization.multi_bit_quantization_corrplot(SDR1_1_norm_sg,
                                                                                   SDR2_1_norm_sg,
                                                                                   min_l,
                                                                                   min_l,
                                                                                   Quant_Range,
                                                                                   True, False)



SDR1_2_sg, SDR2_2_sg = int2byte_conversion.intarray_to_bytearray(SDR1_2gbytes_sg, SDR2_2gbytes_sg, Quant_Range)

SDR1_bincount = binary_count.intarray2binarray(SDR1_2_sg, Quant_Range)
SDR2_bincount = binary_count.intarray2binarray(SDR2_2_sg, Quant_Range)

greycode_stringSDR1 = stringify.stringify(SDR1_bincount.astype(np.uint16))
greycode_stringSDR2 = stringify.stringify(SDR2_bincount.astype(np.uint16))
#print("greycode string for SDR1", greycode_stringSDR1, " of length", len(greycode_stringSDR1))
#print("greycode string for SDR2", greycode_stringSDR2, " of length", len(greycode_stringSDR2))

greycodeSDR1_bytes = string_to_bytearray.string_to_bytearray_conversion(8, greycode_stringSDR1)
greycodeSDR2_bytes = string_to_bytearray.string_to_bytearray_conversion(8, greycode_stringSDR2)
    #print("greycode SDR1", greycodeSDR1_bytes, "of length", len(greycodeSDR1_bytes))
    #print("greycode SDR2", greycodeSDR2_bytes, "of length", len(greycodeSDR2_bytes))

random.Random(4).shuffle(greycodeSDR1_bytes_dct)

print("binary data", greycodeSDR1_bytes_dct)

random.Random(4).shuffle(greycodeSDR1_bytes)
#raw_data.append(greycodeSDR1_bytes.astype(np.uint16).tobytes())
#raw_data=greycodeSDR1_bytes
#with open(file_path, "wb") as f:
    #f.write(bytearray(greycodeSDR1_bytes))

    #raw_data=np.array(raw_data, dtype=np.uint8)

    #print("raw data", raw_data)


#arr = np.array(raw_data, dtype=np.uint8)
# Flatten into 1D vector
#flat_arr = arr.flatten()  # or arr.ravel()


# Convert to binary bytearray
#binary_vector = bytearray(flat_arr)

#random.Random(250).shuffle(binary_vector)
#raw_data=list(binary_vector)

#print("First row", binary_vector)   # bytearray of first row

x = np.array(greycodeSDR1_bytes_dct) - np.mean(np.array(greycodeSDR1_bytes_dct))
N = len(x)

# FFT and compute magnitude spectrum
fft_vals = np.fft.fft(x)
fft_freqs = np.fft.fftfreq(N, d=1.0)
mag = np.abs(fft_vals) / N

# Only keep positive frequencies
half = N // 2
freqs = fft_freqs[:half]
mag = mag[:half]
thres=np.max(mag)*0.5

# Find peaks above a small threshold
peaks, _ = find_peaks(mag, height=np.max(mag)*0.5)  # adjust 0.2 threshold as needed

#normaliser=max(fftData)
#plt2.plot(freqs, mag, label='Magnitude Spectrum DCT')
plt2.plot(freqs[peaks], mag[peaks], "rx", label='Spectral Peaks DCT')

print("Number of high spectral peaks DCT", len(mag[peaks]))

y = np.array(greycodeSDR1_bytes) - np.mean(np.array(greycodeSDR1_bytes))
N = len(y)

# FFT and compute magnitude spectrum
fft_vals = np.fft.fft(y)
fft_freqs = np.fft.fftfreq(N, d=1.0)
mag = np.abs(fft_vals) / N

# Only keep positive frequencies
half = N // 2
freqs = fft_freqs[:half]
mag = mag[:half]

# Find peaks above a small threshold
peaks, _ = find_peaks(mag, height=thres)  # adjust 0.2 threshold as needed

#normaliser=max(fftData)
#plt2.plot(freqs, mag, label='Magnitude Spectrum SG', color='orange')
plt2.plot(freqs[peaks], mag[peaks], "bo", label='Spectral Peaks SG')
print("Number of high spectral peaks SG", len(mag[peaks]))



# Displaying the plot
#plt.show()
plt2.legend()
plt2.show()


# Displaying the plot
#plt.show()'''

x = np.array(greycodeSDR1_bytes) - np.mean(np.array(greycodeSDR1_bytes))
y=np.array(greycodeSDR1_bytes_dct) - np.mean(np.array(greycodeSDR1_bytes_dct))
# Compute autocorrelation
corr_x = np.correlate(x, x, mode='full')
corr_x = corr_x[corr_x.size // 2:]  # keep positive lags
corr_x /= corr_x[0]               # normalize

corr_y = np.correlate(y, y, mode='full')
corr_y = corr_y[corr_y.size // 2:]  # keep positive lags
corr_y /= corr_y[0]               # normalize

# Plot small lags (0–50)
maxlag = 50
plt.figure(figsize=(8,4))
plt.stem(range(maxlag+1), corr_x[:maxlag + 1], use_line_collection=True, label="DCT", markerfmt='rD')
plt.stem(range(maxlag+1), corr_y[:maxlag + 1], use_line_collection=True, label="Sav. Gol.")
plt.xlabel("Lag")
plt.ylabel("Autocorrelation")
plt.title("Autocorrelation for small lags (0–50)")
plt.grid(True)
plt.legend()
plt.show()




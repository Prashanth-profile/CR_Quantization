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
import matplotlib.pyplot as plt5

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
list_of_int_SDR1 = [float(x) for x in list_of_strings_SDR1]
list_of_int_SDR2 = [float(x) for x in list_of_strings_SDR2]
new_list1, new_list2 = zip(*[
    (a, b) for a, b in zip(list_of_int_SDR1, list_of_int_SDR2) if a < 0
])
list_of_int_SDR1 = list(new_list1)
list_of_int_SDR2 = list(new_list2)

RSSI_8bit_SDR1=Common_Source(list_of_int_SDR1)
RSSI_8bit_SDR2=Common_Source(list_of_int_SDR2)


min_length=262144

#Change this for size of kernel and window
min_l = 65536
window_size = min_l
# Plot Original
time = range(min_l)
xlab = "Freq Raw Sample in Hz"
fontsz=40
plt5.rcParams['text.usetex'] = True
fig3, axis3 = plt5.subplots()
plt5.rcParams.update({'font.family': 'Times New Roman', 'font.size': fontsz, })
plt5.grid()


count=0
win=min_l

No_Filter_8=Category_CR() #Freq offset, with gray code
DCT_2=Category_CR()
DCT_4=Category_CR()
DCT_n_4=Category_CR() #Freq offset, with gray code
DCT_n_3=Category_CR()
DCT_n_2=Category_CR()

maxQuantrange = 20

num_rows = maxQuantrange-1
num_columns = int(min_length/min_l)

quan_size = []
source_entropy=[]
mode = 0

pdf_error_dist=np.zeros(min_l*8)

mode=0
pdf_count=0

for ind in range(0, min_length, min_l):

    for mode in range(6):

        print("Mode::::::::::::::::", mode)
        SDR1_1_norm=np.empty(min_l)
        SDR2_1_norm = np.empty(min_l)
        SDR1_1_norm_1 = np.empty(min_l)
        SDR2_1_norm_2 = np.empty(min_l)

        #RSSI Jana
        if mode == 0:
            print("NR stage 1")
            SDR1_1_norm_1 = RSSI_8bit_SDR1.raw_samples[ind:ind + min_l] #8bit
            SDR2_1_norm_2 = RSSI_8bit_SDR2.raw_samples[ind:ind + min_l]
            SDR1_1_norm = np.array(SDR1_1_norm_1).round(decimals=3)
            SDR2_1_norm = np.array(SDR2_1_norm_2).round(decimals=3)

        #No filter
        elif mode == 1:
            SDR1_1_norm_1 = dct.adaptive_dct_filter_window(RSSI_8bit_SDR1.raw_samples[ind:ind + min_l],
                                                           int(win / 2))  # 32bit DCT
            SDR2_1_norm_2 = dct.adaptive_dct_filter_window(RSSI_8bit_SDR2.raw_samples[ind:ind + min_l], int(win / 2))
            #SDR1_1_norm = SDR1_1_norm_1.astype(int)
            #SDR2_1_norm = SDR2_1_norm_2.astype(int)
            SDR1_1_norm = SDR1_1_norm_1.round(decimals=3)
            SDR2_1_norm = SDR2_1_norm_2.round(decimals=3)

        #Unit Step Kernel
        elif mode == 2:
            SDR1_1_norm_1 = dct.adaptive_dct_filter_window(RSSI_8bit_SDR1.raw_samples[ind:ind + min_l],
                                                           int(win / 3))  # 32bit DCT
            SDR2_1_norm_2 = dct.adaptive_dct_filter_window(RSSI_8bit_SDR2.raw_samples[ind:ind + min_l], int(win / 3))
            #SDR1_1_norm = SDR1_1_norm_1.astype(int)
            #SDR2_1_norm = SDR2_1_norm_2.astype(int)
            SDR1_1_norm = SDR1_1_norm_1.round(decimals=3)
            SDR2_1_norm = SDR2_1_norm_2.round(decimals=3)
            #SDR1_1_norm_8 = noise_removal.savgold_filter(RSSI_8bit_SDR1.raw_samples[ind:ind + min_l],
            #                                           win - 1)  # 8-bit Savgol
            #SDR2_1_norm_8 = noise_removal.savgold_filter(RSSI_8bit_SDR2.raw_samples[ind:ind + min_l], win - 1)
            #SDR1_1_norm = SDR1_1_norm_8.round(decimals=3)
            #SDR2_1_norm = SDR2_1_norm_8.round(decimals=3)


        #Gaussian Kernel
        elif mode == 3:
            SDR1_1_norm_1 = dct.adaptive_dct_filter_window(RSSI_8bit_SDR1.raw_samples[ind:ind + min_l],
                                                           int(win / 4))  # 32bit DCT
            SDR2_1_norm_2 = dct.adaptive_dct_filter_window(RSSI_8bit_SDR2.raw_samples[ind:ind + min_l], int(win / 4))
            #SDR1_1_norm = SDR1_1_norm_1.astype(int)
            #SDR2_1_norm = SDR2_1_norm_2.astype(int)
            SDR1_1_norm = SDR1_1_norm_1.round(decimals=3)
            SDR2_1_norm = SDR2_1_norm_2.round(decimals=3)

        #elif mode == 4:
            #SDR1_1_norm_1 = dct.adaptive_dct_filter(RSSI_8bit_SDR1.raw_samples[ind:ind + min_l])  # 32bit DCT
            #SDR2_1_norm_2 = dct.adaptive_dct_filter(RSSI_8bit_SDR2.raw_samples[ind:ind + min_l])
            #SDR1_1_norm_1 = dct.adaptive_dct_filter_window(RSSI_8bit_SDR1.raw_samples[ind:ind + min_l], 4)  # 32bit DCT
            #SDR2_1_norm_2 = dct.adaptive_dct_filter_window(RSSI_8bit_SDR2.raw_samples[ind:ind + min_l], 4)
            #SDR1_1_norm = SDR1_1_norm_1.astype(int)
            #SDR2_1_norm = SDR2_1_norm_2.astype(int)
            #SDR1_1_norm = SDR1_1_norm_1.round(decimals=3)
            #SDR2_1_norm = SDR2_1_norm_2.round(decimals=3)
            #SDR1_1_norm = SDR1_1_norm_1.round(decimals=3)
            #SDR2_1_norm = SDR2_1_norm_2.round(decimals=3)
            #SDR1_1_norm=SDR1_1_norm_8.round(decimals=3)
            #SDR2_1_norm=SDR2_1_norm_8.round(decimals=3)


        elif mode == 5:
            SDR1_1_norm_1 = dct.adaptive_dct_filter(RSSI_8bit_SDR1.raw_samples[ind:ind + min_l]) #32bit DCT
            SDR2_1_norm_2 = dct.adaptive_dct_filter(RSSI_8bit_SDR2.raw_samples[ind:ind + min_l])
            #SDR1_1_norm = SDR1_1_norm_1.astype(int)
            #SDR2_1_norm = SDR2_1_norm_2.astype(int)
            SDR1_1_norm = SDR1_1_norm_1.round(decimals=3)
            SDR2_1_norm = SDR2_1_norm_2.round(decimals=3)



        j = 0
        labelarray = []
        count = 0
        Quantseteps = 8

        for k in range(2, maxQuantrange+1):

            Quant_Range = k

            #else:
            print("Quantize")
            SDR1_2gbytes, SDR2_2gbytes = lossless_quantization.multi_bit_quantization_corrplot(SDR1_1_norm,
                                                                                                   SDR2_1_norm,
                                                                                                   min_l,
                                                                                                   window_size,
                                                                                                   Quant_Range,
                                                                                                   True, False)
            print("N%R stage 2")
            SDR1_2, SDR2_2 = int2byte_conversion.intarray_to_bytearray(SDR1_2gbytes, SDR2_2gbytes, Quant_Range)
            num_errors, error_dist = erroranderror_distribution.error_distribution(SDR1_2gbytes, SDR2_2gbytes, k)

            if mode == 0:
                print("Prsent")
                No_Filter_8.error_bits_gray.append(num_errors)
                sample_entropy = calculate_entropy.calculate_entropy(RSSI_8bit_SDR1.raw_samples[ind:ind + min_l])
                No_Filter_8.entropy.append(sample_entropy)
                entropy=calculate_entropy.calculate_entropy(SDR1_2)
                #No_Filter_8.entropy.append(entropy)
                No_Filter_8.CR_rate.append((entropy) * abs(1 - (2 * (num_errors / (Quant_Range * min_l)))))
                quan_size.append(len(SDR1_2) * k)


            elif mode == 1:
                DCT_n_2.error_bits_gray.append(num_errors)
                #sample_entropy_2 = calculate_entropy.calculate_entropy(RSSI_8bit_SDR1.raw_samples[ind:ind + min_l])
                #DCT_n_2.entropy.append(sample_entropy_2)
                entropy = calculate_entropy.calculate_entropy(SDR1_2)
                #No_Filter_16.entropy.append(entropy)
                DCT_n_2.CR_rate.append((entropy)*abs(1-(2*(num_errors/(Quant_Range*min_l)))))


            elif mode == 2:
                DCT_n_3.error_bits_gray.append(num_errors)
                #Unit_Step.error_bits.append(num_errors_norm)
                entropy = calculate_entropy.calculate_entropy(SDR1_2)
                DCT_n_3.entropy.append(entropy)
                DCT_n_3.CR_rate.append((entropy)*abs(1-(2*(num_errors/(Quant_Range*min_l)))))


            elif mode == 3:
                DCT_n_4.error_bits_gray.append(num_errors)
                # Unit_Step.error_bits.append(num_errors_norm)
                entropy = calculate_entropy.calculate_entropy(SDR1_2)
                DCT_n_4.entropy.append(entropy)
                DCT_n_4.CR_rate.append((entropy) * abs(1 - (2 * (num_errors / (Quant_Range * min_l)))))

            #elif mode == 4:
                #DCT_4.error_bits_gray.append(num_errors)
                #Unit_Step.error_bits.append(num_errors_norm)
                #entropy = calculate_entropy.calculate_entropy(SDR1_2)
                #DCT_4.entropy.append(entropy)
                #DCT_4.CR_rate.append((entropy)*abs(1-(2*(num_errors/(Quant_Range*min_l)))))


            elif mode == 5:
                DCT_2.error_bits_gray.append(num_errors)
                # Unit_Step.error_bits.append(num_errors_norm)
                entropy = calculate_entropy.calculate_entropy(SDR1_2)
                DCT_2.entropy.append(entropy)
                DCT_2.CR_rate.append((entropy) * abs(1 - (2 * (num_errors / (Quant_Range * min_l)))))


            label = f'{k}'
            labelarray.append(label)

mark='o'
mark_cap='D'

print("label", labelarray)

#confidence_interval.plot_confidence_interval(np.array(No_Filter_8.entropy).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "CR Cap. $\eta=$8", 'magenta', mark_cap)
#confidence_interval.plot_confidence_interval(np.array(Gaussian.error_bits_gray).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "Gaussian", 'green', mark)
confidence_interval.plot_confidence_interval(np.array(No_Filter_8.error_bits_gray).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "NF RSSI", 'yellow', mark)
confidence_interval.plot_confidence_interval(np.array(DCT_n_2.error_bits_gray).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "DCT $I=n/2$", 'red', mark)
confidence_interval.plot_confidence_interval(np.array(DCT_n_3.error_bits_gray).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "DCT $I=n/3$", 'black', mark)
confidence_interval.plot_confidence_interval(np.array(DCT_n_4.error_bits_gray).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "DCT $I=n/4$", 'brown', mark)
#confidence_interval.plot_confidence_interval(np.array(DCT_4.error_bits_gray).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "DCT $I=4$", 'blue', mark)
confidence_interval.plot_confidence_interval(np.array(DCT_2.error_bits_gray).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "DCT $I=2$", 'cyan', mark)


plt5.show()
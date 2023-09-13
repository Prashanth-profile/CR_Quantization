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
        self.cost_func=[]
        self.avg_cost=[]


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

min_length=2048

#Change this for size of kernel and window
min_l = 128
window_size = min_l
# Plot Original
time = range(min_l)
xlab = "Freq Raw Sample in Hz"
#plot_CFO.plot_CFO(time, list_of_floats_SDR1[ind:ind + min_l], list_of_floats_SDR2[ind:ind + min_l], ax2, xlab)
fontsz=40
fig3, axis3 = plt3.subplots()
plt3.rcParams.update({'font.family': 'Times New Roman', 'font.size': fontsz, })
plt3.grid()

fig4, axis4 = plt4.subplots()
plt4.rcParams.update({'font.family': 'Times New Roman', 'font.size': fontsz, })
plt4.grid()

count=0
win=min_l

No_Filter=Category_CR() #Freq offset, with gray code
Unit_Step=Category_CR()
Gaussian=Category_CR()
Megha=Category_CR()
#Ali=Category_CR()  #Golay Filter, no gray
Jana=Category_CR()  #No Filter
Aman=Category_CR()  #CFO no gray code
DWT=Category_CR()
Clipping=Category_CR()
Aman_and_Megha=Category_CR()
Savgol=Category_CR()

maxQuantrange = 31

num_rows = maxQuantrange-1
num_columns = int(min_length/min_l)

quan_size = []
mode = 0

cost_per_unit_entropy=0.9
cost_per_unit_biterrors=0.1

for ind in range(0, min_length, min_l):

    for mode in range(8):

        print("Mode::::::::::::::::", mode)

        #RSSI Jana
        if mode == 0:
            SDR1_1_norm = RSSI_SDR1.raw_samples[ind:ind + min_l]
            SDR2_1_norm = RSSI_SDR2.raw_samples[ind:ind + min_l]

        #No filter
        elif mode == 1:
            SDR1_1_norm = CFO_SDR1.raw_samples[ind:ind + min_l]
            SDR2_1_norm = CFO_SDR2.raw_samples[ind:ind + min_l]

        #Unit Step Kernel
        elif mode == 2:
            SDR1_1_norm = noise_removal.window_smoothening(CFO_SDR1.raw_samples[ind:ind + min_l], win)
            SDR2_1_norm = noise_removal.window_smoothening(CFO_SDR2.raw_samples[ind:ind + min_l], win)

        #Gaussian Kernel
        elif mode == 3:
            SDR1_1_norm = noise_removal.gaussian_filtering(CFO_SDR1.raw_samples[ind:ind + min_l], win)
            SDR2_1_norm = noise_removal.gaussian_filtering(CFO_SDR2.raw_samples[ind:ind + min_l], win)

        #Megha DWT
        elif mode == 4:
            SDR1_1_norm = wavelet_transform.wavelet_transform_haar(RSSI_SDR1.raw_samples[ind:ind + min_l], win)
            SDR2_1_norm = wavelet_transform.wavelet_transform_haar(RSSI_SDR2.raw_samples[ind:ind + min_l], win)

        #DWT with CFO
        elif mode == 5:
            SDR1_1_norm = wavelet_transform.wavelet_transform_haar(CFO_SDR1.raw_samples[ind:ind + min_l], win)
            SDR2_1_norm = wavelet_transform.wavelet_transform_haar(CFO_SDR2.raw_samples[ind:ind + min_l], win)

        #Mode 6 means clipping
        elif mode == 6:
            SDR1_1_norm = CFO_SDR1.raw_samples[ind:ind + min_l]
            SDR2_1_norm = CFO_SDR2.raw_samples[ind:ind + min_l]

        elif mode == 7:
            SDR1_1_norm=noise_removal.savgold_filter(CFO_SDR1.raw_samples[ind:ind + min_l], win)
            SDR2_1_norm=noise_removal.savgold_filter(CFO_SDR2.raw_samples[ind:ind + min_l], win)


        j = 0
        labelarray = []
        count = 0
        Quantseteps = 8

        for k in range(2, maxQuantrange+1):

            Quant_Range = k
            # SDR1_2gbytes=[]
            # SDR2_2gbytes = []

            # Output is an integer array/list
            # SDR1_2gbytes, SDR2_2gbytes=lossless_quantization.multi_bit_dynamic_quantization_corrplot(list_of_floats_SDR1, list_of_floats_SDR2, min_length, Quant_Range, True, ind)

            if (mode!=6):
                SDR1_2gbytes, SDR2_2gbytes = lossless_quantization.multi_bit_quantization_corrplot(SDR1_1_norm,
                                                                                                   SDR2_1_norm,
                                                                                                   min_l,
                                                                                                   window_size,
                                                                                                   Quant_Range,
                                                                                                   True, False)
                #print("After", Quant_Range, " bit gray code quantization", SDR1_2gbytes, " and ", SDR2_2gbytes, "of length",
                #      len(SDR1_2gbytes), "and", len(SDR2_2gbytes))

                # Output is an integer array/list
                # SDR1_2bytes, SDR2_2bytes=lossless_quantization.multi_bit_dynamic_quantization_corrplot(list_of_floats_SDR1, list_of_floats_SDR2, min_length, Quant_Range, False, ind)
                SDR1_2bytes, SDR2_2bytes = lossless_quantization.multi_bit_quantization_corrplot(SDR1_1_norm,
                                                                                                 SDR2_1_norm,
                                                                                                 min_l,
                                                                                                 window_size,
                                                                                                 Quant_Range,
                                                                                                 False, False)
            else:
                SDR1_2gbytes, SDR2_2gbytes = lossless_quantization.multi_bit_quantization_corrplot(SDR1_1_norm,
                                                                                                   SDR2_1_norm,
                                                                                                   min_l,
                                                                                                   window_size,
                                                                                                   Quant_Range,
                                                                                                   True, True)
                SDR1_2bytes, SDR2_2bytes = lossless_quantization.multi_bit_quantization_corrplot(SDR1_1_norm,
                                                                                                 SDR2_1_norm,
                                                                                                 min_l,
                                                                                                 window_size,
                                                                                                 Quant_Range,
                                                                                                 False, True)
            #print("After", Quant_Range, " two bit code", SDR1_2bytes, " and ", SDR2_2bytes, "of length", len(SDR1_2bytes), "and",
            #      len(SDR2_2bytes))

            SDR1_2, SDR2_2 = int2byte_conversion.intarray_to_bytearray(SDR1_2bytes, SDR2_2bytes, Quant_Range)
            #plot_histogram.create_histogram(SDR2_2, 4, ax4)
            num_errors, error_dist = erroranderror_distribution.error_distribution(SDR1_2gbytes, SDR2_2gbytes)
            num_errors_norm, error_dist_norm = erroranderror_distribution.error_distribution(SDR1_2bytes, SDR2_2bytes)

            floor_diff=[abs(x - y) for x, y in zip(SDR1_2, SDR2_2)]

            # Adjust spacing between subplots

            # print("Number of errors after ", i, " bit gray code Quantization is ", num_errors, " with maximum dynamic range", error_dist)

            if mode == 0:
                Jana.error_bits_gray.append(num_errors)
                Jana.error_bits.append(num_errors_norm)
                entropy=calculate_entropy.calculate_entropy(SDR1_2)
                Jana.entropy.append(entropy)
                Jana.CR_rate.append(entropy * abs(1 - 2 * (num_errors / (Quant_Range * min_l))))
                #print("Jana CR rate", Jana.CR_rate)
                quan_size.append(len(SDR1_2) * k)
                #print("Quant size", quan_size)
                cost_func = ((entropy / Quant_Range) * cost_per_unit_entropy) + ((1-(num_errors / (k * min_l))) * cost_per_unit_biterrors)
                Jana.cost_func.append(1-cost_func)

            elif mode == 1:
                No_Filter.error_bits_gray.append(num_errors)
                Aman.error_bits.append(num_errors_norm)
                entropy = calculate_entropy.calculate_entropy(SDR1_2)
                No_Filter.entropy.append(entropy)
                No_Filter.CR_rate.append(entropy*abs(1-2*(num_errors/(Quant_Range*min_l))))
                Aman.CR_rate.append((calculate_entropy.calculate_entropy(SDR1_2)) * abs(1 - 2 * (num_errors_norm/(Quant_Range * min_l))))
                cost_func = ((entropy / Quant_Range) * cost_per_unit_entropy) + ((1-(num_errors / (k * min_l))) * cost_per_unit_biterrors)
                No_Filter.cost_func.append(1-cost_func)

            elif mode == 2:
                Unit_Step.error_bits_gray.append(num_errors)
                Unit_Step.error_bits.append(num_errors_norm)
                entropy = calculate_entropy.calculate_entropy(SDR1_2)
                Unit_Step.entropy.append(entropy)
                Unit_Step.CR_rate.append(entropy*abs(1-2*(num_errors/(Quant_Range*min_l))))
                cost_func = ((entropy / Quant_Range) * cost_per_unit_entropy) + ((1-(num_errors / (k * min_l))) * cost_per_unit_biterrors)
                Unit_Step.cost_func.append(1-cost_func)

            elif mode == 3:
                Gaussian.error_bits_gray.append(num_errors)
                Gaussian.error_bits.append(num_errors_norm)
                entropy = calculate_entropy.calculate_entropy(SDR1_2)
                Gaussian.entropy.append(entropy)
                Gaussian.CR_rate.append(entropy*abs(1-2*(num_errors/(Quant_Range*min_l))))
                cost_func = ((entropy / Quant_Range) * cost_per_unit_entropy) + ((1-(num_errors / (k * min_l))) * cost_per_unit_biterrors)
                Gaussian.cost_func.append(1-cost_func)

            elif mode == 4:
                Megha.error_bits_gray.append(num_errors)
                Megha.error_bits.append(num_errors_norm)
                entropy = calculate_entropy.calculate_entropy(SDR1_2)
                Megha.entropy.append(entropy)
                Megha.CR_rate.append(entropy * abs(1 - 2 * (num_errors / (Quant_Range * min_l))))
                cost_func = ((entropy / Quant_Range) * cost_per_unit_entropy) + ((1-(num_errors / (k * min_l))) * cost_per_unit_biterrors)
                Megha.cost_func.append(1-cost_func)

            elif mode == 5:
                DWT.error_bits_gray.append(num_errors)
                DWT.error_bits.append(num_errors_norm)
                entropy = calculate_entropy.calculate_entropy(SDR1_2)
                DWT.entropy.append(entropy)
                DWT.CR_rate.append(entropy * abs(1 - 2 * (num_errors / (Quant_Range * min_l))))
                cost_func = ((entropy / Quant_Range) * cost_per_unit_entropy) + ((1-(num_errors / (k * min_l))) * cost_per_unit_biterrors)
                DWT.cost_func.append(1-cost_func)

            elif mode == 6:
                Clipping.error_bits_gray.append(num_errors)
                Clipping.error_bits.append(num_errors_norm)
                entropy = calculate_entropy.calculate_entropy(SDR1_2)
                Clipping.entropy.append(entropy)
                Clipping.CR_rate.append(entropy * abs(1 - 2 * (num_errors / (Quant_Range * min_l))))
                cost_func = ((entropy / Quant_Range) * cost_per_unit_entropy) + ((1-(num_errors / (k * min_l))) * cost_per_unit_biterrors)
                Clipping.cost_func.append(1-cost_func)

            elif mode == 7:
                Savgol.error_bits_gray.append(num_errors)
                Savgol.error_bits.append(num_errors_norm)
                entropy = calculate_entropy.calculate_entropy(SDR1_2)
                Savgol.entropy.append(entropy)
                Savgol.CR_rate.append(entropy * abs(1 - 2 * (num_errors / (Quant_Range * min_l))))
                cost_func = ((entropy / Quant_Range) * cost_per_unit_entropy) + ((1-(num_errors / (k * min_l))) * cost_per_unit_biterrors)
                Savgol.cost_func.append(1-cost_func)


            label = f'{k}'
            labelarray.append(label)


mark='D'
mark_cap='^'

print("Jana CR rate", Jana.CR_rate)
print("No Filter", No_Filter.CR_rate)

############  DISABLE percentage plots in confidence_interval.py
#confidence_interval.plot_confidence_interval(np.array(Jana.CR_rate).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3,  "Jana CRrate", 'red', mark)
#confidence_interval.plot_confidence_interval(np.array(Jana.entropy).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3,  "Jana Capacity", 'red', mark_cap)

confidence_interval.plot_confidence_interval(np.array(No_Filter.CR_rate).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "NF CRrate", 'blue', mark)
confidence_interval.plot_confidence_interval(np.array(No_Filter.entropy).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "NF Capacity", 'blue', mark_cap)

#confidence_interval.plot_confidence_interval(np.array(Aman.CR_rate).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "Aman CRrate", 'green', mark)
#confidence_interval.plot_confidence_interval(np.array(No_Filter.entropy).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "Aman Capacity", 'green', mark_cap)

#confidence_interval.plot_confidence_interval(np.array(Megha.CR_rate).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "Megha CRrate", 'black', mark)
#confidence_interval.plot_confidence_interval(np.array(Megha.entropy).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "Megha Capacity", 'black', mark_cap)

confidence_interval.plot_confidence_interval(np.array(Unit_Step.CR_rate).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "US CRrate", 'red', mark)
confidence_interval.plot_confidence_interval(np.array(Unit_Step.entropy).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "US Capacity", 'red', mark_cap)

confidence_interval.plot_confidence_interval(np.array(DWT.CR_rate).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "DWT CRrate", 'black', mark)
confidence_interval.plot_confidence_interval(np.array(DWT.entropy).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "DWT Capacity", 'black', mark_cap)

confidence_interval.plot_confidence_interval(np.array(Savgol.CR_rate).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "Savgol CRrate", 'cyan', mark)
confidence_interval.plot_confidence_interval(np.array(Savgol.entropy).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "Savgol Capacity", 'cyan', mark_cap)

confidence_interval.plot_confidence_interval(np.array(Gaussian.CR_rate).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "Gauss CRrate", 'green', mark)
confidence_interval.plot_confidence_interval(np.array(Gaussian.entropy).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "Gauss Capacity", 'green', mark_cap)


print("Jana", Jana.cost_func, len(Jana.cost_func))
Jana.avg_cost=confidence_interval.mean_of_the_matrix(np.array(Jana.cost_func).reshape(num_columns, num_rows).transpose())
Unit_Step.avg_cost=confidence_interval.mean_of_the_matrix(np.array(Unit_Step.cost_func).reshape(num_columns, num_rows).transpose())
Savgol.avg_cost=confidence_interval.mean_of_the_matrix(np.array(Savgol.cost_func).reshape(num_columns, num_rows).transpose())

print("Jana after mean", Jana.avg_cost, len(Jana.avg_cost))
confidence_interval.plot_confidence_interval(np.array(Gaussian.cost_func).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis4, "Gaussian", 'green', '*')
confidence_interval.plot_confidence_interval(np.array(Unit_Step.cost_func).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis4, "US", 'red', '*')
confidence_interval.plot_confidence_interval(np.array(Savgol.cost_func).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis4, "SavGol", 'cyan', '*')
confidence_interval.plot_confidence_interval(np.array(No_Filter.cost_func).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis4, "NF", 'blue', '*')

plt4.show()
plt3.show()
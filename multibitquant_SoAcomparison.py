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
import os
import histogram_equalization
import kltransform
import dct

print(os.environ['PATH'])
class Common_Source:
    def __init__(self, list_of_float):
        self.raw_samples=list_of_float

class Category_CR:
    def __init__(self):
        self.entropy=[]
        self.CR_rate=[]
        #self.error_bits=[]
        self.error_bits_gray=[]
        self.floor_diff=[]
        self.cost_func=[]
        self.avg_cost=[]


with open('C:/Users/prashanth/Desktop/RSSI_SC_805_SDR1.txt', 'r') as fin:
    data_read_SDR1 = fin.read()
    last_char_SDR1 = data_read_SDR1[-1]
    if last_char_SDR1 == '\n':
        data_read_SDR1 = data_read_SDR1[:-1]
with open('C:/Users/prashanth/Desktop/RSSI_SC_805_SDR2.txt', 'r') as fin:
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

min_length=32768

#Change this for size of kernel and window
min_l = 1024
window_size = min_l
# Plot Original
time = range(min_l)
xlab = "Freq Raw Sample in Hz"
#plot_CFO.plot_CFO(time, list_of_floats_SDR1[ind:ind + min_l], list_of_floats_SDR2[ind:ind + min_l], ax2, xlab)
fontsz=50
#plt3.rcParams.update(plt.rcParamsDefault)
plt3.rcParams['text.usetex'] = True
fig3, axis3 = plt3.subplots()
plt3.rcParams.update({'font.family': 'Times New Roman', 'font.size': fontsz, })
plt3.grid()

#plt4.rcParams.update(plt.rcParamsDefault)
plt4.rcParams['text.usetex'] = True
fig4, axis4 = plt4.subplots()
plt4.rcParams.update({'font.family': 'Times New Roman', 'font.size': fontsz, })
plt4.grid()

# fig2, (ax1, ax4, ax2, ax5, ax3) = plt2.subplots(5, 1)
plt2.rcParams.update(plt.rcParamsDefault)
plt2.rcParams['text.usetex'] = True
plt2.rcParams.update({'font.family': 'Times New Roman', 'font.size': fontsz, })
fig2, ax11 = plt2.subplots()
ax11.grid(True)
plt2.ylabel('Frequency of Occurance')
plt2.xlabel('Integer representation')
#ax2.grid(True)
#ax3.grid(True)
#fig2.text(0.5, 0.04, "Integer representation of Quantized values", ha='center')
#fig2.text(0.04, 0.5, "Frequency of occurance", va='center', rotation='vertical')

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
Hist_equal=Category_CR()
KLT=Category_CR()
Kalman=Category_CR()
DCT=Category_CR()
Butterworth=Category_CR()
Cheybeshev=Category_CR()

maxQuantrange = 31

num_rows = maxQuantrange-1
num_columns = int(min_length/min_l)

quan_size = []
source_entropy=[]
mode = 0

cost_per_unit_entropy=0
cost_per_unit_biterrors=1
cost_optimum_n=0

SDR1_2_histeq=[]
SDR2_2_histeq=[]

pdf_error_dist=np.zeros(min_l*8)

mode=7
pdf_count=0

for ind in range(0, min_length, min_l):

    for mode in range(9):

        print("Mode::::::::::::::::", mode)
        SDR1_1_norm=np.empty(min_l)
        SDR2_1_norm = np.empty(min_l)

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
            SDR1_1_norm = wavelet_transform.wavelet_transform_haar(CFO_SDR1.raw_samples[ind:ind + min_l], win)
            SDR2_1_norm = wavelet_transform.wavelet_transform_haar(CFO_SDR2.raw_samples[ind:ind + min_l], win)

            #SDR1_1_norm = histogram_equalization.hist_equalization(SDR1_1_norm)
            #SDR2_1_norm = histogram_equalization.hist_equalization(SDR2_1_norm)

        #DWT with CFO
        elif mode == 5:
            SDR1_1_norm_klt = noise_removal.window_smoothening(CFO_SDR1.raw_samples[ind:ind + min_l], win)
            SDR2_1_norm_klt = noise_removal.window_smoothening(CFO_SDR2.raw_samples[ind:ind + min_l], win)

            SDR1_1_norm = kltransform.klt_transform(SDR1_1_norm_klt, int(math.sqrt(min_l)))
            SDR2_1_norm = kltransform.klt_transform(SDR2_1_norm_klt, int(math.sqrt(min_l)))

            #SDR1_1_norm = histogram_equalization.hist_equalization(SDR1_1_norm)
            #SDR2_1_norm = histogram_equalization.hist_equalization(SDR2_1_norm)

        #Mode 6 means clipping
        elif mode == 6:
            SDR1_1_norm = CFO_SDR1.raw_samples[ind:ind + min_l]
            SDR2_1_norm = CFO_SDR2.raw_samples[ind:ind + min_l]

        elif mode == 7:
            SDR1_1_norm=noise_removal.savgold_filter(CFO_SDR1.raw_samples[ind:ind + min_l], win)
            SDR2_1_norm=noise_removal.savgold_filter(CFO_SDR2.raw_samples[ind:ind + min_l], win)


        elif mode == 8:
            SDR1_1_norm = dct.adaptive_dct_filter(CFO_SDR1.raw_samples[ind:ind + min_l])
            SDR2_1_norm = dct.adaptive_dct_filter(CFO_SDR2.raw_samples[ind:ind + min_l])

            #SDR1_1_norm = histogram_equalization.hist_equalization(SDR1_1_norm)
            #SDR2_1_norm = histogram_equalization.hist_equalization(SDR2_1_norm)


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
                                                                                                   True, False)

            #print("After", Quant_Range, " two bit code", SDR1_2bytes, " and ", SDR2_2bytes, "of length", len(SDR1_2bytes), "and",
            #      len(SDR2_2bytes))

            SDR1_2, SDR2_2 = int2byte_conversion.intarray_to_bytearray(SDR1_2gbytes, SDR2_2gbytes, Quant_Range)
            '''if mode == 4 or mode==5 or mode==8:
                SDR1_2_histeq = histogram_equalization.hist_equalization(SDR1_2gbytes)
                SDR2_2_histeq = histogram_equalization.hist_equalization(SDR2_2gbytes)
                num_errors, error_dist = erroranderror_distribution.error_distribution(SDR1_2_histeq, SDR2_2_histeq)
            else:
                num_errors, error_dist = erroranderror_distribution.error_distribution(SDR1_2gbytes, SDR2_2gbytes)'''
            #plot_histogram.create_histogram(SDR2_2, 4, ax4)
            num_errors, error_dist = erroranderror_distribution.error_distribution(SDR1_2gbytes, SDR2_2gbytes, k)
            #print("Error distribution length",len(error_dist))
            #num_errors_norm, error_dist_norm = erroranderror_distribution.error_distribution(SDR1_2bytes, SDR2_2bytes)

            floor_diff=[abs(x - y) for x, y in zip(SDR1_2_histeq, SDR2_2_histeq)]

            # Adjust spacing between subplots

            # print("Number of errors after ", i, " bit gray code Quantization is ", num_errors, " with maximum dynamic range", error_dist)

            if mode == 0:
                Jana.error_bits_gray.append(num_errors)
                #Jana.error_bits.append(num_errors_norm)
                entropy=calculate_entropy.calculate_entropy(SDR1_2)
                Jana.entropy.append(entropy)
                Jana.CR_rate.append((entropy) * abs(1 - 2 * (num_errors / (Quant_Range * min_l))))
                #print("Jana CR rate", Jana.CR_rate)
                quan_size.append(len(SDR1_2) * k)
                #print("Quant size", quan_size)
                if k==8:
                    cost_func = ((1 - (entropy / Quant_Range)) * cost_per_unit_entropy) + (
                            (num_errors / (k * min_l)) * cost_per_unit_biterrors) + (
                                            (1 - (k / math.log2(min_l))) * cost_optimum_n)
                    Jana.cost_func.append(cost_func)

            elif mode == 1:
                No_Filter.error_bits_gray.append(num_errors)
                #Aman.error_bits.append(num_errors_norm)
                entropy = calculate_entropy.calculate_entropy(SDR1_2)
                No_Filter.entropy.append(entropy)
                No_Filter.CR_rate.append((entropy)*abs(1-2*(num_errors/(Quant_Range*min_l))))
                Aman.CR_rate.append((entropy) * abs(1 - 2 * (num_errors/(Quant_Range * min_l))))
                #if (k == 8) & (ind == min_l):
                    #plot_histogram.create_histogram(SDR1_2, 4, ax11, f'{k}-No-Fil(SotA)', 'blue')
                if k==6:
                    cost_func = ((1-(entropy / Quant_Range)) * cost_per_unit_entropy) + (
                                (num_errors / (k * min_l)) * cost_per_unit_biterrors) + ((1-(k/math.log2(min_l)))*cost_optimum_n)
                    No_Filter.cost_func.append(cost_func)

            elif mode == 2:
                Unit_Step.error_bits_gray.append(num_errors)
                #Unit_Step.error_bits.append(num_errors_norm)
                entropy = calculate_entropy.calculate_entropy(SDR1_2)
                Unit_Step.entropy.append(entropy)
                Unit_Step.CR_rate.append((entropy)*abs(1-2*(num_errors/(Quant_Range*min_l))))
                #if (k == 8) & (ind==6*min_l):
                    #plot_histogram.create_histogram(SDR1_2, 4, ax1, f'{k}-US', 'red')
                if k==6:
                    cost_func = ((1-(entropy / Quant_Range)) * cost_per_unit_entropy) + (
                                (num_errors / (k * min_l)) * cost_per_unit_biterrors) + ((1-(k/math.log2(min_l)))*cost_optimum_n)
                    Unit_Step.cost_func.append(cost_func)


            elif mode == 3:
                Gaussian.error_bits_gray.append(num_errors)
                #Gaussian.error_bits.append(num_errors_norm)
                entropy = calculate_entropy.calculate_entropy(SDR1_2)
                Gaussian.entropy.append(entropy)
                Gaussian.CR_rate.append((entropy)*abs(1-2*(num_errors/(Quant_Range*min_l))))
                #if (k == 8) & (ind == 2*min_l):
                    #plot_histogram.create_histogram(SDR1_2, 4, ax1, f'{k}-Gauss', 'green')
                if k==6:
                    cost_func = ((1-(entropy / Quant_Range)) * cost_per_unit_entropy) + (
                                (num_errors / (k * min_l)) * cost_per_unit_biterrors) + ((1-(k/math.log2(min_l)))*cost_optimum_n)
                    Gaussian.cost_func.append(cost_func)

            elif mode == 4:
                DWT.error_bits_gray.append(num_errors)
                #Megha.error_bits.append(num_errors_norm)
                entropy = calculate_entropy.calculate_entropy(SDR1_2)
                DWT.entropy.append(entropy)
                DWT.CR_rate.append((entropy) * abs(1 - 2 * (num_errors / (Quant_Range * min_l))))
                if k==6:
                    cost_func = ((1 - (entropy / Quant_Range)) * cost_per_unit_entropy) + (
                            (num_errors / (k * min_l)) * cost_per_unit_biterrors) + (
                                            (1 - (k / math.log2(min_l))) * cost_optimum_n)
                    DWT.cost_func.append(cost_func)

            elif mode == 5:
                KLT.error_bits_gray.append(num_errors)
                #DWT.error_bits.append(num_errors_norm)
                entropy = calculate_entropy.calculate_entropy(SDR1_2)
                KLT.entropy.append(entropy)
                KLT.CR_rate.append((entropy) * abs(1 - 2 * (num_errors / (Quant_Range * min_l))))
                #if (k == 8) & (ind==0):
                    #plot_histogram.create_histogram(SDR1_2, 4, ax1, f'{k}-DWT', 'black')
                if k==6:
                    cost_func = ((1-(entropy / Quant_Range)) * cost_per_unit_entropy) + (
                                (num_errors / (k * min_l)) * cost_per_unit_biterrors) + ((1-(k/math.log2(min_l)))*cost_optimum_n)
                    KLT.cost_func.append(cost_func)

            elif mode == 6:
                Clipping.error_bits_gray.append(num_errors)
                #Clipping.error_bits.append(num_errors_norm)
                entropy = calculate_entropy.calculate_entropy(SDR1_2)
                Clipping.entropy.append(entropy)
                Clipping.CR_rate.append((entropy) * abs(1 - 2 * (num_errors / (Quant_Range * min_l))))
                cost_func = ((1 - (entropy / Quant_Range)) * cost_per_unit_entropy) + (
                        (num_errors / (k * min_l)) * cost_per_unit_biterrors) + (
                                        (1 - (k / math.log2(min_l))) * cost_optimum_n)
                Clipping.cost_func.append(cost_func)

            elif mode == 7:
                Savgol.error_bits_gray.append(num_errors)
                #print("Savgold err", Savgol.error_bits_gray)
                #Savgol.error_bits.append(num_errors_norm)
                sample_entropy = calculate_entropy.calculate_entropy(list_of_floats_SDR1[ind:ind + min_l])
                Savgol.entropy.append(sample_entropy)
                entropy = calculate_entropy.calculate_entropy(SDR1_2)
                Savgol.CR_rate.append((entropy) * abs(1 - 2 * (num_errors / (Quant_Range * min_l))))
                #if (k == 8) & (ind==min_l):
                    #plot_histogram.create_histogram(SDR1_2, 4, ax11, f'{k}-SavGol', 'cyan')
                if k==6:
                    cost_func = ((1-(entropy / Quant_Range)) * cost_per_unit_entropy) + (
                                (num_errors / (k * min_l)) * cost_per_unit_biterrors) + ((1-(k/math.log2(min_l)))*cost_optimum_n)
                    Savgol.cost_func.append(cost_func)
                if k==8:
                    pdf_count=pdf_count+1
                    print("PDF count", pdf_count)
                    pdf_error_dist=pdf_error_dist+error_dist
                    print("PDF error dist", pdf_error_dist)

            elif mode == 8:
                DCT.error_bits_gray.append(num_errors)
                entropy = calculate_entropy.calculate_entropy(SDR1_2)
                DCT.entropy.append(entropy)
                DCT.CR_rate.append((entropy) * abs(1 - 2 * (num_errors / (Quant_Range * min_l))))
                #print("CR rate DCT", DCT.CR_rate)
                #if (k == 8) & (ind==min_l):
                    #plot_histogram.create_histogram(SDR1_2, 4, ax1, f'{k}-HistEqual', 'black')


            label = f'{k}'
            labelarray.append(label)


mark='D'
mark_cap='^'

print("Jana CR rate", Jana.CR_rate)
print("No Filter", No_Filter.CR_rate)

simple_plot.plot_pdf_error(np.array(pdf_error_dist)/pdf_count)

#confidence_interval.plot_confidence_interval(np.array(No_Filter.error_bits_gray).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3,  "NF", 'blue', mark)
#confidence_interval.plot_confidence_interval(np.array(Gaussian.error_bits_gray).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "Gaussian", 'green', mark)
#confidence_interval.plot_confidence_interval(np.array(Unit_Step.error_bits_gray).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3,  "US", 'red', mark)
#confidence_interval.plot_confidence_interval(np.array(Savgol.error_bits_gray).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3,  "Savgol", 'cyan', mark)

#confidence_interval.plot_confidence_interval(np.array(Hist_equal.error_bits_gray).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3,  "Savgol+HistEq", 'cyan', '*')
#confidence_interval.plot_confidence_interval(np.array(Megha.error_bits_gray).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3,  "US+HistEq", 'red', '*')
#confidence_interval.plot_confidence_interval(np.array(DWT.error_bits_gray).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3,  "Gauss+HistEq", 'green', '*')
#confidence_interval.plot_confidence_interval(np.array(err_values_kalman).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3,  "kalman", 'blue', 'D')
#confidence_interval.plot_confidence_interval(np.array(err_values_kalman_gray).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3,  "gray kalman", 'red', 'D')

############  DISABLE percentage plots in confidence_interval.py
#confidence_interval.plot_confidence_interval(np.array(Jana.CR_rate).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3,  "Jana CRrate", 'red', mark)
#confidence_interval.plot_confidence_interval(np.array(Jana.entropy).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3,  "Jana Capacity", 'red', mark_cap)

#confidence_interval.plot_confidence_interval(np.array(Savgol.entropy).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "CR Capacity", 'magenta', mark_cap)
confidence_interval.plot_confidence_interval(np.array(Savgol.CR_rate).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "Savgol CRrate", 'cyan', mark)
#confidence_interval.plot_confidence_interval(np.array(Unit_Step.CR_rate).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "US CRrate", 'red', mark)
#confidence_interval.plot_confidence_interval(np.array(Gaussian.CR_rate).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "Gauss CRrate", 'green', mark)
#confidence_interval.plot_confidence_interval(np.array(DCT.CR_rate).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "DCT CRrate", 'brown', mark)
confidence_interval.plot_confidence_interval(np.array(No_Filter.CR_rate).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "NF CRrate", 'blue', mark)
#confidence_interval.plot_confidence_interval(np.array(DWT.CR_rate).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "DWT CRrate", 'black', mark)
#confidence_interval.plot_confidence_interval(np.array(Jana.CR_rate).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "NF(RSSI) CRrate", 'yellow', mark)

#confidence_interval.plot_confidence_interval(np.array(Aman.CR_rate).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "Aman CRrate", 'green', mark)
#confidence_interval.plot_confidence_interval(np.array(No_Filter.entropy).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "Aman Capacity", 'green', mark_cap)

#confidence_interval.plot_confidence_interval(np.array(Megha.CR_rate).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "US+HistEq CRrate", 'red', '*')
#confidence_interval.plot_confidence_interval(np.array(Megha.entropy).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "Megha Capacity", 'black', mark_cap)

#confidence_interval.plot_confidence_interval(np.array(Unit_Step.CR_rate).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "US CRrate", 'red', mark)
#confidence_interval.plot_confidence_interval(np.array(Unit_Step.entropy).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "US Capacity", 'red', mark_cap)

#confidence_interval.plot_confidence_interval(np.array(Hist_equal.CR_rate).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "SG+HistEq CRrate", 'cyan', '*')
#confidence_interval.plot_confidence_interval(np.array(KLT.CR_rate).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "PCA CRrate", 'orange', mark)
#confidence_interval.plot_confidence_interval(np.array(DWT.CR_rate).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "DWT CRrate(SotA)", 'black', mark_cap)

#confidence_interval.plot_confidence_interval(np.array(Kalman.CR_rate).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "Kalman CRrate", 'yellow', mark)

#confidence_interval.plot_confidence_interval(np.array(Butterworth.CR_rate).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "Butterworth CRrate", 'brown', mark)
#confidence_interval.plot_confidence_interval(np.array(Cheybeshev.CR_rate).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "Chebyshev CRrate", 'magenta', mark)
#confidence_interval.plot_confidence_interval(np.array(Gaussian.entropy).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "Gauss Capacity", 'green', mark_cap)

#print("Source entropy")
#confidence_interval.plot_confidence_interval(np.array(source_entropy).transpose(), np.array(quan_size), labelarray, axis3, "CR capacity", 'magenta', '*')

'''print("Jana", Jana.cost_func, len(Jana.cost_func))
Jana.avg_cost=confidence_interval.mean_of_the_matrix(np.array(Jana.cost_func).reshape(num_columns, num_rows).transpose())
Unit_Step.avg_cost=confidence_interval.mean_of_the_matrix(np.array(Unit_Step.cost_func).reshape(num_columns, num_rows).transpose())
Savgol.avg_cost=confidence_interval.mean_of_the_matrix(np.array(Savgol.cost_func).reshape(num_columns, num_rows).transpose())

print("Jana after mean", Jana.avg_cost, len(Jana.avg_cost))
confidence_interval.plot_confidence_interval(np.array(Gaussian.cost_func).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis4, "Gaussian", 'green', '*')
confidence_interval.plot_confidence_interval(np.array(Unit_Step.cost_func).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis4, "US", 'red', '*')
confidence_interval.plot_confidence_interval(np.array(Savgol.cost_func).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis4, "SavGol", 'cyan', '*')
confidence_interval.plot_confidence_interval(np.array(No_Filter.cost_func).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis4, "NF", 'blue', '*')'''

print("Cost NF", No_Filter.cost_func)
print("Cost US", Unit_Step.cost_func)
print("Cost Gauss", Gaussian.cost_func)
print("Cost HistEqual", KLT.cost_func)
print("Cost Savgol", Savgol.cost_func)
print("Cost DCT", DCT.cost_func)

plt2.show()
plt4.show()
plt3.show()
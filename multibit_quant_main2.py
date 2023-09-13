import matplotlib.pyplot as plt2
import matplotlib.pyplot as plt3
import matplotlib.pyplot as plt4

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
import calculate_entropy
import cr_rate_plot


class correlation_mode(enum.Enum):
    BITWISE_CORRELATION = False
    INTEGER_CORRELATION = False
    FIND_NUMBER_OF_ERRORS = True


min_length = 16384
# Choose index 12 for lower noise representation and 17 for higher noise and 16 for higher noise in gray code
ind = 0

# Set font size
fontsz = 40

#########This variable is the window size: This is used in both lossy and lossless quantization

#######################################CFO##############################################
# Read the text file
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
data_read_SDR1 = data_read_SDR1.replace(',', '.')
data_read_SDR2 = data_read_SDR2.replace(',', '.')

# Split the data based on escape character \n
list_of_strings_SDR1 = data_read_SDR1.split('\n')
list_of_strings_SDR2 = data_read_SDR2.split('\n')

# Convert string to float
list_of_floats_SDR1 = [float(x) for x in list_of_strings_SDR1]
list_of_floats_SDR2 = [float(x) for x in list_of_strings_SDR2]
list_of_floats_SDR1 = list(map(lambda x: x * -1 if x < 0 else x, list_of_floats_SDR1))
list_of_floats_SDR2 = list(map(lambda x: x * -1 if x < 0 else x, list_of_floats_SDR2))

print("Raw sample values \n", list_of_floats_SDR1[ind:ind + min_length], " and \n",
      list_of_floats_SDR2[ind:ind + min_length])

# fig2, (ax1, ax4, ax2, ax5, ax3) = plt2.subplots(5, 1)
plt2.rcParams.update({'font.family': 'Times New Roman', 'font.size': fontsz, })
fig2, (ax2, ax4, ax5) = plt2.subplots(3, 1)
plt2.grid()
plt2.rcParams.update({'font.family': 'Times New Roman', 'font.size': fontsz, })
fig2, axis11 = plt4.subplots()
plt4.grid()
plt2.rcParams['font.family'] = 'Times New Roman'  # Specify the font family
plt2.rcParams['font.size'] = fontsz  # Specify the font size
plt2.xticks(fontsize=fontsz)  # Specify the font size for x-axis tick labels
plt2.yticks(fontsize=fontsz)  # Specify the font size for y-axis tick labels

# Get the legend object
legend2 = plt2.legend()

# Set the font size and font family of the legend
font = {'size': fontsz, 'family': 'Times New Roman'}
for text in legend2.get_texts():
    text.set_fontsize(font['size'])
    text.set_fontfamily(font['family'])

min_l = 1024
window_size = min_l
# Plot Original
time = range(min_l)
xlab = "Freq Raw Sample in Hz"
plot_CFO.plot_CFO(time, list_of_floats_SDR1[ind:ind + min_l], list_of_floats_SDR2[ind:ind + min_l], ax2, xlab)

err_values = []
err_values_gray = []
err_values_unitstep = []
err_values_unitstep_gray = []
err_values_gaus = []
err_values_gaus_gray = []

entropy=[]
entropy_US=[]
entropy_gauss=[]

CR_rate=[]
CR_rate_US=[]
CR_rate_gauss=[]

quan_size = []
a = 0

labelarray = []

for ind in range(0, min_length, min_l):
    for a in range(3):

        if a == 0:
            SDR1_1_norm = list_of_floats_SDR1[ind:ind + min_l]
            SDR2_1_norm = list_of_floats_SDR2[ind:ind + min_l]

        elif a == 1:
            SDR1_1_norm = noise_removal.window_smoothening(list_of_floats_SDR1[ind:ind + min_l], 64)
            SDR2_1_norm = noise_removal.window_smoothening(list_of_floats_SDR2[ind:ind + min_l], 64)

        elif a==2:
            SDR1_1_norm = noise_removal.gaussian_filtering(list_of_floats_SDR1[ind:ind + min_l])
            SDR2_1_norm = noise_removal.gaussian_filtering(list_of_floats_SDR2[ind:ind + min_l])

        print("After Z_score normalization", SDR1_1_norm)
        print("After Z_score normalization", SDR2_1_norm)
        xlab = "Filtered value"
        plot_CFO.plot_CFO(time, SDR1_1_norm, SDR2_1_norm, ax4, xlab)

        #plot_histogram.create_histogram(SDR1_1_norm, 4, ax5, 'SDR1')
        #plot_histogram.create_histogram(SDR2_1_norm, 4, ax5, 'SDR2')

        #plot_histogram.create_histogram(SDR1_1_norm, 4, axis11, 'SDR1')
        #plot_histogram.create_histogram(SDR2_1_norm, 4, axis11, 'SDR2')

        ##### Multi bit Quantization starts
        ######################2 bit quantization
        # The maximum quantization range
        maxQuantrange = 4

        j = 0
        count = 0
        Quantseteps = 8

        Quant_Range = maxQuantrange
        # SDR1_2gbytes=[]
        # SDR2_2gbytes = []

        # Output is an integer array/list
        # SDR1_2gbytes, SDR2_2gbytes=lossless_quantization.multi_bit_dynamic_quantization_corrplot(list_of_floats_SDR1, list_of_floats_SDR2, min_length, Quant_Range, True, ind)
        SDR1_2gbytes, SDR2_2gbytes = lossless_quantization.multi_bit_quantization_corrplot(SDR1_1_norm,
                                                                                           SDR2_1_norm,
                                                                                           min_l,
                                                                                           window_size,
                                                                                           Quant_Range,
                                                                                           True)
        print("After", Quant_Range, " bit gray code quantization", SDR1_2gbytes, " and ", SDR2_2gbytes, "of length",
              len(SDR1_2gbytes), "and", len(SDR2_2gbytes))

        # Output is an integer array/list
        # SDR1_2bytes, SDR2_2bytes=lossless_quantization.multi_bit_dynamic_quantization_corrplot(list_of_floats_SDR1, list_of_floats_SDR2, min_length, Quant_Range, False, ind)
        SDR1_2bytes, SDR2_2bytes = lossless_quantization.multi_bit_quantization_corrplot(SDR1_1_norm,
                                                                                         SDR2_1_norm,
                                                                                         min_l,
                                                                                         window_size,
                                                                                         Quant_Range,
                                                                                         False)
        print("After", Quant_Range, " two bit code", SDR1_2bytes, " and ", SDR2_2bytes, "of length", len(SDR1_2bytes), "and",
              len(SDR2_2bytes))

        SDR1_2, SDR2_2 = int2byte_conversion.intarray_to_bytearray(SDR1_2gbytes, SDR2_2gbytes, Quant_Range)
        # plot_histogram.create_histogram(SDR2_2, 4, ax4)
        num_errors, error_dist = erroranderror_distribution.error_distribution(SDR1_2gbytes, SDR2_2gbytes)
        num_errors_norm, error_dist_norm = erroranderror_distribution.error_distribution(SDR1_2bytes, SDR2_2bytes)

        # Adjust spacing between subplots

        # print("Number of errors after ", i, " bit gray code Quantization is ", num_errors, " with maximum dynamic range", error_dist)

        if correlation_mode.FIND_NUMBER_OF_ERRORS.value == True:
            if a == 0:
                err_values_gray.append(num_errors)
                err_values.append(num_errors_norm)
                entropy.append((calculate_entropy.calculate_entropy(SDR1_2)*Quant_Range)/8)
                CR_rate.append(((calculate_entropy.calculate_entropy(SDR1_2)*Quant_Range)/8)*abs((1-2*(num_errors/(Quant_Range*min_l)))))
                quan_size.append(len(SDR1_2) * 8)

            elif a == 1:
                err_values_unitstep_gray.append(num_errors)
                err_values_unitstep.append(num_errors_norm)
                entropy_US.append((calculate_entropy.calculate_entropy(SDR1_2) * Quant_Range) / 8)
                CR_rate_US.append((calculate_entropy.calculate_entropy(SDR1_2)*Quant_Range/8)*abs((1-2*(num_errors/(Quant_Range*min_l)))))

            else:
                err_values_gaus_gray.append(num_errors)
                err_values_gaus.append(num_errors_norm)
                entropy_gauss.append((calculate_entropy.calculate_entropy(SDR1_2) * Quant_Range) / 8)
                CR_rate_gauss.append((calculate_entropy.calculate_entropy(SDR1_2)*Quant_Range/8)*abs((1-2*(num_errors/(Quant_Range*min_l)))))

        #j = j + 2

####Multi bit quantization stops

print("err1", err_values, quan_size)
print("err1", err_values_unitstep, quan_size)
print("err1", err_values_gaus, quan_size)

print("Max Entropy of NF, US, Gauss", max(entropy), max(entropy_US), max(entropy_gauss))

print("CR rate of NF, US, Gauss", CR_rate, CR_rate_US, CR_rate_gauss)

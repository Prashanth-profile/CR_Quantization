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
class Common_Source_float:
    def __init__(self, list_of_float):
        self.raw_samples=list_of_float

class Common_Source_int:
    def __init__(self, list_of_int):
        self.raw_samples=list_of_int

class Category_CR:
    def __init__(self):
        self.entropy=[]
        self.CR_rate=[]
        #self.error_bits=[]
        self.error_bits_gray_8bit=[]
        self.error_bits_gray_32bit = []
        self.floor_diff=[]
        self.cost_func=[]
        self.avg_cost=[]


#with open('C:/Users/prashanth/Desktop/RSSI_SC_212_SDR1.txt', 'r') as fin:
with open('C:/Users/prashanth/Desktop/RSSI_8bitSDR1.txt', 'r') as fin:
    data_read_SDR1 = fin.read()
    last_char_SDR1 = data_read_SDR1[-1]
    if last_char_SDR1 == '\n':
        data_read_SDR1 = data_read_SDR1[:-1]
with open('C:/Users/prashanth/Desktop/RSSI_8bitSDR2.txt', 'r') as fin:
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
list_of_int_SDR1 = [int(x) for x in list_of_strings_SDR1]
list_of_int_SDR2 = [int(x) for x in list_of_strings_SDR2]
#list_of_floats_SDR1 = list(map(lambda x: x * -1 if x < 0 else x, list_of_floats_SDR1))
#list_of_floats_SDR2 = list(map(lambda x: x * -1 if x < 0 else x, list_of_floats_SDR2))

RSSI_SDR1_8=Common_Source_int(list_of_int_SDR1)
RSSI_SDR2_8=Common_Source_int(list_of_int_SDR2)


with open('C:/Users/prashanth/Desktop/RSSI_32bitSDR1.txt', 'r') as fin:
    data_read_SDR1 = fin.read()
    last_char_SDR1 = data_read_SDR1[-1]
    if last_char_SDR1 == '\n':
        data_read_SDR1 = data_read_SDR1[:-1]
with open('C:/Users/prashanth/Desktop/RSSI_32bitSDR2.txt', 'r') as fin:
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
#list_of_floats_SDR1 = list(map(lambda x: x * -1 if x < 0 else x, list_of_floats_SDR1))
#list_of_floats_SDR2 = list(map(lambda x: x * -1 if x < 0 else x, list_of_floats_SDR2))

RSSI_SDR1_32=Common_Source_float(list_of_floats_SDR1)
RSSI_SDR2_32=Common_Source_float(list_of_floats_SDR2)

No_Filter_32=Category_CR()
DCT_32=Category_CR()
DCT_32__4=Category_CR()
DCT_32_14=Category_CR()
DCT_32_13=Category_CR()
DCT_32_12=Category_CR()
No_Filter_8=Category_CR()
DCT_8=Category_CR()
DCT_8_14=Category_CR()
DCT_8_13=Category_CR()
DCT_8_12=Category_CR()

maxQuantrange = 16
min_length=16384

#Change this for size of kernel and window
min_l = 512
window_size = min_l
win=min_l

num_rows = maxQuantrange-1
num_columns = int(min_length/min_l)

quan_size = []
source_entropy=[]
mode = 0

cost_per_unit_entropy=0
cost_per_unit_biterrors=1
cost_optimum_n=0


for ind in range(0, min_length, min_l):

    for mode in range(6):

        print("Mode::::::::::::::::", mode)
        SDR1_1_norm=np.empty(min_l)
        SDR2_1_norm = np.empty(min_l)

        SDR1_1_norm_float=np.empty(min_l)
        SDR2_1_norm_float=np.empty(min_l)

        #RSSI No filter
        if mode == 0:
            #SDR1_1_norm = RSSI_SDR1_8.raw_samples[ind:ind + min_l] #8bit
            #SDR2_1_norm = RSSI_SDR2_8.raw_samples[ind:ind + min_l]
            SDR1_1_norm = RSSI_SDR1_32.raw_samples[ind:ind + min_l]  # 32bit
            SDR2_1_norm = RSSI_SDR2_32.raw_samples[ind:ind + min_l]

        # RSSI 2 filter coeffs
        elif mode == 1:

            SDR1_1_norm = dct.adaptive_dct_filter(RSSI_SDR1_32.raw_samples[ind:ind + min_l]) #32-bit DCT
            SDR2_1_norm = dct.adaptive_dct_filter(RSSI_SDR2_32.raw_samples[ind:ind + min_l])

        ## RSSI 4 filter coeffs
        elif mode == 2:

            SDR1_1_norm = dct.adaptive_dct_filter_window(RSSI_SDR1_32.raw_samples[ind:ind + min_l],
                                                               2)  # 8-bit DCT
            SDR2_1_norm = dct.adaptive_dct_filter_window(RSSI_SDR2_32.raw_samples[ind:ind + min_l],
                                                               2)

        # RSSI 1/4 filter coeffs
        elif mode == 3:

            SDR1_1_norm = dct.adaptive_dct_filter_window(RSSI_SDR1_32.raw_samples[ind:ind + min_l],
                                                               int(win / 4))  # 8-bit DCT
            SDR2_1_norm = dct.adaptive_dct_filter_window(RSSI_SDR2_32.raw_samples[ind:ind + min_l],
                                                               int(win / 4))

        # # RSSI 1/3 filter coeffs
        elif mode == 4:
            SDR1_1_norm = dct.adaptive_dct_filter_window(RSSI_SDR1_32.raw_samples[ind:ind + min_l],
                                                               int(win / 3))  # 8-bit DCT
            SDR2_1_norm = dct.adaptive_dct_filter_window(RSSI_SDR2_32.raw_samples[ind:ind + min_l],
                                                               int(win / 3))

            #SDR1_1_norm = [round(x) for x in SDR1_1_norm_float]
            #SDR2_1_norm = [round(x) for x in SDR2_1_norm_float]

        # RSSI 1/2 filter coeffs
        elif mode == 5:
            SDR1_1_norm = dct.adaptive_dct_filter_window(RSSI_SDR1_32.raw_samples[ind:ind + min_l],
                                                               int(win / 2))  # 8-bit DCT
            SDR2_1_norm = dct.adaptive_dct_filter_window(RSSI_SDR2_32.raw_samples[ind:ind + min_l],
                                                               int(win / 2))


        j = 0
        labelarray = []
        count = 0
        Quantseteps = 8

        for k in range(2, maxQuantrange + 1):
            Quant_Range = k
            # else:
            SDR1_2gbytes, SDR2_2gbytes = lossless_quantization.multi_bit_quantization_corrplot(SDR1_1_norm,
                                                                                               SDR2_1_norm,
                                                                                               min_l,
                                                                                               window_size,
                                                                                               Quant_Range,
                                                                                               True, False)


            SDR1_2, SDR2_2 = int2byte_conversion.intarray_to_bytearray(SDR1_2gbytes, SDR2_2gbytes, Quant_Range)

            num_errors, error_dist = erroranderror_distribution.error_distribution(SDR1_2gbytes, SDR2_2gbytes, Quant_Range)


            if mode == 0:
                sample_entropy = calculate_entropy.calculate_entropy(list_of_floats_SDR1[ind:ind + min_l])
                No_Filter_32.error_bits_gray_32bit.append(num_errors)
                No_Filter_32.entropy.append(sample_entropy)
                entropy = calculate_entropy.calculate_entropy(SDR1_2)
                No_Filter_32.CR_rate.append((entropy) * abs(1 - 2 * (num_errors / (Quant_Range * min_l))))
                quan_size.append(len(SDR1_2) * k)

            elif mode == 1:
                entropy = calculate_entropy.calculate_entropy(SDR1_2)
                DCT_32.error_bits_gray_32bit.append(num_errors)
                DCT_32.entropy.append(entropy)
                DCT_32.CR_rate.append((entropy)*abs(1-(2*(num_errors/(Quant_Range*min_l)))))

            elif mode == 2:
                entropy = calculate_entropy.calculate_entropy(SDR1_2)
                DCT_32__4.error_bits_gray_32bit.append(num_errors)
                DCT_32__4.entropy.append(entropy)
                DCT_32__4.CR_rate.append((entropy)*abs(1-2*(num_errors/(Quant_Range*min_l))))


            elif mode == 3:
                entropy = calculate_entropy.calculate_entropy(SDR1_2)
                DCT_32_14.error_bits_gray_32bit.append(num_errors)
                DCT_32_14.entropy.append(entropy)
                DCT_32_14.CR_rate.append((entropy)*abs(1-2*(num_errors/(Quant_Range*min_l))))


            elif mode == 4:
                sample_entropy = calculate_entropy.calculate_entropy(list_of_int_SDR1[ind:ind + min_l])
                DCT_32_13.error_bits_gray_32bit.append(num_errors)
                DCT_32_13.entropy.append(sample_entropy)
                entropy = calculate_entropy.calculate_entropy(SDR1_2)
                DCT_32_13.CR_rate.append((entropy) * abs(1 - 2 * (num_errors / (Quant_Range * min_l))))

            elif mode == 5:
                sample_entropy = calculate_entropy.calculate_entropy(list_of_floats_SDR1[ind:ind + min_l])
                DCT_32_12.error_bits_gray_32bit.append(num_errors)
                DCT_32_12.entropy.append(sample_entropy)
                entropy = calculate_entropy.calculate_entropy(SDR1_2)
                DCT_32_12.CR_rate.append((entropy) * abs(1 - 2 * (num_errors / (Quant_Range * min_l))))

            label = f'{k}'
            labelarray.append(label)

mark='o'
mark_cap='D'

fontsz=50
#plt3.rcParams.update(plt.rcParamsDefault)
plt3.rcParams['text.usetex'] = True
fig3, axis3 = plt3.subplots()
plt3.rcParams.update({'font.family': 'Times New Roman', 'font.size': fontsz, })
plt3.grid()


confidence_interval.plot_confidence_interval(np.array(No_Filter_32.entropy).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "CR Cap.", 'magenta', mark_cap)
#confidence_interval.plot_confidence_interval(np.array(DCT_8.entropy).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "CR Cap. 8-bit", 'orange', mark_cap)
confidence_interval.plot_confidence_interval(np.array(DCT_32.CR_rate).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "DCT $I=2$", 'cyan', mark)
confidence_interval.plot_confidence_interval(np.array(DCT_32__4.CR_rate).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "DCT $I=4$", 'blue', mark)
confidence_interval.plot_confidence_interval(np.array(DCT_32_14.CR_rate).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "DCT $I=n/4$", 'brown', mark)
confidence_interval.plot_confidence_interval(np.array(DCT_32_13.CR_rate).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "DCT $I=n/3$", 'yellow', mark)
confidence_interval.plot_confidence_interval(np.array(DCT_32_12.CR_rate).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "DCT $I=n/2$", 'red', mark)
confidence_interval.plot_confidence_interval(np.array(No_Filter_32.CR_rate).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "NF RSSI", 'green', mark)



'''confidence_interval.plot_confidence_interval(np.array(No_Filter_32.error_bits_gray_32bit).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3,  "NF RSSI", 'green', mark)
confidence_interval.plot_confidence_interval(np.array(DCT_32_12.error_bits_gray_32bit).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "DCT $I=n/2$", 'brown', mark)
confidence_interval.plot_confidence_interval(np.array(DCT_32_13.error_bits_gray_32bit).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "DCT $I=n/3$", 'red', mark)
confidence_interval.plot_confidence_interval(np.array(DCT_32_14.error_bits_gray_32bit).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "DCT $I=n/4$", 'yellow', mark)
confidence_interval.plot_confidence_interval(np.array(DCT_32__4.error_bits_gray_32bit).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "DCT $I=4$", 'blue', mark)
confidence_interval.plot_confidence_interval(np.array(DCT_32.error_bits_gray_32bit).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "DCT $I=2$", 'cyan', mark)'''


plt3.show()
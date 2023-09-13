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


class correlation_mode(enum.Enum):
    BITWISE_CORRELATION = False
    INTEGER_CORRELATION = False
    FIND_NUMBER_OF_ERRORS = True


min_length = 8192
# Choose index 12 for lower noise representation and 17 for higher noise and 16 for higher noise in gray code
ind = 0

# Set font size
fontsz = 20

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
fig2, (ax1, ax2, ax3) = plt2.subplots(3, 1)
ax1.grid(True)
ax2.grid(True)
ax3.grid(True)
fig2.text(0.5, 0.04, "Floor Difference Values", ha='center')
fig2.text(0.04, 0.5, "Frequency of occurance", va='center', rotation='vertical')


plt4.rcParams.update({'font.family': 'Times New Roman', 'font.size': fontsz, })
fig4, (axis41, axis42, axis43) = plt4.subplots(3,1)
axis41.grid(True)
axis42.grid(True)
axis43.grid(True)
fig4.text(0.5, 0.04, "Bins", ha='center')
fig4.text(0.04, 0.5, "Occ Count", va='center', rotation='vertical')


plt5.rcParams.update({'font.family': 'Times New Roman', 'font.size': fontsz, })
fig5, (axis51, axis52, axis53) = plt5.subplots(3,1)
axis51.grid(True)
axis52.grid(True)
axis53.grid(True)
fig5.text(0.5, 0.04, "Number of bits disagree", ha='center')
fig5.text(0.04, 0.5, "Frequency of occurance", va='center', rotation='vertical')

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
#plot_CFO.plot_CFO(time, list_of_floats_SDR1[ind:ind + min_l], list_of_floats_SDR2[ind:ind + min_l], ax2, xlab)

fig3, axis3 = plt3.subplots()
plt3.rcParams.update({'font.family': 'Times New Roman', 'font.size': fontsz, })
plt3.grid()
#plt3.plot(range(2, 32), label='Ideal CR capacity', color='red')
count=0
win=min_l

err_values = []
err_values_gray = []
err_values_unitstep = []
err_values_unitstep_gray = []
err_values_gaus = []
err_values_gaus_gray = []
err_values_kalman = []
err_values_kalman_gray = []


entropy=[]
entropy_US=[]
entropy_gauss=[]

CR_rate=[]
CR_rate_US=[]
CR_rate_gauss=[]

maxQuantrange = 31

num_rows = maxQuantrange-1
num_columns = int(min_length/min_l)

quan_size = []
a = 0

#Normalize by variance
#SDR1_1_norm_normalized=normalization_and_standardization.z_score_normalization(list_of_floats_SDR1)
#SDR2_1_norm_normalized=normalization_and_standardization.z_score_normalization(list_of_floats_SDR2)

for ind in range(0, min_length, min_l):

    for a in range(3):

        if a == 0:
            SDR1_1_norm = list_of_floats_SDR1[ind:ind + min_l]
            SDR2_1_norm = list_of_floats_SDR2[ind:ind + min_l]

        elif a == 1:
            SDR1_1_norm = noise_removal.window_smoothening(list_of_floats_SDR1[ind:ind + min_l], win)
            SDR2_1_norm = noise_removal.window_smoothening(list_of_floats_SDR2[ind:ind + min_l], win)

        elif a==2:
            SDR1_1_norm = noise_removal.savgold_filter(list_of_floats_SDR1[ind:ind + min_l], win)
            SDR2_1_norm = noise_removal.savgold_filter(list_of_floats_SDR2[ind:ind + min_l], win)

        #SDR1_1_norm=uniform_quantization.convert_to_divisible_by_5(np.array(SDR1_1_norm))
        #SDR2_1_norm=uniform_quantization.convert_to_divisible_by_5(np.array(SDR2_1_norm))

        '''else:
            SDR1_1_norm=kalman_filter.kalman_filter(list_of_floats_SDR1[ind:ind + min_l])
            SDR2_1_norm = kalman_filter.kalman_filter(list_of_floats_SDR2[ind:ind + min_l])'''

        #print("After Z_score normalization", SDR1_1_norm)
        #print("After Z_score normalization", SDR2_1_norm)
        xlab = "Filtered value"
        #plot_CFO.plot_CFO(time, SDR1_1_norm, SDR2_1_norm, ax4, xlab)

        #plot_histogram.create_histogram(SDR1_1_norm, 4, ax5, 'SDR1')
        #plot_histogram.create_histogram(SDR2_1_norm, 4, ax5, 'SDR2')

        #plot_histogram.create_histogram(SDR1_1_norm, 4, axis11, 'SDR1')
        #plot_histogram.create_histogram(SDR2_1_norm, 4, axis11, 'SDR2')

        ##### Multi bit Quantization starts
        ######################2 bit quantization
        # The maximum quantization range

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
            #print("After", Quant_Range, " two bit code", SDR1_2bytes, " and ", SDR2_2bytes, "of length", len(SDR1_2bytes), "and",
            #      len(SDR2_2bytes))

            SDR1_2, SDR2_2 = int2byte_conversion.intarray_to_bytearray(SDR1_2bytes, SDR2_2bytes, Quant_Range)
            #plot_histogram.create_histogram(SDR2_2, 4, ax4)
            num_errors, error_dist = erroranderror_distribution.error_distribution(SDR1_2gbytes, SDR2_2gbytes)
            num_errors_norm, error_dist_norm = erroranderror_distribution.error_distribution(SDR1_2bytes, SDR2_2bytes)

            floor_diff=[abs(x - y) for x, y in zip(SDR1_2, SDR2_2)]

            # Adjust spacing between subplots

            # print("Number of errors after ", i, " bit gray code Quantization is ", num_errors, " with maximum dynamic range", error_dist)

            if a == 0:
                err_values_gray.append(num_errors)
                err_values.append(num_errors_norm)
                entropy.append(calculate_entropy.calculate_entropy(SDR1_2))
                CR_rate.append(((calculate_entropy.calculate_entropy(SDR1_2)) * abs((1 - 2 * (num_errors / (Quant_Range * min_l))))))
                quan_size.append(len(SDR1_2) * k)
                if (k == 2) & (ind==0):
                    plot_histogram.create_histogram(SDR1_2, 4, axis41, f'{k}-bitNF', 'blue')
                    plot_histogram.create_histogram(floor_diff, 4, ax1, f'{k}-bitNF', 'blue')
                    print("floor diff", floor_diff)
                    plot_histogram.create_histogram(error_dist, 4, axis51, f'{k}-bitNF', 'blue')
                elif (k == 4) & (ind==0):
                    plot_histogram.create_histogram(SDR1_2, 4, axis42, f'{k}-bitNF', 'blue')
                    plot_histogram.create_histogram(floor_diff, 4, ax2, f'{k}-bitNF', 'blue')
                    print("floor diff", floor_diff)
                    plot_histogram.create_histogram(error_dist, 4, axis52, f'{k}-bitNF', 'blue')
                elif (k == 8) & (ind == 0):
                    plot_histogram.create_histogram(SDR1_2, 4, axis43, f'{k}-bitNF', 'blue')
                    plot_histogram.create_histogram(floor_diff, 4, ax3, f'{k}-bitNF', 'blue')
                    print("floor diff", floor_diff)
                    plot_histogram.create_histogram(error_dist, 4, axis53, f'{k}-bitNF', 'blue')

            elif a == 1:
                err_values_unitstep_gray.append(num_errors)
                err_values_unitstep.append(num_errors_norm)
                entropy_US.append(calculate_entropy.calculate_entropy(SDR1_2))
                CR_rate_US.append((calculate_entropy.calculate_entropy(SDR1_2))*abs((1-2*(num_errors/(Quant_Range*min_l)))))
                if (k == 2) & (ind==0):
                    plot_histogram.create_histogram(SDR1_2, 4, axis41, f'{k}-bitUS', 'red')
                    plot_histogram.create_histogram(floor_diff, 4, ax1, f'{k}-bitUS', 'red')
                    print("floor diff", floor_diff)
                    plot_histogram.create_histogram(error_dist, 4, axis51, f'{k}-bitUS', 'red')
                elif (k == 4) & (ind==0):
                    plot_histogram.create_histogram(SDR1_2, 4, axis42, f'{k}-bitUS', 'red')
                    plot_histogram.create_histogram(floor_diff, 4, ax2, f'{k}-bitUS', 'red')
                    print("floor diff", floor_diff)
                    plot_histogram.create_histogram(error_dist, 4, axis52, f'{k}-bitUS', 'red')
                elif (k == 8) & (ind == 0):
                    plot_histogram.create_histogram(SDR1_2, 4, axis43, f'{k}-bitUS', 'red')
                    plot_histogram.create_histogram(floor_diff, 4, ax3, f'{k}-bitUS', 'red')
                    print("floor diff", floor_diff)
                    plot_histogram.create_histogram(error_dist, 4, axis53, f'{k}-bitUS', 'red')

            elif a==2:
                err_values_gaus_gray.append(num_errors)
                err_values_gaus.append(num_errors_norm)
                entropy_gauss.append(calculate_entropy.calculate_entropy(SDR1_2))
                CR_rate_gauss.append((calculate_entropy.calculate_entropy(SDR1_2))*abs((1-2*(num_errors/(Quant_Range*min_l)))))
                if (k == 2) & (ind==0):
                    plot_histogram.create_histogram(SDR1_2, 4, axis41, f'{k}-bitGauss', 'green')
                    plot_histogram.create_histogram(floor_diff, 4, ax1, f'{k}-bitGauss', 'green')
                    print("floor diff", floor_diff)
                    plot_histogram.create_histogram(error_dist, 4, axis51, f'{k}-bitGauss', 'green')
                elif (k == 4) & (ind==0):
                    plot_histogram.create_histogram(SDR1_2, 4, axis42, f'{k}-bitGauss', 'green')
                    plot_histogram.create_histogram(floor_diff, 4, ax2, f'{k}-bitGauss', 'green')
                    print("floor diff", floor_diff)
                    plot_histogram.create_histogram(error_dist, 4, axis52, f'{k}-bitGauss', 'green')
                elif (k == 8) & (ind == 0):
                    plot_histogram.create_histogram(SDR1_2, 4, axis43, f'{k}-bitGauss', 'green')
                    plot_histogram.create_histogram(floor_diff, 4, ax3, f'{k}-bitGauss', 'green')
                    print("floor diff", floor_diff)
                    plot_histogram.create_histogram(error_dist, 4, axis53, f'{k}-bitGauss', 'green')
            '''else:
                err_values_kalman_gray.append(num_errors)
                err_values_kalman.append(num_errors_norm)'''

            label = f'{k}'
            labelarray.append(label)

        #j = j + 2

####Multi bit quantization stops

'''print("err1", err_values, quan_size)
print("err1", err_values_unitstep, quan_size)
print("err1", err_values_gaus, quan_size)

print("entropy=", np.array(entropy).reshape(num_columns, num_rows))
print("entropy US=", np.array(entropy_US).reshape(num_columns, num_rows))
print("entropy Gauss=", np.array(entropy_gauss).reshape(num_columns, num_rows))

############  ENABLE percentage plots in confidence_interval.py
print("error matrix", np.array(err_values).reshape(num_columns, num_rows))
confidence_interval.plot_confidence_interval(np.array(err_values).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "no filter", 'blue', 'o')
confidence_interval.plot_confidence_interval(np.array(err_values_gray).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3,  "gray no filters", 'blue', 's')
confidence_interval.plot_confidence_interval(np.array(err_values_unitstep).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3,  "unit step", 'red', 'o')
confidence_interval.plot_confidence_interval(np.array(err_values_unitstep_gray).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3,  "gray unit step", 'red', 's')
confidence_interval.plot_confidence_interval(np.array(err_values_gaus).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3,  "gaussian", 'green', 'o')
confidence_interval.plot_confidence_interval(np.array(err_values_gaus_gray).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3,  "gray gaussian", 'green', 's')
#confidence_interval.plot_confidence_interval(np.array(err_values_kalman).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3,  "kalman", 'blue', 'D')
#confidence_interval.plot_confidence_interval(np.array(err_values_kalman_gray).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3,  "gray kalman", 'red', 'D')'''

print("entropy=", np.array(entropy))
print("entropy US=", np.array(entropy_US))
print("entropy Gauss=", np.array(entropy_gauss))

mark='P'
mark_cap='v'
'''if win==win[0]:
    mark='D'
    mark_cap='^'
elif win==wind[1]:
    mark='o'
    mark_cap='.'
elif win == wind[2]:
    mark='s'
    mark_cap='1'''

############  DISABLE percentage plots in confidence_interval.py
#confidence_interval.plot_confidence_interval(np.array(err_values).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3, "no filter", 'red', '')
#confidence_interval.plot_confidence_interval(np.array(err_values_unitstep).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3,  "unit step", 'cyan', 'o')
confidence_interval.plot_confidence_interval(np.array(CR_rate_US).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3,  "CRrate US"f'{win}', 'magenta', mark)
#confidence_interval.plot_confidence_interval(np.array(err_values_gaus).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3,  "gaussian", 'black', 's')
confidence_interval.plot_confidence_interval(np.array(CR_rate_gauss).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3,  "CRrate Gauss"f'{win}', 'green', mark)

confidence_interval.plot_confidence_interval(np.array(entropy_US).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3,  "Capacity US"f'{win}', 'magenta', mark_cap)
confidence_interval.plot_confidence_interval(np.array(entropy_gauss).reshape(num_columns, num_rows).transpose(), np.array(quan_size), labelarray, axis3,  "Capacity Guass"f'{win}', 'green', mark_cap)

confidence_interval.plot_confidence_interval(np.array(CR_rate).reshape(num_columns, num_rows).transpose(),
                                             np.array(quan_size), labelarray, axis3, "CRrate NF", 'blue', 'P')
confidence_interval.plot_confidence_interval(np.array(entropy).reshape(num_columns, num_rows).transpose(),
                                             np.array(quan_size), labelarray, axis3, "Capacity NF", 'blue', 'v')


plt3.show()
plt2.show()
plt5.show()
plt4.show()

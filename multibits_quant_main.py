import matplotlib.pyplot as plt2
import matplotlib.pyplot as plt3
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

class correlation_mode(enum.Enum):
    BITWISE_CORRELATION=False
    INTEGER_CORRELATION=False
    FIND_NUMBER_OF_ERRORS=True


min_length=1024
time=range(min_length)
#Choose index 12 for lower noise representation and 17 for higher noise and 16 for higher noise in gray code
ind=0

#########This variable is the window size: This is used in both lossy and lossless quantization
window_size=min_length

#######################################CFO##############################################
#Read the text file
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

#Split the data based on escape character \n
list_of_strings_SDR1 = data_read_SDR1.split('\n')
list_of_strings_SDR2 = data_read_SDR2.split('\n')

#Convert string to float
list_of_floats_SDR1 = [float(x) for x in list_of_strings_SDR1]
list_of_floats_SDR2 = [float(x) for x in list_of_strings_SDR2]
list_of_floats_SDR1 = list(map(lambda x: x*-1 if x < 0 else x, list_of_floats_SDR1))
list_of_floats_SDR2 = list(map(lambda x: x*-1 if x < 0 else x, list_of_floats_SDR2))

# Interpolate between the corresponding elements
#interpolated_list = [a + (b - a) / 2 for a, b in zip(list_of_floats_SDR1, list_of_floats_SDR2)]

# Create two arrays with the interpolated values
#list_of_floats_SDR1 = list_of_floats_SDR1.copy()
#list_of_floats_SDR2 = interpolated_list.copy()

print("Raw sample values \n", list_of_floats_SDR1[ind:ind+min_length], " and \n", list_of_floats_SDR2[ind:ind+min_length])

#fig2, (ax1, ax4, ax2, ax5, ax3) = plt2.subplots(5, 1)
fig2, (ax2, ax4, ax5) = plt2.subplots(3, 1)
min_l=min_length
#Plot Original
time=range(min_l)
plot_CFO.plot_CFO(time, list_of_floats_SDR1[ind:ind+min_l], list_of_floats_SDR2[ind:ind+min_l], ax2)

SDR1_1_norm=list_of_floats_SDR1[ind:ind+min_l]
SDR2_1_norm=list_of_floats_SDR2[ind:ind+min_l]

#SDR1_1_norm=noise_removal.window_smoothening(list_of_floats_SDR1[ind:ind+min_l], 32)
#SDR2_1_norm=noise_removal.window_smoothening(list_of_floats_SDR2[ind:ind+min_l], 32)

#SDR1_1_norm=noise_removal.gaussian_filtering(list_of_floats_SDR1[ind:ind+min_l])
#SDR2_1_norm=noise_removal.gaussian_filtering(list_of_floats_SDR2[ind:ind+min_l])

#SDR1_1_norm=normalization_and_standardization.mean_centering(SDR1_1_norm_noisy)
#SDR2_1_norm=normalization_and_standardization.mean_centering(SDR2_1_norm_noisy)

#SDR1_1_norm = normalization_and_standardization.z_score_normalization(SDR1_1_norm_noisy)
#SDR2_1_norm = normalization_and_standardization.z_score_normalization(SDR2_1_norm_noisy)

#SDR1_1_norm = normalization_and_standardization.min_max_scaling(SDR1_1_norm_noisy)
#SDR2_1_norm = normalization_and_standardization.min_max_scaling(SDR2_1_norm_noisy)
#print("After Z_score normalization", SDR1_1_norm)
#print("After Z_score normalization", SDR2_1_norm)


#SDR1_1_norm = normalization_and_standardization.min_max_scaling(SDR1_1_norm_z)
#SDR2_1_norm = normalization_and_standardization.min_max_scaling(SDR2_1_norm_z)

print("After Z_score normalization", SDR1_1_norm)
print("After Z_score normalization", SDR2_1_norm)
plot_CFO.plot_CFO(time, SDR1_1_norm, SDR2_1_norm, ax4)

plot_histogram.create_histogram(SDR1_1_norm, 4, ax5, 'SDR1')
plot_histogram.create_histogram(SDR2_1_norm, 4, ax5, 'SDR2')


##### Multi bit Quantization starts
######################2 bit quantization
#The maximum quantization range
maxQuantrange=31

err_values = []
err_values_gray = []
quan_size = []

j=0
labelarray=[]
count=0
Quantseteps = 8

for i in range(2,maxQuantrange+1):

    Quant_Range=i

    #Output is an integer array/list
    #SDR1_2gbytes, SDR2_2gbytes=lossless_quantization.multi_bit_dynamic_quantization_corrplot(list_of_floats_SDR1, list_of_floats_SDR2, min_length, Quant_Range, True, ind)
    SDR1_2gbytes, SDR2_2gbytes = lossless_quantization.multi_bit_quantization_corrplot(SDR1_1_norm,
                                                                                               SDR2_1_norm,
                                                                                               min_length,
                                                                                                window_size,
                                                                                                Quant_Range,
                                                                                               True)
    print("After", i, " bit gray code quantization", SDR1_2gbytes, " and ", SDR2_2gbytes, "of length", len(SDR1_2gbytes), "and", len(SDR2_2gbytes))

    # Output is an integer array/list
    #SDR1_2bytes, SDR2_2bytes=lossless_quantization.multi_bit_dynamic_quantization_corrplot(list_of_floats_SDR1, list_of_floats_SDR2, min_length, Quant_Range, False, ind)
    SDR1_2bytes, SDR2_2bytes = lossless_quantization.multi_bit_quantization_corrplot(SDR1_1_norm,
                                                                                             SDR2_1_norm,
                                                                                             min_length,
                                                                                             window_size,
                                                                                             Quant_Range,
                                                                                             False)
    print("After", i, " two bit code", SDR1_2bytes, " and ", SDR2_2bytes, "of length", len(SDR1_2bytes), "and", len(SDR2_2bytes))



    fig1, axes = plt2.subplots(nrows=4, ncols=1)

    time2=range(min_length)
    axes[0].plot(time2, SDR1_2gbytes, color=f'C{i}', label=f'{i}bitGray_SDR1')
    axes[0].plot(time2, SDR2_2gbytes, color=f'C{i+8}', label=f'{i}bitGray_SDR2')
    axes[0].plot(time2, SDR1_2bytes, color=f'C{i+2}', label=f'{i}bit_SDR1')
    axes[0].plot(time2, SDR2_2bytes, color=f'C{i+4}', label=f'{i}bit_SDR2')
    axes[0].set_xlabel("Time Index")
    axes[0].set_ylabel("Quantized Values")
    axes[0].legend()

    SDR1_2, SDR2_2 = int2byte_conversion.intarray_to_bytearray(SDR1_2gbytes, SDR2_2gbytes, Quant_Range)
    #plot_histogram.create_histogram(SDR2_2, 4, ax4)
    num_errors, error_dist = erroranderror_distribution.error_distribution(SDR1_2gbytes, SDR2_2gbytes)
    num_errors_norm, error_dist_norm = erroranderror_distribution.error_distribution(SDR1_2bytes, SDR2_2bytes)

    # Set the positions of the bars
    x = np.arange(len(error_dist))

    bar_width = 0.5
    axes[1].bar(range(len(error_dist)), error_dist, bar_width, color=f'C{1}', label='Gray Code')
    axes[1].set_xlabel("Time Index")
    axes[1].set_ylabel("Number of error bits")
    axes[1].set_title('Number of errors using Gray Code')

    axes[2].bar(range(len(error_dist_norm)), error_dist_norm, bar_width, color=f'C{0}', label='Normal')
    axes[2].set_xlabel("Time Index")
    axes[2].set_ylabel("Number of error bits")
    axes[2].set_title('Number of errors using Normal Code')

    plot_histogram.create_histogram(SDR1_2gbytes, 4, axes[3], 'norm')
    plot_histogram.create_histogram(SDR2_2gbytes, 4, axes[3], 'Gray')


    # Adjust spacing between subplots
    #plt2.tight_layout()

    #print("Number of errors after ", i, " bit gray code Quantization is ", num_errors, " with maximum dynamic range", error_dist)

    if correlation_mode.FIND_NUMBER_OF_ERRORS.value==True:
        ##### FOR GRAY CODES
        #SDR1_2, SDR2_2=int2byte_conversion.intarray_to_bytearray(SDR1_2gbytes, SDR2_2gbytes, Quant_Range)
        #num_errors, error_dist = erroranderror_distribution.error_distribution(SDR1_2, SDR2_2)
        #print("Number of errors after ", i, " bit gray code Quantization is ", num_errors, " with maximum dynamic range", error_dist)
        err_values_gray.append(num_errors)

        #colorgray = f'C{j}'
        #labelgray = f'{i}bG'

        #labelarray.append(labelgray)

        # Bit Wise correlation
        '''if correlation_mode.BITWISE_CORRELATION.value == True:
            bitwisecorr = bitwisecorrelation.maincall_onebit(SDR1_2gbytes, SDR2_2gbytes, i)
            plot_correlation.correlation_plot_multibit(range(len(bitwisecorr)), bitwisecorr, ax4, colorgray, labelgray)

        elif correlation_mode.INTEGER_CORRELATION.value == True:
            min_l = min(len(SDR1_2gbytes), len(SDR2_2gbytes))
            corr_coeff, number_of_samples = correlation_calculation.complete_correlation(min_l, SDR1_2gbytes, SDR2_2gbytes)
            plot_correlation.correlation_plot_multibit(number_of_samples, corr_coeff, ax4, colorgray, labelgray)'''

        #####  FOR NORMAL CODES
        #SDR1_2, SDR2_2 = int2byte_conversion.intarray_to_bytearray(SDR1_2bytes, SDR2_2bytes, Quant_Range)
        #num_errors_norm, error_dist_norm = erroranderror_distribution.error_distribution(SDR1_2, SDR2_2)
        #print("Number of errors after ", i, " bit code Quantization is ", num_errors, " with maximum dynamic range", error_dist)
        err_values.append(num_errors_norm)
        quan_size.append(len(SDR1_2)*8)

        #color = f'C{j+1}'
        label = f'{i}b'
        labelarray.append(label)

        # Bit Wise correlation
        '''if correlation_mode.BITWISE_CORRELATION.value == True:
            bitwisecorr = bitwisecorrelation.maincall_onebit(SDR1_2bytes, SDR2_2bytes, i)
            plot_correlation.correlation_plot_multibit(range(len(bitwisecorr)), bitwisecorr, ax4, color, label)

        elif correlation_mode.INTEGER_CORRELATION.value == True:
            min_l = min(len(SDR1_2bytes), len(SDR2_2bytes))
            corr_coeff, number_of_samples = correlation_calculation.complete_correlation(min_l, SDR1_2gbytes, SDR2_2gbytes)
            plot_correlation.correlation_plot_multibit(number_of_samples, corr_coeff, ax4, color, label)'''
    j=j+2

####Multi bit quantization stops
plt2.show()

fig3, axis3 = plt3.subplots()

simple_plot.percentage_plot_axis(np.array(err_values), np.array(quan_size), labelarray, axis3, 'r-')
simple_plot.percentage_plot_axis(np.array(err_values_gray), np.array(quan_size), labelarray, axis3, 'b-')
plt3.show()

print(err_values)
print(err_values_gray)
print(quan_size)

intercept, coeff= linear_regression.lin_reg(SDR1_2gbytes.reshape(-1,1), SDR2_2gbytes)

print(intercept, coeff)
print(linear_regression.reverse_linear_regression(intercept, coeff, SDR2_2gbytes))

file_path = r'C:\Users\prashanth\Desktop\1byte_array.bin'
save_to_bin.save_byte_array(SDR1_2, file_path)



#simple_plot.percentage_plot(np.array(err_values), np.array(quan_size))
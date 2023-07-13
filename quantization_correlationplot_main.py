import matplotlib.pyplot as plt2
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

class correlation_mode(enum.Enum):
    BITWISE_CORRELATION=False
    INTEGER_CORRELATION=True
    FIND_NUMBER_OF_ERRORS=True


min_length=16
time=range(min_length)
ind=17

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

print("Raw sample values", list_of_floats_SDR1[ind:ind+min_length], " and ", list_of_floats_SDR2[ind:ind+min_length])

#fig2, (ax1, ax4, ax2, ax5, ax3) = plt2.subplots(5, 1)
fig2, (ax2, ax4) = plt2.subplots(2, 1)
min_l=min_length
#Plot Original
time=range(min_l)
plot_CFO.plot_CFO(time, list_of_floats_SDR1[ind:ind+min_l], list_of_floats_SDR2[ind:ind+min_l], ax2)
maxSDR1=max(list_of_floats_SDR1[ind:ind+min_length])
maxSDR2=max(list_of_floats_SDR2[ind:ind+min_length])

minSDR1=min(list_of_floats_SDR1[ind:ind+min_length])
minSDR2=min(list_of_floats_SDR2[ind:ind+min_length])

#print("Number of elements", len(list_of_floats_SDR1), " with max for SDR1", maxSDR1, "at", list_of_floats_SDR1.index(maxSDR1) ," and max at SDR2 ", maxSDR2, " at ", list_of_floats_SDR2.index(maxSDR2))
#print("Number of elements", len(list_of_floats_SDR1), " with min for SDR1", minSDR1, "at", list_of_floats_SDR1.index(minSDR1) ," and min at SDR2 ", minSDR2, " at ", list_of_floats_SDR2.index(minSDR2))

old_error_dist = []
remind=len(list_of_floats_SDR1)%min_length

####Lossy Quantization starts
#MEAN
alpha = 0.01
mean_medbar=True

SDR1_bytes, SDR2_bytes=lossy_quantization.lossy_quantization(list_of_floats_SDR1, list_of_floats_SDR2, min_length, window_size, True, alpha)

#Correlation plot starts here
#min_l=min(len(SDR1_bytes), len(SDR2_bytes))
#corr_coeff, number_of_samples = correlation_calculation.complete_correlation(min_l, list(SDR1_bytes), list(SDR2_bytes))
#plot_correlation.correlation_plot_multibit(number_of_samples, corr_coeff, ax4, '#ff81c0', "Lossy Mean")

#MEDIAN
SDR1_bytes, SDR2_bytes=lossy_quantization.lossy_quantization(list_of_floats_SDR1, list_of_floats_SDR2, min_length, window_size, False, alpha)

#Correlation plot starts here
#min_l=min(len(SDR1_bytes), len(SDR2_bytes))
#corr_coeff, number_of_samples = correlation_calculation.complete_correlation(min_l, list(SDR1_bytes), list(SDR2_bytes))
#plot_correlation.correlation_plot_multibit(number_of_samples, corr_coeff, ax4, '#653700', "Lossy Median")

######Lossy Quantization Ends

###### Lossless quantization starts
######1 bit Quanzization starts
#MEAN
SDR1_mebytes, SDR2_mebytes=lossless_quantization.one_bit_quantization(list_of_floats_SDR1, list_of_floats_SDR2, min_length, window_size, True)
print("After 1 bit mean ", SDR1_mebytes, SDR2_mebytes)

#Correlation plot starts here
#min_l=min(len(SDR1_bytes), len(SDR2_bytes))
#corr_coeff, number_of_samples = correlation_calculation.complete_correlation(min_l, list(SDR1_bytes), list(SDR2_bytes))
#plot_correlation.correlation_plot_multibit(number_of_samples, corr_coeff, ax4, '#dbb40c', "1bit Mean")

#MEDIAN
SDR1_mdbytes, SDR2_mdbytes=lossless_quantization.one_bit_quantization(list_of_floats_SDR1, list_of_floats_SDR2, min_length, window_size, False)
print("After 1 bit median ", SDR1_mdbytes, SDR2_mdbytes)

#Correlation plot starts here
#min_l=min(len(SDR1_bytes), len(SDR2_bytes))
#corr_coeff, number_of_samples = correlation_calculation.complete_correlation(min_l, list(SDR1_bytes), list(SDR2_bytes))
#plot_correlation.correlation_plot_multibit(number_of_samples, corr_coeff, ax4, '#be0119', "1bit Median")

######1 bit Quantization stops

##### Multi bit Quantization starts
######################2 bit quantization
Quant_Range=2

SDR1_2gbytes, SDR2_2gbytes=lossless_quantization.multi_bit_quantization_corrplot(list_of_floats_SDR1, list_of_floats_SDR2, min_length, window_size, Quant_Range, True, ind)
print("After two bit gray code", SDR1_2gbytes, " and ", SDR2_2gbytes)
#plot_histogram.create_histogram(SDR1_2gbytes, 4, ax22)
#plot_histogram.create_histogram(SDR2_2gbytes, 4, ax22)

#time2=range(min_l)

#plot_CFO.plot_CFO_grey(time2, SDR1_2gbytes[ind:ind+min_l], SDR2_2gbytes[ind:ind+min_l], ax1)

SDR1_2bytes, SDR2_2bytes=lossless_quantization.multi_bit_quantization_corrplot(list_of_floats_SDR1, list_of_floats_SDR2, min_length, window_size, Quant_Range, False, ind)
print("After two bit code", SDR1_2bytes, " and ", SDR2_2bytes)
#plot_histogram.create_histogram(SDR1_2bytes, ax11)
#plot_histogram.create_histogram(SDR2_2bytes, ax11)
#time2=range(min_l)
#plot_CFO.plot_CFO(time2, SDR1_2bytes[ind:ind+min_l], SDR2_2bytes[ind:ind+min_l], ax1)

err_values=[]
quan_size=[]

if correlation_mode.FIND_NUMBER_OF_ERRORS.value==True:
    SDR1_2, SDR2_2=int2byte_conversion.intarray_to_bytearray(SDR1_2gbytes, SDR2_2gbytes, Quant_Range)
    num_errors, error_dist = erroranderror_distribution.error_distribution(SDR1_2, SDR2_2)
    print("Number of errors after 2 bit gray code Quantization", num_errors, " with maximum dynamic range", error_dist)
    err_values.append(num_errors)
    quan_size.append(len(SDR1_2)*8)

    SDR1_2, SDR2_2 = int2byte_conversion.intarray_to_bytearray(SDR1_2bytes, SDR2_2bytes, Quant_Range)
    num_errors, error_dist = erroranderror_distribution.error_distribution(SDR1_2, SDR2_2)
    print("Number of errors after 2 bit code Quantization", num_errors, " with maximum dynamic range", error_dist)
    err_values.append(num_errors)
    quan_size.append(len(SDR1_2)*8)


#################4 bit quantization
Quant_Range=4

SDR1_4gbytes, SDR2_4gbytes=lossless_quantization.multi_bit_quantization_corrplot(list_of_floats_SDR1, list_of_floats_SDR2, min_length, window_size, Quant_Range, True, ind)
print("After 4 bit gray code", SDR1_4gbytes, " and ", SDR2_4gbytes)
#time2=range(min_l)
#plot_CFO.plot_CFO_grey(time2, SDR1_4gbytes[ind:ind+min_l], SDR2_4gbytes[ind:ind+min_l], ax4)




SDR1_4bytes, SDR2_4bytes=lossless_quantization.multi_bit_quantization_corrplot(list_of_floats_SDR1, list_of_floats_SDR2, min_length, window_size, Quant_Range, False, ind)
print("After 4 bit code", SDR1_4bytes, " and ", SDR2_4bytes)
#time2=range(min_l)
#plot_CFO.plot_CFO(time2, SDR1_4bytes[ind:ind+min_l], SDR2_4bytes[ind:ind+min_l], ax4)

if correlation_mode.FIND_NUMBER_OF_ERRORS.value==True:
    SDR1_4, SDR2_4 = int2byte_conversion.intarray_to_bytearray(SDR1_4gbytes, SDR2_4gbytes, Quant_Range)
    num_errors, error_dist = erroranderror_distribution.error_distribution(SDR1_4, SDR2_4)
    print("Number of errors after 4 bit gray code Quantization", num_errors, " with maximum dynamic range", error_dist)
    err_values.append(num_errors)
    quan_size.append(len(SDR1_4)*8)

    SDR1_4, SDR2_4 = int2byte_conversion.intarray_to_bytearray(SDR1_4bytes, SDR2_4bytes, Quant_Range)
    num_errors, error_dist = erroranderror_distribution.error_distribution(SDR1_4, SDR2_4)
    print("Number of errors after 4 bit code Quantization", num_errors, " with maximum dynamic range", error_dist)
    err_values.append(num_errors)
    quan_size.append(len(SDR1_4)*8)




########################8 bit quantization
Quant_Range=8

SDR1_8gbytes, SDR2_8gbytes=lossless_quantization.multi_bit_quantization_corrplot(list_of_floats_SDR1, list_of_floats_SDR2, min_length, window_size, Quant_Range, True, ind)
print("After 8 bit gray code", SDR1_8gbytes, " and ", SDR2_8gbytes)
#time2=range(min_l)
#plot_CFO.plot_CFO_grey(time2, SDR1_8gbytes[ind:ind+min_l], SDR2_8gbytes[ind:ind+min_l], ax3)

SDR1_8bytes, SDR2_8bytes=lossless_quantization.multi_bit_quantization_corrplot(list_of_floats_SDR1, list_of_floats_SDR2, min_length, window_size, Quant_Range, False, ind)
print("After 8 bit code", SDR1_8bytes, " and ", SDR2_8bytes)
#time2=range(min_l)
#plot_CFO.plot_CFO(time2, SDR1_8bytes[ind:ind+min_l], SDR2_8bytes[ind:ind+min_l], ax3)

if correlation_mode.FIND_NUMBER_OF_ERRORS.value==True:
    SDR1_8, SDR2_8 = int2byte_conversion.intarray_to_bytearray(SDR1_8gbytes, SDR2_8gbytes, Quant_Range)
    num_errors, error_dist = erroranderror_distribution.error_distribution(SDR1_8, SDR2_8)
    print("Number of errors after 8 bit gray code Quantization", num_errors, " with maximum dynamic range", error_dist)
    err_values.append(num_errors)
    quan_size.append(len(SDR1_8)*8)

    SDR1_8, SDR2_8 = int2byte_conversion.intarray_to_bytearray(SDR1_8bytes, SDR2_8bytes, Quant_Range)
    num_errors, error_dist = erroranderror_distribution.error_distribution(SDR1_8, SDR2_8)
    print("Number of errors after 8 bit code Quantization", num_errors, " with maximum dynamic range", error_dist)
    err_values.append(num_errors)
    quan_size.append(len(SDR1_8)*8)


#Plot Quantized
#time=range(len(list(SDR1_bytes)))
#plot_CFO.plot_CFO(time, list(SDR1_bytes), list(SDR2_bytes), ax5)


#16 bit quantization
Quant_Range=16

SDR1_16gbytes, SDR2_16gbytes=lossless_quantization.multi_bit_quantization_corrplot(list_of_floats_SDR1, list_of_floats_SDR2, min_length, window_size, Quant_Range, True, ind)
print("After 16 bits gray code", SDR1_16gbytes, " and ", SDR2_16gbytes)



SDR1_16bytes, SDR2_16bytes=lossless_quantization.multi_bit_quantization_corrplot(list_of_floats_SDR1, list_of_floats_SDR2, min_length, window_size, Quant_Range, False, ind)
print("After 16 bits code", SDR1_16bytes, " and ", SDR2_16bytes)

if correlation_mode.FIND_NUMBER_OF_ERRORS.value==True:
    SDR1_16, SDR2_16 = int2byte_conversion.intarray_to_bytearray(SDR1_16gbytes, SDR2_16gbytes, Quant_Range)
    num_errors, error_dist = erroranderror_distribution.error_distribution(SDR1_16, SDR2_16)
    print("Number of errors after 16 bit gray code Quantization", num_errors, " with maximum dynamic range", error_dist)
    err_values.append(num_errors)
    quan_size.append(len(SDR1_16)*8)

    SDR1_16, SDR2_16 = int2byte_conversion.intarray_to_bytearray(SDR1_16bytes, SDR2_16bytes, Quant_Range)
    num_errors, error_dist = erroranderror_distribution.error_distribution(SDR1_16, SDR2_16)
    print("Number of errors after 16 bit code Quantization", num_errors, " with maximum dynamic range", error_dist)
    err_values.append(num_errors)
    quan_size.append(len(SDR1_16)*8)





if correlation_mode.BITWISE_CORRELATION.value==True or correlation_mode.INTEGER_CORRELATION.value==True:
    corr_coeff_cfo, number_of_samples_cfo = correlation_calculation.complete_correlation(min_length, list_of_floats_SDR1[ind:], list_of_floats_SDR2[ind:])
    print(corr_coeff_cfo)
    plot_correlation.correlation_plot_multibit(number_of_samples_cfo, corr_coeff_cfo, ax4, '#01ff07', "Correlation of raw samples")

if correlation_mode.BITWISE_CORRELATION.value==True:

    bitwisecorr = bitwisecorrelation.maincall_onebit(list(SDR1_mebytes), list(SDR2_mebytes), 8)
    plot_correlation.correlation_plot_multibit(range(len(bitwisecorr)), bitwisecorr, ax4, '#dbb40c', "1bit Mean")

    # Correlation plot starts here
    bitwisecorr = bitwisecorrelation.maincall_onebit(list(SDR1_mdbytes), list(SDR2_mdbytes), 8)
    plot_correlation.correlation_plot_multibit(range(len(bitwisecorr)), bitwisecorr, ax4, '#be0119', "1bit Median")

    # Bit Wise correlation
    bitwisecorr = bitwisecorrelation.maincall_onebit(SDR1_2gbytes, SDR2_2gbytes, 2)
    plot_correlation.correlation_plot_multibit(range(len(bitwisecorr)), bitwisecorr, ax4, 'b-', "2 bit Gray")

    # Bit Wise correlation
    bitwisecorr = bitwisecorrelation.maincall_onebit(SDR1_2bytes, SDR2_2bytes, 2)
    plot_correlation.correlation_plot_multibit(range(len(bitwisecorr)), bitwisecorr, ax4, 'c-', "2 bit")

    # Bit Wise correlation
    bitwisecorr = bitwisecorrelation.maincall_onebit(SDR1_4gbytes, SDR2_4gbytes, 4)
    plot_correlation.correlation_plot_multibit(range(len(bitwisecorr)), bitwisecorr, ax4, 'g-', "4 bit Gray")

    # Bit Wise correlation
    bitwisecorr = bitwisecorrelation.maincall_onebit(SDR1_4bytes, SDR2_4bytes, 4)
    plot_correlation.correlation_plot_multibit(range(len(bitwisecorr)), bitwisecorr, ax4, 'y-', "4 bit")

    # Bit Wise correlation
    bitwisecorr = bitwisecorrelation.maincall_onebit(SDR1_8gbytes, SDR2_8gbytes, 8)
    plot_correlation.correlation_plot_multibit(range(len(bitwisecorr)), bitwisecorr, ax4, 'r-', "8 bit Gray")

    # Bit Wise correlation
    bitwisecorr = bitwisecorrelation.maincall_onebit(SDR1_8bytes, SDR2_8bytes, 8)
    plot_correlation.correlation_plot_multibit(range(len(bitwisecorr)), bitwisecorr, ax4, 'k-', "8 bit")

    # Bit Wise correlation
    bitwisecorr = bitwisecorrelation.maincall_onebit(SDR1_16gbytes, SDR2_16gbytes, 16)
    plot_correlation.correlation_plot_multibit(range(len(bitwisecorr)), bitwisecorr, ax4, '#1f77b4', "16 bit Gray")

    # Bit Wise correlation
    bitwisecorr = bitwisecorrelation.maincall_onebit(SDR1_16bytes, SDR2_16bytes, 16)
    plot_correlation.correlation_plot_multibit(range(len(bitwisecorr)), bitwisecorr, ax4, 'm-', "16 bit")

elif correlation_mode.INTEGER_CORRELATION.value==True:

    # Correlation plot starts here
    min_l = min(len(SDR1_2gbytes), len(SDR2_2gbytes))
    corr_coeff, number_of_samples = correlation_calculation.complete_correlation(min_l, SDR1_2gbytes, SDR2_2gbytes)
    plot_correlation.correlation_plot_multibit(number_of_samples, corr_coeff, ax4, 'b-', "2 bit Gray")

    # Correlation plot starts here
    min_l = min(len(SDR1_2bytes), len(SDR2_2bytes))
    corr_coeff, number_of_samples = correlation_calculation.complete_correlation(min_l, SDR1_2bytes, SDR2_2bytes)
    plot_correlation.correlation_plot_multibit(number_of_samples, corr_coeff, ax4, 'c-', "2 bit")

    # Correlation plot starts here
    min_l = min(len(SDR1_4gbytes), len(SDR2_4gbytes))
    corr_coeff, number_of_samples = correlation_calculation.complete_correlation(min_l, SDR1_4gbytes, SDR2_4gbytes)
    plot_correlation.correlation_plot_multibit(number_of_samples, corr_coeff, ax4, 'g-', "4 bit Gray")

    # Correlation plot starts here
    min_l = min(len(SDR1_4bytes), len(SDR2_4bytes))
    corr_coeff, number_of_samples = correlation_calculation.complete_correlation(min_l, SDR1_4bytes, SDR2_4bytes)
    plot_correlation.correlation_plot_multibit(number_of_samples, corr_coeff, ax4, 'y-', "4 bit")

    # Correlation plot starts here
    min_l = min(len(SDR1_8gbytes), len(SDR2_8gbytes))
    corr_coeff, number_of_samples = correlation_calculation.complete_correlation(min_l, SDR1_8gbytes, SDR2_8gbytes)
    plot_correlation.correlation_plot_multibit(number_of_samples, corr_coeff, ax4, 'r-', "8 bit Gray")

    # Correlation plot starts here
    min_l = min(len(SDR1_8bytes), len(SDR2_8bytes))
    corr_coeff, number_of_samples = correlation_calculation.complete_correlation(min_l, SDR1_8bytes, SDR2_8bytes)
    plot_correlation.correlation_plot_multibit(number_of_samples, corr_coeff, ax4, 'k-', "8 bit")

    # Correlation plot starts here
    min_l = min(len(SDR1_16gbytes), len(SDR2_16gbytes))
    corr_coeff, number_of_samples = correlation_calculation.complete_correlation(min_l, list(SDR1_16gbytes), list(SDR2_16gbytes))
    plot_correlation.correlation_plot_multibit(number_of_samples, corr_coeff, ax4, '#1f77b4', "16 bit Gray")

    # Correlation plot starts here
    min_l = min(len(SDR1_16bytes), len(SDR2_16bytes))
    corr_coeff, number_of_samples = correlation_calculation.complete_correlation(min_l, list(SDR1_16bytes), list(SDR2_16bytes))
    plot_correlation.correlation_plot_multibit(number_of_samples, corr_coeff, ax4, 'm-', "16 bit")

####Multi bit quantization stops

plt2.show()

print(err_values)
print(quan_size)

simple_plot.auto_plot(np.array(err_values), np.array(quan_size))
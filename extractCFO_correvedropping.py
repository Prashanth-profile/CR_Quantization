import matplotlib.pyplot as plt2
import plot_RSSI
import plot_CFO
import plot_PO
import math
import correlation_calculation
import plot_correlation
import noise_removal
import lossless_quantization
import int2byte_conversion
import binary_count
import stringify
import string_to_bytearray
import random
import hash_encrypt
import save_to_bin

fontsz=40
min_length=256
time=range(min_length)
ind=100
win=256
Quant_Range=8

plt2.rcParams['text.usetex'] = True
plt2.rcParams.update({'font.family': 'Times New Roman', 'font.size': fontsz})
fig2, axis = plt2.subplots()
plt2.grid()

#########################################RSSI########################################
#######################################CFO##############################################
#Read the text file
with open('C:/Users/prashanth/Desktop/CFO_SC_286_SDR1.txt', 'r') as fin:
    data_read_SDR1 = fin.read()
    last_char_SDR1 = data_read_SDR1[-1]
    if last_char_SDR1 == '\n':
        print("last next line character detected in first sample file")
        data_read_SDR1 = data_read_SDR1[:-1]
with open('C:/Users/prashanth/Desktop/CFO_SC_286_SDR2.txt', 'r') as fin:
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
list_of_floats_SDR1 = list(map(lambda x: x*-1 if x < 0 else x, list_of_floats_SDR1))
list_of_floats_SDR2 = list(map(lambda x: x*-1 if x < 0 else x, list_of_floats_SDR2))


SDR1_1_norm=noise_removal.window_smoothening(list_of_floats_SDR1[ind:ind+min_length], win)
SDR2_1_norm=noise_removal.window_smoothening(list_of_floats_SDR2[ind:ind+min_length], win)

print("length", len(list_of_floats_SDR1))

#plot_CFO.plot_CFO(time, list_of_floats_SDR1[ind:ind+min_length], list_of_floats_SDR2[ind:ind+min_length], ax2)

corr_coeff_cfo, number_of_samples_cfo = correlation_calculation.complete_correlation(min_length, list_of_floats_SDR1[ind:ind+min_length],
                                                                             list_of_floats_SDR2[ind:ind+min_length])
corr_coeff_smoothcfo, number_of_samples_smoothcfo = correlation_calculation.complete_correlation(min_length, SDR1_1_norm,
                                                                             SDR2_1_norm)

SDR1_2gbytes, SDR2_2gbytes = lossless_quantization.multi_bit_quantization_corrplot(SDR1_1_norm,
                                                                                   SDR2_1_norm,
                                                                                   min_length,
                                                                                   win,
                                                                                   Quant_Range,
                                                                                   True, False)



SDR1_2, SDR2_2 = int2byte_conversion.intarray_to_bytearray(SDR1_2gbytes, SDR2_2gbytes, Quant_Range)

SDR1_bincount = binary_count.intarray2binarray(SDR1_2, Quant_Range)
SDR2_bincount = binary_count.intarray2binarray(SDR2_2, Quant_Range)

greycode_stringSDR1 = stringify.stringify(SDR1_bincount.astype(int))
greycode_stringSDR2 = stringify.stringify(SDR2_bincount.astype(int))
print("greycode string for SDR1", greycode_stringSDR1, " of length", len(greycode_stringSDR1))
print("greycode string for SDR2", greycode_stringSDR2, " of length", len(greycode_stringSDR2))

greycodeSDR1_bytes = string_to_bytearray.string_to_bytearray_conversion(8, greycode_stringSDR1)
greycodeSDR2_bytes = string_to_bytearray.string_to_bytearray_conversion(8, greycode_stringSDR2)

random.Random(4).shuffle(greycodeSDR2_bytes)

plt2.plot(list(greycodeSDR2_bytes), label='Legitimate')

###################HASH
after_PA=[]
for ind in range(0, 256, 64):
    shaoutput=list(hash_encrypt.encrypt_bytes(bytearray(greycodeSDR1_bytes[ind:ind+64])))
    after_PA.extend(shaoutput)
print("Size of PA", len(after_PA))
plt2.plot(after_PA, label='After SHA512')

##############################################Eavesdropper################################################



with open('C:/Users/prashanth/Desktop/EveAl_CFO_286_SDR3.txt', 'r') as fin:
    EveAl_data_read_SDR3 = fin.read()
    EveAl_last_char_SDR3 = EveAl_data_read_SDR3[-1]
    if EveAl_last_char_SDR3 == '\n':
        print("last next line character detected in second sample file")
        EveAl_data_read_SDR3 = EveAl_data_read_SDR3[:-1]

with open('C:/Users/prashanth/Desktop/EveBob_CFO_286_SDR3.txt', 'r') as fin:
    EveBob_data_read_SDR3 = fin.read()
    EveBob_last_char_SDR3 = EveBob_data_read_SDR3[-1]
    if EveBob_last_char_SDR3 == '\n':
        print("last next line character detected in second sample file")
        EveBob_data_read_SDR3 = EveBob_data_read_SDR3[:-1]

# average = mean(data)
# print(average)
EveAl_data_read_SDR3 = EveAl_data_read_SDR3.replace(',', '.')
EveBob_data_read_SDR3 = EveBob_data_read_SDR3.replace(',', '.')

#Split the data based on escape character \n
EveAl_list_of_strings_SDR3 = EveAl_data_read_SDR3.split('\n')
EveBob_list_of_strings_SDR3 = EveBob_data_read_SDR3.split('\n')

#Convert string to float
EveAl_list_of_floats_SDR3 = [float(x) for x in EveAl_list_of_strings_SDR3]
EveBob_list_of_floats_SDR3 = [float(x) for x in EveBob_list_of_strings_SDR3]
EveAl_list_of_floats_SDR3 = list(map(lambda x: x*-1 if x < 0 else x, EveAl_list_of_floats_SDR3))
EveBob_list_of_floats_SDR3 = list(map(lambda x: x*-1 if x < 0 else x, EveBob_list_of_floats_SDR3))


EveAl_SDR3_1_norm=noise_removal.window_smoothening(EveAl_list_of_floats_SDR3[ind:ind+min_length], win)
EveBob_SDR3_1_norm=noise_removal.window_smoothening(EveBob_list_of_floats_SDR3[ind:ind+min_length], win)

#plot_CFO.plot_CFO(time, list_of_floats_SDR1[ind:ind+min_length], list_of_floats_SDR2[ind:ind+min_length], ax2)

corr_coeff_cfo_eveal, number_of_samples_cfo_eveal = correlation_calculation.complete_correlation(min_length, EveAl_list_of_floats_SDR3[ind:ind+min_length],
                                                                             list_of_floats_SDR1[ind:ind+min_length])
corr_coeff_smoothcfo_eveal, number_of_samples_smoothcfo_eveal = correlation_calculation.complete_correlation(min_length, EveAl_SDR3_1_norm,
                                                                             SDR1_1_norm)
corr_coeff_cfo_evebob, number_of_samples_cfo_evebob = correlation_calculation.complete_correlation(min_length, EveBob_list_of_floats_SDR3[ind:ind+min_length],
                                                                             list_of_floats_SDR2[ind:ind+min_length])
corr_coeff_smoothcfo_evebob, number_of_samples_smoothcfo_evebob = correlation_calculation.complete_correlation(min_length, EveBob_SDR3_1_norm,
                                                                             SDR2_1_norm)

SDR1_2gbytes, SDR2_2gbytes = lossless_quantization.multi_bit_quantization_corrplot(EveAl_SDR3_1_norm,
                                                                                   EveBob_SDR3_1_norm,
                                                                                   min_length,
                                                                                   win,
                                                                                   Quant_Range,
                                                                                   True, False)



SDR1_2, SDR2_2 = int2byte_conversion.intarray_to_bytearray(SDR1_2gbytes, SDR2_2gbytes, Quant_Range)

SDR1_bincount = binary_count.intarray2binarray(SDR1_2, Quant_Range)
SDR2_bincount = binary_count.intarray2binarray(SDR2_2, Quant_Range)

greycode_stringSDR1 = stringify.stringify(SDR1_bincount.astype(int))
greycode_stringSDR2 = stringify.stringify(SDR2_bincount.astype(int))
print("greycode string for SDR1", greycode_stringSDR1, " of length", len(greycode_stringSDR1))
print("greycode string for SDR2", greycode_stringSDR2, " of length", len(greycode_stringSDR2))

greycodeSDR1_bytes = string_to_bytearray.string_to_bytearray_conversion(8, greycode_stringSDR1)
greycodeSDR2_bytes = string_to_bytearray.string_to_bytearray_conversion(8, greycode_stringSDR2)

random.Random(4).shuffle(greycodeSDR2_bytes)

plt2.plot(list(greycodeSDR2_bytes), label='Eavesdropper')

plt2.xlabel('Time')
plt2.ylabel('Value')
# Adding legend
plt2.legend()

# Displaying the plot
plt2.show()
#######################################PO##############################################




'''
#plot_correlation.correlation_plot(number_of_samples_smoothcfo_eve, corr_coeff_smoothcfo_eve, axis, 'b--', "CFO smooth Eavedrooper")
plot_correlation.correlation_plot(number_of_samples_smoothcfo_eveal, corr_coeff_smoothcfo_eveal, axis, 'k-', "CFO Eve-Alice")
plot_correlation.correlation_plot(number_of_samples_smoothcfo_evebob, corr_coeff_smoothcfo_evebob, axis, 'b-', "CFO Eve-Bob")
plot_correlation.correlation_plot(number_of_samples_smoothcfo, corr_coeff_smoothcfo, axis, 'r-', "CFO Alice-Bob Smooth")
plot_correlation.correlation_plot(number_of_samples_cfo, corr_coeff_cfo, axis, 'c-', "CFO Alice-Bob")

#######################################PO##############################################
#Read the text file
#plt2.rcParams['font.family'] = 'Times New Roman'  # Specify the font family
plt2.rcParams['font.size'] = fontsz  # Specify the font size
plt2.xticks(fontsize=fontsz)  # Specify the font size for x-axis tick labels
plt2.yticks(fontsize=fontsz)  # Specify the font size for y-axis tick labels
plt2.show()'''
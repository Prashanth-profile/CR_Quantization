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
import errorcorrectioncode
import merger_list
import sk_dsp_comm.digitalcom as dc
import sk_dsp_comm.fec_conv as fec

##### Make sure appropriate values is choosen. Setting more than one value to True can cause unexpected behavior
class Quantization(enum.Enum):
    UNIFORM= True
    WINDOW_THRESHOLD=False
    GREY_CODE=True
    #Set MEAN_MEDIANBAR to True of False only after setting LOSSY_QUANTIZATION or WINDOW_THRESHOLD to True. Otherwise, it really is not useful
    LOSSY_QUANTIZATION = False
    MEAN_MEDIANBAR=False
    REEDSOLOMONCODE=True

class convolutional_code_stage(enum.Enum):
    STAGE=3

min_length=128
time=range(min_length)
ind=0

#########This variable is the window size: This is used in both lossy and lossless quantization
Quant_Range=2
window_size=min_length

#######################################CFO##############################################
#Read the text file
with open('C:/Users/prashanth/Desktop/CFO_SC_212_SDR1.txt', 'r') as fin:
    data_read_SDR1 = fin.read()
    last_char_SDR1 = data_read_SDR1[-1]
    if last_char_SDR1 == '\n':
        print("last next line character detected in first sample file")
        data_read_SDR1 = data_read_SDR1[:-1]
with open('C:/Users/prashanth/Desktop/CFO_SC_212_SDR2.txt', 'r') as fin:
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

print("Number of elements", len(list_of_floats_SDR1))

old_error_dist = []
remind=len(list_of_floats_SDR1)%min_length

if Quantization.LOSSY_QUANTIZATION.value == True:
    alpha = 0.01
    lossquantizedbits_SDR1 = window_average_threshold_quantization.float_to_binary_lossyquantization_onebit(list_of_floats_SDR1, window_size, Quantization.MEAN_MEDIANBAR.value, alpha)
    lossquantizedbits_SDR2 = window_average_threshold_quantization.float_to_binary_lossyquantization_onebit(list_of_floats_SDR2, window_size, Quantization.MEAN_MEDIANBAR.value, alpha)

    lossy_max_len=min(len(lossquantizedbits_SDR1), len(lossquantizedbits_SDR2))
    remind =  lossy_max_len% min_length

    print("Length of lossy quantization", len(lossquantizedbits_SDR1), len(lossquantizedbits_SDR2))

    SDR1_string = stringify.stringify(lossquantizedbits_SDR1[ind:ind+min_length])
    SDR2_string = stringify.stringify(lossquantizedbits_SDR2[ind:ind+min_length])

    print("SDR1 string", SDR1_string, "of length ", len(SDR1_string))
    print("SDR1 string", SDR2_string, "of length ", len(SDR2_string))

    SDR1_bytes = string_to_bytearray.string_to_bytearray_conversion(8, SDR1_string)
    SDR2_bytes = string_to_bytearray.string_to_bytearray_conversion(8, SDR2_string)

    print("Results of byte array conversion for lossy quantization", SDR1_bytes, "of length", len(SDR1_bytes))
    print("Results of byte array conversion for lossy quantization", SDR2_bytes, "of length", len(SDR2_bytes))

    num_errors, error_dist = erroranderror_distribution.error_distribution(SDR1_bytes,SDR2_bytes)

else:
    if Quantization.WINDOW_THRESHOLD.value==True:
        threshold_quantized_bits_SDR1 = window_average_threshold_quantization.window_average_meanmedian(list_of_floats_SDR1[ind:ind+min_length], window_size, Quantization.MEAN_MEDIANBAR.value)
        threshold_quantized_bits_SDR2 = window_average_threshold_quantization.window_average_meanmedian(list_of_floats_SDR2[ind:ind+min_length], window_size, Quantization.MEAN_MEDIANBAR.value)

        SDR1_string = stringify.stringify(threshold_quantized_bits_SDR1)
        SDR2_string = stringify.stringify(threshold_quantized_bits_SDR2)

        #print("One bit non lossy quantization achieved using MEAN_MEDIANBAR", Quantization.MEAN_MEDIANBAR.value)

        SDR1_bytes = string_to_bytearray.string_to_bytearray_conversion(8, SDR1_string)
        SDR2_bytes = string_to_bytearray.string_to_bytearray_conversion(8, SDR2_string)

        #print("Results of byte array conversion for WTQ", SDR1_bytes, "of length", len(SDR1_bytes))
        #print("Results of byte array conversion for WTQ", SDR2_bytes, "of length", len(SDR2_bytes))

        min_len = round(min_length / 8)
        num_errors, error_dist = erroranderror_distribution.error_distribution(SDR1_bytes, SDR2_bytes)

    ###################       BYTE ARRAY EXAMPLE   #################################
    # Example usage:
    #arr1 = b'\x01\x02\x03\x04\x05'
    #arr2 = b'\x02\x02\x02\x04\x04'
    ###################       BYTE ARRAY EXAMPLE   #################################

    #num_errors, error_dist = erroranderror_distribution.error_distribution(SDR1_bytes, SDR2_bytes)
    #erroranderror_distribution.plot_error_distribution(error_dist)

    # Print the total number of errors and distribution
    #print("Total number of errors: ", num_errors)
    #print("Distribution of errors: ", error_dist)

    if Quantization.UNIFORM.value==True:
        uniform_quantized_bytes_SDR1 = uniform_quantization.uniform_quantization_window(list_of_floats_SDR1[ind:ind+min_length], Quant_Range, window_size)
        uniform_quantized_bytes_SDR2 = uniform_quantization.uniform_quantization_window(list_of_floats_SDR2[ind:ind+min_length], Quant_Range, window_size)

        print("Result of uniform quantization in integer for SDR1", uniform_quantized_bytes_SDR1.astype(int), "with length ", len(uniform_quantized_bytes_SDR1.astype(int)))
        print("Result of uniform quantization in integer for SDR2", uniform_quantized_bytes_SDR2.astype(int), "with length ", len(uniform_quantized_bytes_SDR2.astype(int)))

        if Quantization.GREY_CODE.value==True:
            uniform_graycode_SDR1 = bintogrey.array_conversion_togray(uniform_quantized_bytes_SDR1.astype(int))
            uniform_graycode_SDR2 = bintogrey.array_conversion_togray(uniform_quantized_bytes_SDR2.astype(int))
            #uniform_graycode_SDR2=uniform_quantized_bytes_SDR2

            '''print("Result of gray code in integer for SDR1", uniform_graycode_SDR1.astype(int),
                  "with length ", len(uniform_graycode_SDR1.astype(int)))
            print("Result of gray code in integer for SDR2", uniform_graycode_SDR2.astype(int),
                  "with length ", len(uniform_graycode_SDR2.astype(int)))'''

            SDR1_bincount = binary_count.intarray2binarray(uniform_graycode_SDR1.astype(int),Quant_Range)
            SDR2_bincount = binary_count.intarray2binarray(uniform_graycode_SDR2.astype(int),Quant_Range)
        else:
            SDR1_bincount = binary_count.intarray2binarray(uniform_quantized_bytes_SDR1.astype(int),Quant_Range)
            SDR2_bincount = binary_count.intarray2binarray(uniform_quantized_bytes_SDR2.astype(int),Quant_Range)

        SDR1_string = stringify.stringify(SDR1_bincount.astype(int))
        SDR2_string = stringify.stringify(SDR2_bincount.astype(int))

        SDR1_bytes=string_to_bytearray.string_to_bytearray_conversion(8, SDR1_string)
        SDR2_bytes=string_to_bytearray.string_to_bytearray_conversion(8, SDR2_string)

        print("Results of byte array conversion for uniform quantization", SDR1_bytes, "of length", len(SDR1_bytes))
        print("Results of byte array conversion for uniform quantization", SDR2_bytes, "of length", len(SDR2_bytes))

        num_errors, error_dist = erroranderror_distribution.error_distribution(SDR1_bytes, SDR2_bytes)

num_errors, error_dist = erroranderror_distribution.error_distribution(SDR1_bytes, SDR2_bytes)
print("Number of errors before error correction coding", num_errors)
print("Total number of errors: ", num_errors)
print("Distribution of errors: ", error_dist)

'''#min_len=min(len(SDR1_bytes), len(SDR2_bytes))
#num_errors, error_dist = erroranderror_distribution.error_distribution(SDR1_bytes[0:min_len], SDR2_bytes[0:min_len])
print("Number of errors", num_errors)
plt.plot(range(len(error_dist)), error_dist)
plt.xlabel('Bit Position')
plt.ylabel('Number of errors in the bit position')
plt.title('Distribution of Errors with 2048 samples')
plt.show()'''

##########################################  CONVOLUTIONAL CODES BEGIN HERE   ####################################

if convolutional_code_stage.STAGE.value==3:
    SDR1_bytes=b"\x72\x51\x01"
    SDR2_bytes = b"\x72\x51\x01"

    cc1 = fec.FECConv(('1000', '0111', '1101'), 3)
    state = '000'
    input_bytes = SDR1_bytes
    x = np.array(errorcorrectioncode.bytearray_to_binarray(input_bytes))
    print("x is", x)
    encoded,state = cc1.conv_encoder(x,state)
    print("encoded", encoded.astype(int))
    parity=[encoded.astype(int)[x] for x in range(len(encoded)) if x%3!=0]
    print("parity is ", parity)

    input_bytes = SDR1_bytes
    SDR2_bin=errorcorrectioncode.bytearray_to_binarray(SDR2_bytes)
    print("SDR2 bin is", SDR2_bin)
    received_bin= merger_list.merge_offset(SDR2_bin, parity, 2)
    print("received bin", np.array(received_bin))

    received_bin = np.pad(received_bin, (0, 4))
    decoded=cc1.viterbi_decoder(np.array(received_bin),'hard')
    print("decoded", decoded, "of length", len(decoded), "\nagainst", x)
    print("decoded status", decoded.astype(int) == x)

    bit_count, bit_errors = dc.bit_errors(x,decoded)
    print("Number of errors after 4 stage convolutional coding is ", bit_errors, "with parity length ", len(parity))

elif convolutional_code_stage.STAGE.value==2:
    cc1 = fec.FECConv(('100', '111'), 2)
    state = '00'
    input_bytes = SDR1_bytes
    x = np.array(errorcorrectioncode.bytearray_to_binarray(input_bytes))
    print("x is", x)
    encoded,state = cc1.conv_encoder(x,state)
    print("encoded", encoded.astype(int))
    parity = [encoded.astype(int)[x] for x in range(len(encoded)) if x % 2 != 0]

    #SDR2_bin = errorcorrectioncode.bytearray_to_binarray(SDR2_bytes)
    input_bytes = SDR2_bytes
    SDR2_bin = np.array(errorcorrectioncode.bytearray_to_binarray(input_bytes))
    print("received binary", parity, "data", SDR2_bin)
    received_bin = merger_list.merge(SDR2_bin, parity)
    received_bin = np.pad(received_bin, (0, 1))
    print("received bin", np.array(received_bin))

    decoded=cc1.viterbi_decoder(np.array(received_bin),'hard')
    print("decoded", decoded)
    print("decoded status", decoded.astype(int) == x)

    bit_count, bit_errors = dc.bit_errors(x,decoded)
    print("Number of errors after 3 stage convolutional coding is ", bit_errors, "with parity length ", len(parity))

##############################    CONVOLUTIONAL CODE ENDS HERE       ###################################


################################# REED SOLOMON ENCODING AND DECODING ####################################

#Initialize RS encoding parameters in bytes
if Quantization.REEDSOLOMONCODE.value==True:
    segment_size=8
    parity_size=16
    print("Length", len(SDR1_bytes), len(SDR2_bytes))
    number_of_segments=round(len(SDR1_bytes)/(segment_size))
    print("Number of segments", number_of_segments)

    RS_encode = reedsolomon_codec.RS_encoding(SDR1_bytes, segment_size, parity_size, number_of_segments)

    print("RS encoding ", RS_encode, " with parity byte length ", len(RS_encode))
    # RS decoding for uniformly quantized binary codes and grey codes
    RS_decode = reedsolomon_codec.RS_decoding(SDR2_bytes, RS_encode, segment_size, parity_size, number_of_segments)
    print("decoded bytes  ", RS_decode, " with byte length ", len(RS_decode))
    print("Decoding status without gray codes ", RS_decode == SDR1_bytes)
    num_errors, error_dist = erroranderror_distribution.error_distribution(RS_decode, SDR1_bytes)
    print("Length of parity for reed solomon codecs is ", len(RS_encode)*8, "with number of errors", num_errors)
################################# REED SOLOMON ENCODING AND DECODING ENDS  ####################################
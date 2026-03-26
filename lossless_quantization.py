import window_average_threshold_quantization
import stringify
import string_to_bytearray
import uniform_quantization
import bintogrey
import binary_count
import numpy as np
import normalization_and_standardization

def one_bit_quantization(list_of_floats_SDR1, list_of_floats_SDR2, min_length, window_size, mean_medbar):
    threshold_quantized_bits_SDR1 = window_average_threshold_quantization.window_average_meanmedian(list_of_floats_SDR1[0:min_length], window_size, mean_medbar)
    threshold_quantized_bits_SDR2 = window_average_threshold_quantization.window_average_meanmedian(list_of_floats_SDR2[0:min_length], window_size, mean_medbar)

    SDR1_string = stringify.stringify(threshold_quantized_bits_SDR1)
    SDR2_string = stringify.stringify(threshold_quantized_bits_SDR2)

    #print("SDR1 string", SDR1_string)
    #print("SDR2 string", SDR2_string)

    #print("One bit non lossy quantization achieved using MEAN_MEDIANBAR", Quantization.MEAN_MEDIANBAR.value)

    SDR1_bytes = string_to_bytearray.string_to_bytearray_conversion(8, SDR1_string)
    SDR2_bytes = string_to_bytearray.string_to_bytearray_conversion(8, SDR2_string)

    return SDR1_bytes, SDR2_bytes

def multi_bit_quantization(list_of_floats_SDR1, list_of_floats_SDR2, min_length, window_size, Quant_Range, gray_state):
    uniform_quantized_bytes_SDR1 = uniform_quantization.uniform_quantization_window(list_of_floats_SDR1[0:min_length],
                                                                                    Quant_Range, window_size)
    uniform_quantized_bytes_SDR2 = uniform_quantization.uniform_quantization_window(list_of_floats_SDR2[0:min_length],
                                                                                    Quant_Range, window_size)

    if gray_state == True:
        uniform_graycode_SDR1 = bintogrey.array_conversion_togray(uniform_quantized_bytes_SDR1.astype(np.uint8))
        uniform_graycode_SDR2 = bintogrey.array_conversion_togray(uniform_quantized_bytes_SDR2.astype(np.uint8))

        SDR1_bincount = binary_count.intarray2binarray(uniform_graycode_SDR1.astype(np.uint8), Quant_Range)
        SDR2_bincount = binary_count.intarray2binarray(uniform_graycode_SDR2.astype(np.uint8), Quant_Range)
    else:
        SDR1_bincount = binary_count.intarray2binarray(uniform_quantized_bytes_SDR1.astype(np.uint8), Quant_Range)
        SDR2_bincount = binary_count.intarray2binarray(uniform_quantized_bytes_SDR2.astype(np.uint8), Quant_Range)

    SDR1_string = stringify.stringify(SDR1_bincount.astype(np.uint8))
    SDR2_string = stringify.stringify(SDR2_bincount.astype(np.uint8))

    SDR1_bytes = string_to_bytearray.string_to_bytearray_conversion(8, SDR1_string)
    SDR2_bytes = string_to_bytearray.string_to_bytearray_conversion(8, SDR2_string)

    return SDR1_bytes, SDR2_bytes

def multi_bit_quantization_corrplot(list_of_floats_SDR1, list_of_floats_SDR2, min_length, window_size, Quant_Range, gray_state, clip):
    uniform_quantized_bytes_SDR1 = uniform_quantization.uniform_quantization_window(list_of_floats_SDR1[0:min_length],
                                                                                    Quant_Range, window_size, clip)
    uniform_quantized_bytes_SDR2 = uniform_quantization.uniform_quantization_window(list_of_floats_SDR2[0:min_length],
                                                                                    Quant_Range, window_size, clip)

    if gray_state == True:
        uniform_graycode_SDR1 = bintogrey.array_conversion_togray(uniform_quantized_bytes_SDR1.astype(int))
        uniform_graycode_SDR2 = bintogrey.array_conversion_togray(uniform_quantized_bytes_SDR2.astype(int))

        uniform_SDR1=uniform_graycode_SDR1.astype(int)
        uniform_SDR2=uniform_graycode_SDR2.astype(int)
    else:
        uniform_SDR1 = uniform_quantized_bytes_SDR1.astype(int)
        uniform_SDR2 = uniform_quantized_bytes_SDR2.astype(int)


    return uniform_SDR1, uniform_SDR2

def multi_bit_dynamic_quantization_corrplot(list_of_floats_SDR1, list_of_floats_SDR2, min_length, Quant_Range, gray_state, ind):
    #z_score_SDR1=normalization_and_standardization.z_score_normalization(list_of_floats_SDR1[ind:ind+min_length])
    #z_score_SDR2 = normalization_and_standardization.z_score_normalization(list_of_floats_SDR2[ind:ind + min_length])

    uniform_quantized_bytes_SDR1 = uniform_quantization.uniform_dynamic_quantization(list_of_floats_SDR1[ind:ind+min_length],
                                                                                    2**Quant_Range)
    uniform_quantized_bytes_SDR2 = uniform_quantization.uniform_dynamic_quantization(list_of_floats_SDR2[ind:ind+min_length],
                                                                                    2**Quant_Range)

    #uniform_quantized_bytes_SDR1 = uniform_quantization.uniform_dynamic_quantization(z_score_SDR1,
    #                                                                                2**Quant_Range)
    #uniform_quantized_bytes_SDR2 = uniform_quantization.uniform_dynamic_quantization(z_score_SDR2,
    #                                                                                2**Quant_Range)

    if gray_state == True:
        uniform_graycode_SDR1 = bintogrey.array_conversion_togray(uniform_quantized_bytes_SDR1.astype(int))
        uniform_graycode_SDR2 = bintogrey.array_conversion_togray(uniform_quantized_bytes_SDR2.astype(int))

        uniform_SDR1=uniform_graycode_SDR1.astype(int)
        uniform_SDR2=uniform_graycode_SDR2.astype(int)
    else:
        uniform_SDR1 = uniform_quantized_bytes_SDR1.astype(int)
        uniform_SDR2 = uniform_quantized_bytes_SDR2.astype(int)


    return uniform_SDR1, uniform_SDR2
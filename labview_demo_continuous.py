import noise_removal
import lossless_quantization
import int2byte_conversion
import erroranderror_distribution
import calculate_entropy
import binary_count
import stringify
import string_to_bytearray
import reedsolomon_codec
import numpy as np


ind=0

def SavGoldfiltering(list_of_float_SDR1, list_of_float_SDR2, min_l, win):
    list_of_float_SDR1 = list(map(lambda x: x * -1 if x < 0 else x, list_of_float_SDR1))
    list_of_float_SDR2 = list(map(lambda x: x * -1 if x < 0 else x, list_of_float_SDR2))
    SDR1_1_norm = noise_removal.savgold_filter(list_of_float_SDR1[0:min_l], win)
    SDR2_1_norm = noise_removal.savgold_filter(list_of_float_SDR2[0:min_l], win)
    result=[]
    result.extend(SDR1_1_norm)
    result.extend(SDR2_1_norm)
    return result

def ECC(SDR1_bincount, SDR2_bincount, Quant_Range, num_of_observations, parity):

    greycode_stringSDR1 = stringify.stringify(SDR1_bincount)
    greycode_stringSDR2 = stringify.stringify(SDR2_bincount)


    greycodeSDR1_bytes = string_to_bytearray.string_to_bytearray_conversion(8, greycode_stringSDR1)
    greycodeSDR2_bytes = string_to_bytearray.string_to_bytearray_conversion(8, greycode_stringSDR2)

    number_of_segments = 1
    segment_size=int(num_of_observations * (Quant_Range/8)/number_of_segments)
    parity_size=int(parity/number_of_segments)

    #print("before rs codec", greycodeSDR1_bytes, greycodeSDR2_bytes)

    RS_encode = reedsolomon_codec.RS_encoding(list(greycodeSDR1_bytes[0:segment_size * number_of_segments]), segment_size,
                                              parity_size, number_of_segments)

    # RS Decode
    RS_decode = reedsolomon_codec.RS_decoding(list(greycodeSDR2_bytes[0:segment_size * number_of_segments]), RS_encode,
                                              segment_size, parity_size, number_of_segments)



    SDR2_bincount = binary_count.intarray2binarray(list(RS_decode), 8)

    results=[]
    results.extend(SDR1_bincount)
    results.extend(SDR2_bincount)

    return results

def multi_bit_Quantization(SDR1_1_norm, SDR2_1_norm, min_l, window_size, Quant_Range):
    SDR1_2gbytes, SDR2_2gbytes = lossless_quantization.multi_bit_quantization_corrplot(SDR1_1_norm,
                                                                                       SDR2_1_norm,
                                                                                       min_l,
                                                                                       window_size,
                                                                                       Quant_Range,
                                                                                       True, False)

    SDR1_2, SDR2_2 = int2byte_conversion.intarray_to_bytearray(SDR1_2gbytes, SDR2_2gbytes, Quant_Range)

    num_errors, error_dist = erroranderror_distribution.error_distribution(SDR1_2gbytes, SDR2_2gbytes)

    entropy = calculate_entropy.calculate_entropy(SDR1_2)
    CR_rate=entropy * abs(1 - 2 * (num_errors / (Quant_Range * min_l)))

    SDR1_bincount = binary_count.intarray2binarray(SDR1_2, Quant_Range)
    SDR2_bincount = binary_count.intarray2binarray(SDR2_2, Quant_Range)

    #ECC(SDR1_bincount, SDR2_bincount, Quant_Range, min_l, 10)

    print("SDR1 bin", SDR1_bincount)
    print("SDR2 bin", SDR2_bincount)

    print(SDR1_bincount==SDR2_bincount)

    result=[]
    result.append(CR_rate)
    result.extend(SDR1_bincount)
    result.extend(SDR2_bincount)
    return result


print(multi_bit_Quantization([0,2,3,4,5,10,11,12,13,10,10,10,10], [1,2,3,4,5,10,11,12,13,10,10,10,11], 13, 13, 4))
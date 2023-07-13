import window_average_threshold_quantization
import stringify
import string_to_bytearray

def lossy_quantization(list_of_floats_SDR1, list_of_floats_SDR2, min_length, window_size, mean_medianbar, alpha):
    lossquantizedbits_SDR1 = window_average_threshold_quantization.float_to_binary_lossyquantization_onebit(list_of_floats_SDR1, min_length, window_size, mean_medianbar, alpha)
    lossquantizedbits_SDR2 = window_average_threshold_quantization.float_to_binary_lossyquantization_onebit(list_of_floats_SDR2, min_length, window_size, mean_medianbar, alpha)

    lossy_max_len=min(len(lossquantizedbits_SDR1), len(lossquantizedbits_SDR2))
    remind =  lossy_max_len% min_length

    print("Length of lossy quantization", len(lossquantizedbits_SDR1), len(lossquantizedbits_SDR2))

    SDR1_string = stringify.stringify(lossquantizedbits_SDR1)
    SDR2_string = stringify.stringify(lossquantizedbits_SDR2)

    print("SDR1 string", SDR1_string, "of length ", len(SDR1_string))
    print("SDR1 string", SDR2_string, "of length ", len(SDR2_string))

    SDR1_bytes = string_to_bytearray.string_to_bytearray_conversion(8, SDR1_string)
    SDR2_bytes = string_to_bytearray.string_to_bytearray_conversion(8, SDR2_string)

    return SDR1_bytes[0:round(min_length/8)], SDR2_bytes[0:round(min_length/8)]
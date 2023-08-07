import binary_count
import stringify
import string_to_bytearray
import numpy as np

def count_uncommon_elements_at_each_index(str1, str2):
    count = 0
    for char1, char2 in zip(str1, str2):
        if char1 != char2:
            count += 1
    return count

def intarray_to_bytearray(quantized_int_SDR1, quantized_int_SDR2, Quant_Range):
    SDR1_bincount = binary_count.intarray2binarray(quantized_int_SDR1, Quant_Range)
    SDR2_bincount = binary_count.intarray2binarray(quantized_int_SDR2, Quant_Range)

    SDR1_string = stringify.stringify(SDR1_bincount.astype(int))
    SDR2_string = stringify.stringify(SDR2_bincount.astype(int))

    SDR1_bytes = string_to_bytearray.string_to_bytearray_conversion(Quant_Range, SDR1_string)
    SDR2_bytes = string_to_bytearray.string_to_bytearray_conversion(Quant_Range, SDR2_string)

    print("SDR1 bytes", SDR1_bytes, "of size", len(SDR1_bytes))
    print("SDR2 bytes", SDR2_bytes, "of size", len(SDR1_bytes))

    return SDR1_bytes, SDR2_bytes

# Example usage
string1 = "abcdefg"
string2 = "aXXeXg"
result = count_uncommon_elements_at_each_index(string1, string2)
print(result)  # Output: 3
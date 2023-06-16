import numpy as np


def bin_array(num, m):
    if num >= 0:
        binary_str = np.binary_repr(num).zfill(m)
    else:
        # Convert the absolute value of the negative number to binary
        abs_num = abs(num)
        binary_str = np.binary_repr(abs_num, width=m)

        # Perform two's complement by flipping the bits and adding 1
        binary_str = ''.join('1' if bit == '0' else '0' for bit in binary_str)
        binary_str = binary_str.zfill(m)  # Pad with leading zeros if necessary

    binary_array = np.array(list(binary_str)).astype(np.int8)

    return binary_array


test_num = [38, 22, 100, 121]
test1 = [0, 0, 0, 1, 1, 1, 0, 0]
test2 = [0, 0, 0, 1, 1, 1, 1, 1]

getbinary = lambda x, n: format(x, 'b').zfill(n)


def intarray2binarray(int_array, nr_bits):
    b = []
    for i in range(len(int_array)):
        b = np.concatenate([b, bin_array(int_array[i], nr_bits)])
    # printing original number
    # print("The original number is : " + str(int_array))
    # print("The converted binary list is : ", b)
    return b


def bitcount_window(binarray1, binarray2, window_size):
    bincount = []
    if len(binarray1) % window_size != 0:
        print("Error in window_size or sample size ", len(binarray1))
        return -1
    if len(binarray1) != len(binarray2):
        print("Error in one or both sample size, sample size not same")
        return -1
    for i in range(0, len(binarray1), window_size):
        # print("bincount", bincount)
        # print("np.count", np.count_nonzero(binarray1[i:i+window_size]==binarray2[i:i+window_size]))
        bincount.append(np.count_nonzero(binarray1[i:i + window_size] == binarray2[i:i + window_size]))
    print("Equal bit count", sum(bincount))
    return bincount


def perform_elementwise_boolean_operation(array1, array2):
    result = [x and y for x, y in zip(array1, array2)]
    return all(result)


'''array1 = [True, True, True, True]
array2 = [True, True, True, True]

result = perform_elementwise_boolean_operation(list(array1), list(array2))
print(result)

bitcount_window(test1, test2, 1)'''


def case_2():
    print("Quantization 2")
    return 0b11000000


def case_3():
    print("Quantization 3")
    return 0b11100000


def case_4():
    print("Quantization 4")
    return 0b11110000


def case_5():
    print("Quantization 5")
    return 0b11111000


def case_6():
    print("Quantization 6")
    return 0b11111100


def case_7():
    print("Quantization 7")
    return 0b11111110


def case_8():
    print("Quantization 8")
    return 0b11111111


def default_case():
    raise ValueError("Wrong quantization chosen")
    # Code for the default case goes here


def choose_extraction_bits(value):
    case_dict = {
        2: case_2,
        3: case_3,
        4: case_4,
        5: case_5,
        6: case_6,
        7: case_7,
        8: case_8,
    }

    # Get the function associated with the value and call it
    case_func = case_dict.get(value, default_case)
    result = case_func()

    return result


def count_bit_errors(byte_array1, byte_array2, Quant_Range):
    errors_per_2bits = []

    extraction_bits = choose_extraction_bits(Quant_Range)

    for byte_a, byte_b in zip(byte_array1, byte_array2):
        # XOR the two bytes to find the differing bits
        diff_bits = byte_a ^ byte_b
        print(diff_bits)

        # Count the number of differing bits for every 2-bit position
        for i in range(0, Quant_Range):
            # Extract the 2 bits at position i
            bits = (diff_bits << i) & extraction_bits
            print(bits)

            # Count the number of differing bits in the 2-bit position
            errors = bin(bits).count("1")
            errors_per_2bits.append(errors)

    return errors_per_2bits


# Example usage
# byte_array1 = bytearray(b'\xFF\x33\x55')
# byte_array2 = bytearray(b'\x0F\x33\x24')
# byte_array2 = bytearray(b'\x0F\x3B\x57')

# Example usage
'''byte_array1 = [7, 3, 5]
byte_array2 = [7, 11, 6]

bit_errors = count_bit_errors(byte_array1, byte_array2, 4)

print("Number of bit errors at each 2-bit position:", bit_errors)'''

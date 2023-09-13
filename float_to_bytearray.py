import struct


def float_array_to_64bitbyte_array(float_array):
    byte_array = bytearray()

    for num in float_array:
        # Convert float to 64-bit unsigned integer representation
        uint64_value = struct.unpack('Q', struct.pack('d', num))[0]

        # Convert the uint64 value to bytes and append to the byte array
        byte_array.extend(uint64_value.to_bytes(8, byteorder='big'))

    return byte_array


def float_array_to_32bitbyte_array(float_array):
    byte_array = bytearray()
    for num in float_array:
        # Convert the floating-point number to its IEEE 754 binary representation
        num_bytes = struct.pack('f', num)

        # Convert the bytes to a byte array and extend the result
        byte_array.extend(num_bytes)

    return byte_array


# Test the function
#float_numbers = [3.14, 1.618, 2.718]
#byte_array = float_array_to_byte_array(float_numbers)
#print(byte_array)

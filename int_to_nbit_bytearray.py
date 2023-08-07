def int_to_variable_bit_byte_array(value, num_bits):
    # Ensure the value is within the specified bit range
    if value < 0 or value >= 2**num_bits:
        raise ValueError(f"Value must be a {num_bits}-bit integer (0 to {2**num_bits - 1})")

    # Determine the number of bytes required to represent the integer value
    num_bytes = (num_bits + 7) // 8

    # Create the byte array
    byte_array = []
    for _ in range(num_bytes):
        byte_array.append(value & 0xFF)
        value >>= 8

    # Reverse the byte array if needed (little-endian representation)
    byte_array.reverse()

    return byte_array

# Example usage
value = 511  # Replace this with any integer value (0 to 2^num_bits - 1)
num_bits = 10  # Replace this with the desired number of bits (2 to 10)
byte_array = bytearray(int_to_variable_bit_byte_array(value, num_bits))
print(byte_array)

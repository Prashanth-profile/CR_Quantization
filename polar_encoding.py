def systematic_polar_encoding(input_list):
    n = len(input_list)
    k = 0
    while 2 ** k < n + k:
        k += 1

    encoded_list = [0] * (n + k)

    for i in range(n):
        encoded_list[i] = input_list[i]

    for i in range(k):
        j = 0
        while j < n:
            for l in range(2 ** i):
                if j + n < n + k:
                    encoded_list[j + n] = encoded_list[j + n] ^ encoded_list[j]
                j += 1
            j += 2 ** i

    parity_bytes = encoded_list[n:]
    print("Encoded list", encoded_list)

    return parity_bytes

def systematic_polar_decoding(input_bits, parity_bits):
    n = len(input_bits)
    k = len(parity_bits)
    decoded_list = input_bits[:]

    for i in range(k):
        j = 0
        while j < n:
            for l in range(2 ** i):
                if j + n < len(decoded_list):
                    decoded_list[j] = decoded_list[j] ^ decoded_list[j + n] ^ parity_bits[i]
                j += 1
            j += 2 ** i

    information_bits = decoded_list[:n]

    return information_bits

# Example usage
input_list = [1, 0, 1, 1]  # Input list to be encoded
parity_bytes = systematic_polar_encoding(input_list)
print("Parity bytes:", parity_bytes)

# Example usage
input_bits = [0, 1, 1, 1]  # Input bits
parity_bits = [1, 0, 1]    # Parity bits
decoded_bits = systematic_polar_decoding(input_bits, parity_bits)
print("Decoded bits:", decoded_bits)
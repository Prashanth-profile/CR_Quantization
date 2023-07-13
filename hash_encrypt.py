import hashlib

def encrypt_bytes(input_bytes):
    # Create a SHA-256 hash object
    sha512_hash = hashlib.sha512()

    # Update the hash object with the input bytes
    sha512_hash.update(input_bytes)

    # Get the hash value as bytes
    encrypted_bytes = sha512_hash.digest()

    return encrypted_bytes

def save_to_bin(SDR1_bytes):
    hash_lossy = encrypt_bytes(SDR1_bytes)
    file_path = r'C:\Users\prashanth\Desktop\2byte_array.bin'
    save_to_bin.save_byte_array(hash_lossy, file_path)
    return

# Example usage
'''input_bytes = b'\x01\x02\x03\x04\x05'
encrypted_bytes = encrypt_bytes(input_bytes)
print("Input Bytes:", input_bytes)
print("Encrypted Bytes:", encrypted_bytes, len(encrypted_bytes))'''

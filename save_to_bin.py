def save_byte_array(byte_array, file_path):
    # Write the byte array to a binary file
    with open(file_path, 'wb') as file:
        file.write(byte_array)

# Example usage
#byte_array = b'\x48\x65\x6c\x6c\x6f\x2c\x20\x57\x6f\x72\x6c\x64'
#file_path = r'C:\Users\prashanth\Desktop\1byte_array.bin'
#save_byte_array(byte_array, file_path)'''
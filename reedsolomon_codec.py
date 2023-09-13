from reedsolo import RSCodec

#segment_size=28
#parity_size=4

#number_of_segments=3

def RS_encoding(complete_data, segment_size, parity_size, number_of_segments):
    rsc = RSCodec(parity_size)
    rs_encoded=bytearray()
    parity_bytes_complete=bytearray()
    for i in range(0, segment_size*number_of_segments, segment_size):
        segmentencode=rsc.encode(complete_data[i:i+segment_size])
        print("segment code", segmentencode)
        parity_bytes=segmentencode[len(segmentencode)-parity_size:]
        rs_encoded.extend(segmentencode)
        parity_bytes_complete.extend(parity_bytes)
        #print("Complete_parity_bytes",parity_bytes_complete)
    print("Complete_parity_bytes", parity_bytes_complete)
    return parity_bytes_complete


def RS_decoding(complete_data, parity_bytes, segment_size, parity_size, number_of_segments):
    rsc = RSCodec(parity_size)
    j=0
    encoded_bytes=bytearray()
    decoded_bytes = bytearray()
    for i in range(0, segment_size*number_of_segments, segment_size):
        encoded_bytes=bytearray(complete_data[i:i+segment_size])
        encoded_bytes.extend(parity_bytes[j:j+parity_size])
        decoded_bytes_per_segment=rsc.decode(encoded_bytes)[0]
        j=j+parity_size
        decoded_bytes.extend(decoded_bytes_per_segment)
    print("decoded bytes", decoded_bytes)
    return decoded_bytes


''''########################## REED SOLOMON ENCODING
arr1 = b'\x01\x02\x03\x04\x05\x01\x02\x03\x04\x05\x01\x02\x03\x04\x05\x01\x01\x02\x03\x04\x05\x01\x02\x03\x04\x05\x01\x02\x03\x04\x05\x01'
arr2 = b'\x01\x02\x02\x04\x04\x01\x02\x03\x04\x05\x01\x02\x03\x04\x05\x01\x01\x02\x02\x04\x04\x01\x02\x03\x04\x05\x01\x02\x03\x04\x05\x01'

#arr1=b'W\xd4P\x02J\xaa\xaa\xff\xaa\x8b\xcf\x00\x08\x00UU\xab\xfdT\x00\x00W^\xd0\x01@\x1f\xeeEW\xd5\xca'
#arr2=b'W\xd5P\x02\x8a\xaa\xab\xff\xaa\xab\xcf\x00\x08\x00UU\xaa\xffU@\x00W^\xd4\x00@\x17o\x00\x07\xd5j'

print("Length", len(arr1), len(arr2))

#Size of message length in bytes
segment_size=4

#Size of parity in bytes
parity_size=2     ####Parity bytes must not be equal to segment size to prove effectiveness of ECC

#Number of smaller message segments
number_of_segments=8
print("Number of segments", number_of_segments)

RS_encode = RS_encoding(arr1, segment_size, parity_size, number_of_segments)
print("RS encode", RS_encode, "with length", len(RS_encode))
RS_decode = RS_decoding(arr2, RS_encode, segment_size, parity_size, number_of_segments)
print("RS decode", RS_decode, "with length", len(RS_decode))

print("Decoding status without gray codes ", bytearray(RS_decode) == arr1)'''
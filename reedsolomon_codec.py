from reedsolo import RSCodec

segment_size=223
parity_size=32

rsc=RSCodec(parity_size)

def RS_encoding(complete_data):
    rs_encoded=bytearray()
    parity_bytes_complete=bytearray()
    for i in range(0, len(complete_data), segment_size):
        segmentencode=rsc.encode(complete_data[i:i+segment_size])
        parity_bytes=segmentencode[len(segmentencode)-parity_size:len(segmentencode)]
        rs_encoded.extend(segmentencode)
        parity_bytes_complete.extend(parity_bytes)
        #print("Complete_parity_bytes",parity_bytes_complete)

    return parity_bytes_complete


def RS_decoding(complete_data, parity_bytes):
    j=0
    encoded_bytes=bytearray()
    decoded_bytes = bytearray()
    for i in range(0, len(complete_data), segment_size):
        encoded_bytes=bytearray(complete_data[i:i+segment_size])
        encoded_bytes.extend(parity_bytes[j:j+parity_size])
        decoded_bytes_per_segment=rsc.decode(encoded_bytes)[0]
        j=j+parity_size
        decoded_bytes.extend(decoded_bytes_per_segment)
    return list(decoded_bytes)
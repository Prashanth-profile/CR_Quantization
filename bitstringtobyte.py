def bitstring_to_bytes(s, Quantrange):
    #print("length of string is ", len(s))
    rem=len(s)%8
    #print(rem, " bits rejected")
    return int(s[:len(s)-rem], 2).to_bytes((len(s[:len(s)-rem]) + 7) // Quantrange, byteorder='big')

'''def bitstring_to_bytes(s):
    v = int(s, 2)
    b = bytearray()
    while v:
        b.append(v & 0xff)
        v >>= 8
    return bytes(b[::-1])'''
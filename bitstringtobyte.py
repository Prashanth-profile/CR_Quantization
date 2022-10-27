from bitstring import BitArray
import numpy as np
import itertools

def bitstobyte(bits):
    #print(int(len(bits)/8))
    #b=np.zeros(int(len(bits)/8))
    #for i in range(0, int(len(bits)/8), 8):
        #print(i)
    b=BitArray(bits)
    #print("b is ", b)
    return b
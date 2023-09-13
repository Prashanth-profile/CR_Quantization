import numpy as np

def string_to_bytearray_conversion(Quant_Range, data):
    #print("Length of data strings", len(data))
    #print("Number of segments", int(len(data)/Quant_Range))
    #data = [data[8*i:8*(i+1)] for i in range(int(len(data)/8))]
    data = [data[Quant_Range * i:Quant_Range * (i + 1)] for i in range(int(len(data)/Quant_Range))]
    #print("data", data)
    data = [int(i, 2) for i in data]
    #print("data", data)
    #data[np.where(data==0)] =1
    #data = ''.join(chr(i) for i in data)
    #print(bytearray(data))
    return data

def string_to_greycode_bytearray_conversion(Quant_Range, data):
    #data = [data[8*i:8*(i+1)] for i in range(int(len(data)/8))]
    data = [data[Quant_Range * i:Quant_Range * (i + 1)] for i in range(int(len(data) / Quant_Range))]
    data = [int(i, 2) for i in data]
    data = [data(i)^(data(i) >> 1) for i in range(len(data))]
    #data[np.where(data==0)] =1
    #data = ''.join(chr(i) for i in data)
    #print(bytearray(data))
    return data
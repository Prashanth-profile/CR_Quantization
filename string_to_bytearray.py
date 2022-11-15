import numpy as np

def string_to_bytearray_conversion(Quant_Range, data):
    data = [data[Quant_Range*i:Quant_Range*(i+1)] for i in range(int(len(data)/Quant_Range))]
    data = [int(i, 2) for i in data]
    #data[np.where(data==0)] =1
    #data = ''.join(chr(i) for i in data)
    #print(bytearray(data))
    return bytearray(data)
import numpy as np


def grayCode(n):
    # Right Shift the number
    # by 1 taking xor with
    # original number
    return n ^ (n >> 1)

def array_conversion_togray(arr):
    grayarr=[]
    for i in range(0, len(arr)):
        code=grayCode(arr[i])
        grayarr.append(code)
    return np.array(grayarr)
# Driver Code
n = [77, 67]
print(array_conversion_togray(n))
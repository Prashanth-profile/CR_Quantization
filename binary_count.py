import numpy as np

def bin_array(num, m):
    """Convert a positive integer num into an m-bit bit vector"""
    return np.array(list(np.binary_repr(num).zfill(m))).astype(np.int8)

test_num = [38, 22, 100, 121]
test1=[0, 0, 0, 1, 1, 1, 0, 0]
test2=[0, 0, 0, 1, 1, 1, 1, 1]

getbinary = lambda x, n: format(x, 'b').zfill(n)

def intarray2binarray(int_array, nr_bits):
    b=[]
    for i in range(len(int_array)):
        b=np.concatenate([b,bin_array(int_array[i],nr_bits)])
    # printing original number
    #print("The original number is : " + str(int_array))
    #print("The converted binary list is : ", b)
    return b

def bitcount_window(binarray1, binarray2, window_size):
    bincount=[]
    if len(binarray1)%window_size!=0:
        print("Error in window_size or sample size ", len(binarray1))
        return -1
    if len(binarray1)!=len(binarray2):
        print("Error in one or both sample size, sample size not same")
        return -1
    for i in range(0, len(binarray1), window_size):
        #print("bincount", bincount)
        #print("np.count", np.count_nonzero(binarray1[i:i+window_size]==binarray2[i:i+window_size]))
        bincount.append(np.count_nonzero(binarray1[i:i+window_size]==binarray2[i:i+window_size]))
    print("Equal bit count", sum(bincount))
    return bincount

def perform_elementwise_boolean_operation(array1, array2):
    result = [x and y for x, y in zip(array1, array2)]
    return all(result)

array1 = [True, True, True, True]
array2 = [True, True, True, True]

result = perform_elementwise_boolean_operation(list(array1), list(array2))
print(result)

bitcount_window(test1, test2, 1)
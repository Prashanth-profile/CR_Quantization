# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import matplotlib.pyplot as plt
import numpy as np

with open('C:/Users/Prashanth/Desktop/writefile.txt', 'r') as fin:
    data_read_SDR1 = fin.read()
with open('C:/Users/Prashanth/Desktop/writefile2.txt', 'r') as fin:
    data_read_SDR2 = fin.read()

# average = mean(data)
# print(average)
data_read_SDR1 = data_read_SDR1.replace(',', '.')
data_read_SDR2 = data_read_SDR2.replace(',', '.')

list_of_strings_SDR1 = data_read_SDR1.split('\n')
list_of_strings_SDR2 = data_read_SDR2.split('\n')

list_of_floats_SDR1 = [float(x) for x in list_of_strings_SDR1]
print(list_of_floats_SDR1)
list_of_floats_SDR2 = [float(x) for x in list_of_strings_SDR2]
print(list_of_floats_SDR2)

quantized_bits_SDR1 = np.zeros(len(list_of_floats_SDR2))
quantized_bits_SDR2 = np.zeros(len(list_of_floats_SDR2))

average_SDR1 = np.mean(list_of_floats_SDR1)
print(average_SDR1)
average_SDR2 = np.mean(list_of_floats_SDR2)
print(average_SDR2)

var_SDR1 = np.var(list_of_floats_SDR1)
print(var_SDR1)
var_SDR2 = np.var(list_of_floats_SDR2)
print(var_SDR2)

for i in range(len(list_of_floats_SDR1)):
    if list_of_floats_SDR1[i] < average_SDR1:
        quantized_bits_SDR1[i] = 0
    else:
        quantized_bits_SDR1[i] = 1
for j in range(len(list_of_floats_SDR2)):
    if list_of_floats_SDR2[j] < average_SDR2:
        quantized_bits_SDR2[j] = 0
    else:
        quantized_bits_SDR2[j] = 1

min_length = min(len(list_of_floats_SDR1), len(list_of_floats_SDR2))
min_length=100
print("Min length =", min_length)
print("secret key of SDR1=", quantized_bits_SDR1[0:min_length])
print("secret key of SDR2=", quantized_bits_SDR2[0:min_length])
time = list(range(min_length))

unequal_count = 0
for i, j in zip(quantized_bits_SDR1[0:min_length], quantized_bits_SDR2[0:min_length]):
    if i != j:
        unequal_count = unequal_count + 1

print("Number of unequal bits", unequal_count)

plt.plot(time, list_of_floats_SDR1[1:min_length+1], 'b-', label='SDR1')
plt.plot(time, list_of_floats_SDR2[1:min_length+1], 'g-', label='SDR2')
plt.legend(loc='upper left')
plt.xlabel('Time (t)')
plt.ylabel('SNR values')
plt.show()

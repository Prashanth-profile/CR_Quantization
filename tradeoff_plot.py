import math

import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['text.usetex'] = True
plt.rcParams.update({'font.family': 'Times New Roman', 'font.size': 50, })

# Data
#x = np.arange(1, 8)
#y1 = [2048, 1024, 512, 256, 256]
#y2 = [16, 32, 64, 576, 424*8]

#y1 = [2048, 2048, 2048, 256, 256, 256]
#y2 = [12*8, 72*8, 42*8, 402*8, 420*8, 6*8]

#ECC Results n vs P
#x = np.arange(1, 8)
#y1 = [2048, 2048, 4096, 512, 512, 256, 256]
#y2 = [24*8, 72*8, 180*8, 1008*8, 1020*8, 576, 0]

#Emulator conference
x = np.arange(1, 5)
y1=[4.370447577262874, 4.3937943777026, 8.0, 9.998046875]
y2=[math.log2(256*8), math.log2(1024*8), math.log2(256*32), math.log2(1024*32)]
# Plotting
plt.figure(figsize=(8, 5))

#ECC Results n vs P
#plt.bar(x - 0.2, y1, width=0.4, label='Nr. n of samples', color='blue')
#plt.bar(x + 0.2, y2, width=0.4, label='Min. Nr. of parity bits', color='green')

#Emulator conference
plt.bar(x - 0.2, y1, width=0.4, label='CR Cap. in bits per obs.', color='blue')
plt.bar(x + 0.2, y2, width=0.4, label='$2^y$ bits of mem. resource', color='cyan')

plt.xlabel('Order of Quantization')
#plt.ylabel('Y-axis')
#plt.xticks(x, ['1', '2', '4', '8', '8[NF]'])
#ECC Results n vs P
#plt.xticks(x, ['Hu\net al', 'Ali\net al', 'Megha\net al', 'Megha\net alMQ', 'Jana\net alMQ', 'CR', 'Ideal'])

#Emulator conference
plt.xticks(x, ['RSSI 8-bit\nn=256', 'RSSI 8-bit\nn=1024', 'RSSI 32-bit\nn=256', 'RSSI 32-bit\nn=1024'])
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
          ncols=4, mode="expand", borderaxespad=0.)
plt.grid()
plt.show()
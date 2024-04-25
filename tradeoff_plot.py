import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['text.usetex'] = True
plt.rcParams.update({'font.family': 'Times New Roman', 'font.size': 50, })

# Data
x = np.arange(1, 5)
y1 = [2048, 1024, 512, 256]
y2 = [16, 32, 64, 576]

# Plotting
plt.figure(figsize=(8, 5))

plt.bar(x - 0.2, y1, width=0.4, label='Nr. n of samples', color='blue')
plt.bar(x + 0.2, y2, width=0.4, label='Min. Nr. of parity bits', color='green')

plt.xlabel('Order of Quantization')
#plt.ylabel('Y-axis')
plt.xticks(x, ['1', '2', '4', '8'])
plt.legend()
plt.grid()
plt.show()
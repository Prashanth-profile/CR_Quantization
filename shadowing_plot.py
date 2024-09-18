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

#Shadowing profile conference
x = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
#y=[0, -10, -20, -25, -35, -35, -15, -18, - 5, -5, 0]
y=[0, -10, -20, -30, -40, -50, -40, -30, - 20, -10, 0]

#Speeding profile journal
#x = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
#y=[1, 1, 5, 30, 100, 100, 100, 100, 70, 60, 30]

# Plotting
plt.figure(figsize=(8, 5))

plt.plot(x, y, color='black')

plt.xlabel('Time in seconds')
plt.ylabel('Attenuation in dB')
#plt.xticks(x, ['1', '2', '4', '8', '8[NF]'])
plt.grid()
plt.show()
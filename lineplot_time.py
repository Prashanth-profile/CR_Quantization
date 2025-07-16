import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['text.usetex'] = True
plt.rcParams.update({'font.family': 'Times New Roman', 'font.size': 50, })
plt.grid()

# Sample data
#x = [1, 2, 3, 4, 5]
y = [10, 20, 15, 25, 30]

n=[128, 256, 512, 1024, 2048, 4096]
Y_bits_cr=[112, 256, 576, 1280, 2816, 6144]
Y_bits_pcr=[28672, 65536, 147456, 327680, 720896, 1572864]


x_label=['256', '2048', '16384', '131072', '405120'] #bytes
x = np.arange(len(x_label))
x_cr=[256, 2048, 16384, 131072, 405120]
Y_time_cr=[0.01515500000000003, 0.12685190000000013, 2.0385261000000003, 464.1688067, 4900.890062400001]
Y_cr_n=[256, 2048, 16384, 131072, 405120]
y_cr_quant=[8, 11, 13]
Y_time_pcr=[6.28999999996438e-05, 0.0001289999999998237, 0.0006892000000000564, 0.004947099999999871, 0.035995699999999964]
Y_pcr_n=[4, 8, 64, 512, 4096]
Y_pcr_quant=[2, 3, 6, 9, 12]
Y_time_MT=[4.259999999997599e-05, 2.569999999998962e-05, 3.729999999999012e-05, 0.0001880999999999966, 0.0005893999999999899]

Y_total_cr=0.3*np.array(Y_cr_n)
Y_total_pcr=0.3*np.array(Y_pcr_n)+np.array(Y_time_pcr)
Y_total_802156=0.015*np.array(Y_cr_n)
Y_total_80211a=0.05*np.array(Y_cr_n)
Y_total_802154=0.01*np.array(Y_cr_n)
Y_total_irs=0.002*np.array(Y_cr_n)

Y_cr_obs=0.3*np.array(Y_cr_n)
Y_cr_comp=np.array(Y_time_cr)
Y_pcr_comp=np.array(Y_time_pcr)

# Create the plot
#plt.plot(x, Y_total_pcr, marker='o', linestyle='-', color='b', label='CFO-CR PCR')
plt.plot(x, Y_total_cr, marker='o', linestyle='-', color='r', label='RSSI-CR')
plt.plot(x, Y_total_802156, marker='o', linestyle='-', color='c', label='IEEE 802.15.6')
#plt.plot(x, Y_total_pcr, marker='o', linestyle='-', color='k', label='IEEE 802.15.6 + MT')
plt.plot(x, Y_total_80211a, marker='o', linestyle='-', color='magenta', label='IEEE 802.11a')
plt.plot(x, Y_total_802154, marker='o', linestyle='-', color='black', label='IEEE 802.15.4')
plt.plot(x, Y_total_irs, marker='o', linestyle='-', color='yellow', label='IRS')
#plt.plot(x, Y_total_pcr, marker='o', linestyle='-', color='k', label='IEEE 802.15.6 + MT')

#plt.plot(x, Y_cr_obs, marker='o', linestyle='-', color='b', label='$T_{obs}$')
#plt.plot(x, Y_cr_comp, marker='o', linestyle='-', color='r', label='$T_{CR}$')
#plt.plot(x, Y_pcr_comp, marker='o', linestyle='-', color='k', label='PCR Tcomp')

#Y_total_cr=0.015*np.array(Y_cr_n)+np.array(Y_time_cr)
#Y_total_pcr=0.015*np.array(Y_pcr_n)+np.array(Y_time_pcr)

#plt.plot(x, Y_total_pcr, marker='o', linestyle='-', color='k', label='IEEE 802.15.6 PCR')

# Labels and title
plt.xticks(x, x_label)  # Set x-axis labels
plt.xlabel('Size of CR')
plt.ylabel('Time in seconds')

# Show legend
plt.legend()

# Show the plot
plt.show()

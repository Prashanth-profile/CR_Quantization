import math

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import matplotlib.pyplot as plt2

plt.rcParams['text.usetex'] = True
plt.rcParams.update({'font.family': 'Times New Roman', 'font.size': 50, })
plt.grid()

# Sample data
x_label=['256', '512', '1024', '2048', '4096', '8192', '16384'] #bytes
x_label2=['256', '576', '1280', '2816', '6144', '13312', '28672']
#x_label=['CFO-CR', 'IEEE 802.15.6', 'IEEE 802.11a', 'IEEE 802.15.4', 'IRS'] #bytes
x = np.arange(len(x_label2))
x_cr=[256, 2048, 16384, 131072, 405120]
Y_time_cr=[0.01515500000000003, 0.12685190000000013, 2.0385261000000003, 464.1688067, 4900.890062400001]
Y_cr_n2=[256, 576, 1280, 2816, 6144, 13312, 28672]
Y_cr_n=[256, 512, 1024, 2048, 4096, 8192, 16384]
adaptive_quant=[1,2,3]
Y_IT_rate=[23.76, 1.68, 0.78]


#Y_total_cr=0.3*np.array(Y_cr_n)
Y_total_802156=0.015*np.array(Y_cr_n)
Y_total_80211a=0.05*np.array(Y_cr_n)
Y_total_802154=0.01*np.array(Y_cr_n)
Y_total_irs=0.004*np.array(Y_cr_n)

#YY_total_cr=np.divide((np.array(Y_cr_n)*np.log2(np.array(Y_cr_n))), 8*Y_total_cr)
YY_total_802156=np.divide((np.array(Y_cr_n)*np.log2(np.array(Y_cr_n))), 8*0.015*np.array(Y_cr_n))
YY_total_80211a=np.divide((np.array(Y_cr_n)*np.log2(np.array(Y_cr_n))), 8*0.05*np.array(Y_cr_n))
YY_total_802154=np.divide((np.array(Y_cr_n)*np.log2(np.array(Y_cr_n))), 8*0.01*np.array(Y_cr_n))
YY_total_irs=np.divide((np.array(Y_cr_n)*np.log2(np.array(Y_cr_n))), 8*0.004*np.array(Y_cr_n))

#Enable for IT rate
Y_total_IT_rate=[Y_IT_rate, Y_IT_rate, Y_IT_rate]

Y_cr_obs=0.3*np.array(Y_cr_n)
Y_cr_comp=np.array(Y_time_cr)

#YY_totoal=[YY_total_cr, YY_total_802156, YY_total_80211a, YY_total_802154, YY_total_irs]
YY_totoal=[YY_total_802156, YY_total_80211a, YY_total_802154, YY_total_irs]
YY_precfocr=np.divide([4, 1.3, 36.8, 84.73], 8)
XX_total=['', 'IEEE\n802.15.6', 'IEEE\n802.11a', 'IEEE\n802.15.4', 'IRS+IEEE\n802.11n']
X = np.arange(len(XX_total))
eight=[8, 8, 8, 8]
eight_time=[0.015, 0.05, 0.01, 0.004]
Y_eight=[256, 256, 256, 256]

YY_eight_rate=np.divide(np.array(eight)*(np.array(Y_eight)), 8*np.array(eight_time)*np.array(Y_eight))


# Create the plot
#plt.plot(x, Y_total_pcr, marker='o', linestyle='-', color='b', label='CFO-CR PCR')
#plt.plot(x, YY_total_cr, marker='o', linestyle='-', color='red', label='CFO-CR CR')
#plt.plot(x, YY_total_80211a, marker='o', linestyle='-', color='magenta', label='IEEE 802.11a')
#plt.plot(x, YY_total_802156, marker='o', linestyle='-', color='black', label='IEEE 802.15.6')
#plt.plot(x, YY_total_802154, marker='o', linestyle='-', color='orange', label='IEEE 802.15.4')
#plt.plot(x, YY_total_irs, marker='o', linestyle='-', color='yellow', label='IRS')
#plt.plot(x, Y_total_pcr, marker='o', linestyle='-', color='k', label='IEEE 802.15.6 + MT')
#Enable for temporal rate

plt.plot(X[1:], YY_precfocr, 'bs', label='Secret Key Rate', markersize=14)
region_marker1 = mlines.Line2D([], [], color='blue', marker='s', linestyle='None',
                              markersize=10, label='$\eta=8$-bit achieved\nTemporal CR Rate')
plt.plot(X[1:], YY_eight_rate, 'rs', label='8-bit RSSI', markersize=14)
region_marker2 = mlines.Line2D([], [], color='red', marker='s', linestyle='None',
                              markersize=10, label='$\eta=8$-bit max\nTemporal CR Rate')
plt.boxplot(YY_totoal, patch_artist=True, boxprops=dict(facecolor='skyblue'))

legend_handles = [plt.Line2D([0], [0], color='skyblue', lw=4, label='$\eta=32$-bit max\nTemporal CR Rate'), region_marker2, region_marker1]


# Labels and title
plt.xticks(X, XX_total)  # Set x-axis labels
plt.xlabel('State-of-the-art Category')
plt.ylabel('Temporal CR rate in bytes/s')


# Show legend
plt.legend(handles=legend_handles)

# Show the plot
plt.show()
#plt2.show()

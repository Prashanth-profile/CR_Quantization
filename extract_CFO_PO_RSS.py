import matplotlib.pyplot as plt2
import plot_RSSI
import plot_CFO
import plot_PO
import math
import correlation_calculation
import plot_correlation
import noise_removal

fontsz=50
min_length=1024
time=range(min_length)
ind=0
win=1024

#########################################RSSI########################################
#Read the text file
with open('C:/Users/prashanth/Desktop/SDR1_RSSI_8bit.txt', 'r') as fin:
    data_read_SDR1 = fin.read()
    last_char_SDR1 = data_read_SDR1[-1]
    if last_char_SDR1 == '\n':
        print("last next line character detected in first sample file")
        data_read_SDR1 = data_read_SDR1[:-1]
with open('C:/Users/prashanth/Desktop/SDR2_RSSI_8bit.txt', 'r') as fin:
    data_read_SDR2 = fin.read()
    last_char_SDR2 = data_read_SDR2[-1]
    if last_char_SDR2 == '\n':
        print("last next line character detected in second sample file")
        data_read_SDR2 = data_read_SDR2[:-1]

'''with open('C:/Users/prashanth/Desktop/Logs Freqsweep/RSSI_Freqsweep_132_SDR1.txt', 'r') as fin:
    data_read_SDR1 = fin.read()
with open('C:/Users/prashanth/Desktop/Logs Freqsweep/RSSI_Freqsweep_132_SDR2.txt', 'r') as fin:
    data_read_SDR2 = fin.read()'''

# average = mean(data)
# print(average)
data_read_SDR1 = data_read_SDR1.replace(',', '.')
data_read_SDR2 = data_read_SDR2.replace(',', '.')

#Split the data based on escape character \n
list_of_strings_SDR1 = data_read_SDR1.split('\n')
list_of_strings_SDR2 = data_read_SDR2.split('\n')

#Convert string to float
list_of_floats_SDR1 = [int(x) for x in list_of_strings_SDR1]
list_of_floats_SDR2 = [int(x) for x in list_of_strings_SDR2]
list_of_floats_SDR1, list_of_floats_SDR2 = zip(*[
    (a, b) for a, b in zip(list_of_floats_SDR1, list_of_floats_SDR2) if a <= 0
])

#SDR1_1_norm=noise_removal.window_smoothening(list_of_floats_SDR1[ind:ind+min_length], win)
#SDR2_1_norm=noise_removal.window_smoothening(list_of_floats_SDR2[ind:ind+min_length], win)


#fig2, (ax1, ax2, ax3) = plt2.subplots(3, 1)
#fig3, (ax1, ax2) = plt2.subplot(2,1)
plt2.rcParams['text.usetex'] = True
plt2.rcParams.update({'font.family': 'Times New Roman', 'font.size': fontsz})
fig2, axis = plt2.subplots()
#fig, axis = plt2.subplot_mosaic([['top', 'top']],
#                                  empty_sentinel="BLANK")
plt2.grid()

#plot_RSSI.plot_RSSI(time, list_of_floats_SDR1[ind:ind+min_length], list_of_floats_SDR2[ind:ind+min_length], ax1)

corr_coeff_rssi, number_of_samples_rssi = correlation_calculation.complete_correlation(min_length, list_of_floats_SDR1[ind:ind+min_length],
                                                                             list_of_floats_SDR2[ind:ind+min_length])
#corr_coeff_smoothrssi, number_of_samples_smoothrssi = correlation_calculation.complete_correlation(min_length, SDR1_1_norm,
#                                                                             SDR2_1_norm)
#######################################CFO##############################################
#Read the text file
with open('C:/Users/prashanth/Desktop/SDR1_RSSI_16bit.txt', 'r') as fin:
    data_read_SDR1 = fin.read()
    last_char_SDR1 = data_read_SDR1[-1]
    if last_char_SDR1 == '\n':
        print("last next line character detected in first sample file")
        data_read_SDR1 = data_read_SDR1[:-1]
with open('C:/Users/prashanth/Desktop/SDR2_RSSI_16bit.txt', 'r') as fin:
    data_read_SDR2 = fin.read()
    last_char_SDR2 = data_read_SDR2[-1]
    if last_char_SDR2 == '\n':
        print("last next line character detected in second sample file")
        data_read_SDR2 = data_read_SDR2[:-1]

# average = mean(data)
# print(average)
data_read_SDR1 = data_read_SDR1.replace(',', '.')
data_read_SDR2 = data_read_SDR2.replace(',', '.')

#Split the data based on escape character \n
list_of_strings_SDR1 = data_read_SDR1.split('\n')
list_of_strings_SDR2 = data_read_SDR2.split('\n')

#Convert string to float
list_of_floats_SDR1 = [float(x) for x in list_of_strings_SDR1]
list_of_floats_SDR2 = [float(x) for x in list_of_strings_SDR2]
#list_of_floats_SDR1 = list(map(lambda x: x*-1 if x < 0 else x, list_of_floats_SDR1))
#list_of_floats_SDR2 = list(map(lambda x: x*-1 if x < 0 else x, list_of_floats_SDR2))
list_of_floats_SDR1, list_of_floats_SDR2 = zip(*[
    (a, b) for a, b in zip(list_of_floats_SDR1, list_of_floats_SDR2) if a <= 0
])

#SDR1_1_norm=noise_removal.window_smoothening(list_of_floats_SDR1[ind:ind+min_length], win)
#SDR2_1_norm=noise_removal.window_smoothening(list_of_floats_SDR2[ind:ind+min_length], win)

print("length", len(list_of_floats_SDR1))

#plot_CFO.plot_CFO(time, list_of_floats_SDR1[ind:ind+min_length], list_of_floats_SDR2[ind:ind+min_length], ax2)

corr_coeff_cfo, number_of_samples_cfo = correlation_calculation.complete_correlation(min_length, list_of_floats_SDR1[ind:ind+min_length],
                                                                             list_of_floats_SDR2[ind:ind+min_length])
#corr_coeff_smoothcfo, number_of_samples_smoothcfo = correlation_calculation.complete_correlation(min_length, SDR1_1_norm,
#                                                                             SDR2_1_norm)

#######################################PO##############################################
#Read the text file
'''with open('C:/Users/prashanth/Desktop/PO_SC_212_SDR1.txt', 'r') as fin:
    data_read_SDR1 = fin.read()
    last_char_SDR1 = data_read_SDR1[-1]
    if last_char_SDR1 == '\n':
        print("last next line character detected in first sample file")
        data_read_SDR1 = data_read_SDR1[:-1]
with open('C:/Users/prashanth/Desktop/PO_SC_212_SDR2.txt', 'r') as fin:
    data_read_SDR2 = fin.read()
    last_char_SDR2 = data_read_SDR2[-1]
    if last_char_SDR2 == '\n':
        print("last next line character detected in second sample file")
        data_read_SDR2 = data_read_SDR2[:-1]

# average = mean(data)
# print(average)
data_read_SDR1 = data_read_SDR1.replace(',', '.')
data_read_SDR2 = data_read_SDR2.replace(',', '.')

#Split the data based on escape character \n
list_of_strings_SDR1 = data_read_SDR1.split('\n')
list_of_strings_SDR2 = data_read_SDR2.split('\n')

#Convert string to float
list_of_floats_SDR1 = [float(x) for x in list_of_strings_SDR1]
list_of_floats_SDR2 = [float(x) for x in list_of_strings_SDR2]
list_of_floats_SDR1 = list(map(lambda x: x*-1 if x < 0 else x, list_of_floats_SDR1))
list_of_floats_SDR2 = list(map(lambda x: x*-1 if x < 0 else x, list_of_floats_SDR2))


SDR1_1_norm=noise_removal.window_smoothening(list_of_floats_SDR1[ind:ind+min_length], win)
SDR2_1_norm=noise_removal.window_smoothening(list_of_floats_SDR2[ind:ind+min_length], win)

print("length", len(list_of_floats_SDR1))

#plot_CFO.plot_CFO(time, list_of_floats_SDR1[ind:ind+min_length], list_of_floats_SDR2[ind:ind+min_length], ax2)

corr_coeff_po, number_of_samples_po = correlation_calculation.complete_correlation(min_length, list_of_floats_SDR1[ind:ind+min_length],
                                                                             list_of_floats_SDR2[ind:ind+min_length])

corr_coeff_smoothpo, number_of_samples_smoothpo = correlation_calculation.complete_correlation(min_length, SDR1_1_norm,
                                                                             SDR2_1_norm)

#######################################POW##############################################
#Read the text file
with open('C:/Users/prashanth/Desktop/VOL_SC_212_SDR1.txt', 'r') as fin:
    data_read_SDR1 = fin.read()
    last_char_SDR1 = data_read_SDR1[-1]
    if last_char_SDR1 == '\n':
        print("last next line character detected in first sample file")
        data_read_SDR1 = data_read_SDR1[:-1]
with open('C:/Users/prashanth/Desktop/VOL_SC_212_SDR2.txt', 'r') as fin:
    data_read_SDR2 = fin.read()
    last_char_SDR2 = data_read_SDR2[-1]
    if last_char_SDR2 == '\n':
        print("last next line character detected in second sample file")
        data_read_SDR2 = data_read_SDR2[:-1]

# average = mean(data)
# print(average)
data_read_SDR1 = data_read_SDR1.replace(',', '.')
data_read_SDR2 = data_read_SDR2.replace(',', '.')

#Split the data based on escape character \n
list_of_strings_SDR1 = data_read_SDR1.split('\n')
list_of_strings_SDR2 = data_read_SDR2.split('\n')

#Convert string to float
list_of_floats_SDR1 = [float(x) for x in list_of_strings_SDR1]
list_of_floats_SDR2 = [float(x) for x in list_of_strings_SDR2]
list_of_floats_SDR1 = list(map(lambda x: x*-1 if x < 0 else x, list_of_floats_SDR1))
list_of_floats_SDR2 = list(map(lambda x: x*-1 if x < 0 else x, list_of_floats_SDR2))


SDR1_1_norm=noise_removal.window_smoothening(list_of_floats_SDR1[ind:ind+min_length], win)
SDR2_1_norm=noise_removal.window_smoothening(list_of_floats_SDR2[ind:ind+min_length], win)'''

print("length", len(list_of_floats_SDR1))

#plot_CFO.plot_CFO(time, list_of_floats_SDR1[ind:ind+min_length], list_of_floats_SDR2[ind:ind+min_length], ax2)

corr_coeff_vol, number_of_samples_vol = correlation_calculation.complete_correlation(min_length, list_of_floats_SDR1[ind:ind+min_length],
                                                                             list_of_floats_SDR2[ind:ind+min_length])
#corr_coeff_smoothvol, number_of_samples_smoothvol = correlation_calculation.complete_correlation(min_length, SDR1_1_norm,
#                                                                             SDR2_1_norm)

#plot_correlation.correlation_plot(number_of_samples_smoothcfo, corr_coeff_smoothcfo, axis, 'b--', "CFO smooth")
plot_correlation.correlation_plot(number_of_samples_rssi, corr_coeff_rssi, axis, 'r-', "RSSI $\eta=8$-bits")
plot_correlation.correlation_plot(number_of_samples_cfo, corr_coeff_cfo, axis, 'b-', "RSSI $\eta=16$-bits")
#plot_correlation.correlation_plot(number_of_samples_cfo_0dB, corr_coeff_cfo_0dB, axis, 'c-', "CFO 0dB")
#plot_correlation.correlation_plot(number_of_samples_smoothrssi, corr_coeff_smoothrssi, axis, 'r--', "RSSI smooth")
#plot_correlation.correlation_plot(number_of_samples_smoothvol, corr_coeff_smoothvol, axis, 'k--', "Amplitude smooth")
#plot_correlation.correlation_plot(number_of_samples_vol, corr_coeff_vol, axis, 'k-', "Amplitude")
#plot_correlation.correlation_plot(number_of_samples_smoothpo, corr_coeff_smoothpo, axis, 'g--', "Phase Offset smooth")
#plot_correlation.correlation_plot(number_of_samples_po, corr_coeff_po, axis, 'g-', "Phase Offset")
#plot_correlation.correlation_plot(number_of_samples_smoothrssi, corr_coeff_smoothrssi, axis, 'r--', "RSSI smoothened")
#plot_correlation.correlation_plot(number_of_samples_smoothcfo, corr_coeff_smoothcfo, axis, 'b--', "CFO smoothened")
#plot_correlation.correlation_plot(number_of_samples_smoothpo, corr_coeff_smoothpo, axis, 'g--', "Phase Offset smoothened")
#plot_correlation.correlation_plot(number_of_samples_smoothvol, corr_coeff_smoothvol, axis, 'k--', "Voltage smoothened")

#######################################PO##############################################
#Read the text file
#plt2.rcParams['font.family'] = 'Times New Roman'  # Specify the font family
plt2.rcParams['font.size'] = fontsz  # Specify the font size
plt2.xticks(fontsize=fontsz)  # Specify the font size for x-axis tick labels
plt2.yticks(fontsize=fontsz)  # Specify the font size for y-axis tick labels
plt2.show()
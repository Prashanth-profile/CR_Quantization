import matplotlib.pyplot as plt2
import main
import plot_RSSI
import plot_CFO
import plot_PO
import math


min_length=128
time=range(min_length)
ind=0

#########################################RSSI########################################
#Read the text file
with open('C:/Users/prashanth/Desktop/Logs SC 1302/Logs 500ms/RSSI_SC_132_SDR1.txt', 'r') as fin:
    data_read_SDR1 = fin.read()
with open('C:/Users/prashanth/Desktop/Logs SC 1302/Logs 500ms/RSSI_SC_132_SDR2.txt', 'r') as fin:
    data_read_SDR2 = fin.read()

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


fig2, (ax1, ax2, ax3) = plt2.subplots(3, 1)


plot_RSSI.plot_RSSI(time, list_of_floats_SDR1[ind:ind+min_length], list_of_floats_SDR2[ind:ind+min_length], ax1)

#######################################CFO##############################################
#Read the text file
with open('C:/Users/prashanth/Desktop/Logs SC 1302/Logs 500ms/CFO_SC_132_SDR1.txt', 'r') as fin:
    data_read_SDR1 = fin.read()
with open('C:/Users/prashanth/Desktop/Logs SC 1302/Logs 500ms/CFO_SC_132_SDR2.txt', 'r') as fin:
    data_read_SDR2 = fin.read()

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

plot_CFO.plot_CFO(time, list_of_floats_SDR1[ind:ind+min_length], list_of_floats_SDR2[ind:ind+min_length], ax2)

#######################################PO##############################################
#Read the text file
with open('C:/Users/prashanth/Desktop/Logs SC 1302/Logs 500ms/PO_SC_132_SDR1.txt', 'r') as fin:
    data_read_SDR1 = fin.read()
with open('C:/Users/prashanth/Desktop/Logs SC 1302/Logs 500ms/PO_SC_132_SDR2.txt', 'r') as fin:
    data_read_SDR2 = fin.read()

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
#list_of_floats_SDR1 = list(map(lambda x: x*-1 if x > 0 else x, list_of_floats_SDR1))
#list_of_floats_SDR2 = list(map(lambda x: x*-1 if x < 0 else x, list_of_floats_SDR2))
#print("list of float ", list_of_floats_SDR1)

#time_offset_SDR1 = [[i * math.pi/ (2*180) for i in x] for x in zip(list_of_floats_SDR1)]
#time_offset_SDR2 = [[i * math.pi / (2*180) for i in x] for x in zip(list_of_floats_SDR2)]
#print("time offset ", time_offset_SDR1)

plot_PO.plot_PO(time, list_of_floats_SDR1[ind:ind+min_length], list_of_floats_SDR2[ind:ind+min_length], ax3)

plt2.show()

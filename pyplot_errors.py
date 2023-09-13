import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager

# Sample data
#x = ['RSSI Mean', 'RSSI Median', 'CFO Mean', 'CFO Median', 'QE']
#x= ['NF Mean', 'NF Median', 'US Mean', 'US Median', 'Gauss Mean', 'Gauss Median']
x= ['2bit NF', '2bit US', '2bit Gaus', '8bit NF', '8bit US', '8bit Gaus', '16bit NF', '16bit US', '16bit Gaus']
#y1 = [165, 174, 154]
#y2= [1024, 1024, 1024]
'''y00med=[279, 208, 260, 430, 480, 315, 503, 510, 431, 230, 325, 317, 265, 240, 281, 231]
y00men=[276, 202, 261, 337, 325, 273, 367, 329, 300, 202, 293, 285, 242, 250, 243, 198]
y1=[86, 76, 137, 85, 117, 92, 102, 127, 111, 93, 85, 50, 82, 91, 79, 89]
y2=[62, 80, 118, 98, 110, 84, 112, 142, 102, 92, 96, 52, 76, 74, 90, 94]
y3= [91, 103, 88, 93, 118, 93, 104, 104, 86, 94, 96, 93, 107, 80, 83, 93]'''
#Quantization 8
#y1=[3325, 1843, 1578, 2109, 3496, 3460, 3666, 1857, 2697, 3764, 3022, 3027, 1818, 3751, 2590, 2044]
#y2=[1644, 1430, 2604, 1852, 1592, 1881, 2151, 2754, 2316, 1536, 1743, 1470, 1810, 1960, 2299, 1803]
#y3=[1572, 1433, 2098, 1767, 1892, 1711, 2068, 2516, 2346, 1686, 2303, 1442, 1897, 2156, 2186, 1798]

#Quantization 2
'''y1=[124, 45, 50, 49, 160, 187, 396, 23, 174, 444, 159, 212, 55, 376, 97, 56]
y2=[7, 15, 52, 25, 45, 29, 22, 67, 61, 29, 17, 13, 10, 19, 34, 11]
y3=[17, 22, 24, 16, 31, 9, 39, 42, 50, 34, 27, 13, 14, 36, 45, 13]'''


#Quantization 1
#y1_mean=[23, 20, 32, 29, 53, 28, 45, 39, 35, 24, 26, 16, 30, 22, 19, 49]
#y1_median=[28, 26, 28, 34, 48, 30, 46, 38, 52, 30, 28, 10, 36, 28, 18, 36]
#y2_mean=[14, 2, 6, 15, 44, 7, 13, 7, 32, 8, 2, 1, 7, 0, 4, 9]
#y3_mean=[7, 3, 4, 18, 32, 5, 7, 4, 7, 5, 3, 1, 4, 1, 6, 9]
#y2_median=[12, 4, 10, 18, 20, 6, 14, 6, 14, 18, 2, 2, 6, 4, 4, 18]
#y3_median=[22, 2, 12, 18, 12, 10, 4, 6, 12, 12, 4, 2, 8, 6, 4, 12]

#CR Rate
y1=[0.5774299696421278, 0.6140046484714721, 0.5151897715991678, 0.41876665875094893, 0.4710722363655379, 0.5421631605563811, 0.5590146258986616, 0.3040029952592252, 0.6450401671707505, 0.33156517898849946, 0.49463213543577034, 0.5132662293984313, 0.6036429950488245, 0.562194305466448, 0.7298406714536945, 0.5590619764580668]
y2=[0.36679233631592495, 0.4168340142745747, 0.45743915737828444, 0.3935457331526545, 0.37598163247998945, 0.3740494596779801, 0.41659608367378376, 0.3705916031703557, 0.3259829184222826, 0.40563831495140784, 0.42879318121545035, 0.44123394930265847, 0.4216668749784454, 0.3950434350403225, 0.4617793782235333, 0.37688410084854856]
y3=[0.3549724211816885, 0.4053549848325445, 0.4591220767914284, 0.38224368521039986, 0.36577133472381285, 0.3507138290977903, 0.3975358814145674, 0.35542199225583637, 0.3177345780863788, 0.43388071537075135, 0.4326600155760746, 0.4410214064113086, 0.4067773187819205, 0.40425622249132886, 0.44350963873008253, 0.37302321302721647]
y4=[2.0747794638389467, 4.84043605579176, 5.009846709241738, 4.159809817545274, 1.8173383298478558, 1.9643653397204268, 1.5446220498529053, 4.279711153945571, 3.1525944343797554, 1.1403316217624784, 2.3588058800414755, 2.258679008719621, 5.0788429870800735, 0.9816266507262524, 3.8420329622484974, 4.4349240417252505]
y5=[4.875115055821873, 5.42529202213602, 3.655909875523498, 4.548906045053154, 5.042004700114607, 4.943724917269898, 4.340196679045109, 3.111989947426227, 3.9611628811833985, 5.267821872546068, 5.069614811057578, 5.765142971820805, 5.169528225272123, 4.912485403300115, 4.322410804211831, 5.107510832322222]
y6=[4.925108801183447, 5.489283440342194, 4.413863892537984, 4.839263649170724, 4.836696285105121, 5.113332447150275, 4.3829763860724915, 3.2960547401582683, 3.7062744378494106, 5.150313673317352, 3.971584147647351, 5.867504486867254, 5.108824769862545, 4.0938500333458965, 4.311395613711471, 5.134600578308269]
y7=[2.366061486454043, 5.19193519834388, 5.455366549045407, 4.631013170552105, 1.9332922988639132, 2.019792784464472, 1.58451650409066, 5.00905690771499, 3.464016806432378, 1.299214601861117, 2.475156570181241, 2.152359526529899, 5.463339695553318, 1.12720825601973, 3.9487981199712063, 4.666343976710941]
y8=[5.498082661522793, 5.897816750489854, 3.7766922155350673, 4.816850606184835, 5.604087775178237, 5.189845626673612, 4.715621526805641, 3.386061942353284, 4.5453717847209605, 5.762924821594576, 5.333499419279107, 6.150162953020745, 5.339886007321245, 5.0695438774736505, 4.341075770463541, 5.253193049948646]
y9=[5.524590519112581, 5.72799224469813, 4.668399593949235, 5.298829908973819, 5.4082861711281724, 5.543539244027891, 4.516848874930713, 3.8351671999824175, 3.954975890786456, 5.507303769434506, 4.100220418152613, 6.0842073965549694, 5.427641252161495, 4.2782654492716015, 4.38480844828792, 5.393886211217633]
yn=[1024]

crcapacity=[0.7784967162172741, 0.4809216603237816, 0.4696713352991236, 7.668814443875758, 7.647773068704821, 7.718302637133822, 15.741388904527554, 15.721526397717652, 15.747632971667972]
idealcrcapacity=[2, 2, 2, 8, 8, 8, 16, 16, 16]

# Set the style
plt.grid()

# Set the width of the bars
bar_width = 0.2

# Generate array for x-axis positions of the bars
x_pos = np.arange(len(x)+1)
fontsz=40

# Create a bar plot
#plt.bar(x_pos, y1, width=bar_width, label='Bit errors', color='skyblue')
#plt.bar(x_pos + bar_width, y2, width=bar_width, label='Nr. of generated bits', color='lightgreen')

# Create a box plot
colors = ['red', 'green', 'blue']
#data = [y00med, y00men, y1, y2, y3]
#data=[y1, y2, y3]
#data=[y1_mean, y1_median, y2_mean, y2_median, y3_mean, y3_median]
data=[y1, y2, y3, y4, y5, y6, y7, y8, y9]
plt.boxplot(data, labels=x, patch_artist=True)


plt.plot(x_pos[1:], crcapacity, color='blue', label="Max CR capacity")
plt.plot(x_pos[1:], idealcrcapacity, color='red', label="Ideal CR capacity")

# Add labels and title
plt.xlabel('Filtering Techniques', fontsize=fontsz, fontname='Times New Roman')
plt.ylabel('Number of bits', fontsize=fontsz, fontname='Times New Roman')
#plt.title('Bit discrepencies for various CR generation techniques', fontsize=fontsz, fontname='Times New Roman')

# Customize tick parameters
#plt.xticks(x_pos + bar_width, x, fontname='Times New Roman', fontsize=fontsz)
plt.xticks(x_pos[1:], x, fontname='Times New Roman', fontsize=fontsz)
plt.yticks(fontsize=fontsz, fontname='Times New Roman')

#plt.hlines(y=2, xmin=x_pos[1], xmax=x_pos[3], colors='red', linestyles='-', lw=2, label='Ideal CR capacity')
#plt.hlines(y=8, xmin=x_pos[4], xmax=x_pos[6], colors='red', linestyles='-', lw=2)
#plt.hlines(y=16, xmin=x_pos[7], xmax=x_pos[9], colors='red', linestyles='-', lw=2)

# Add a legend
#plt.legend(loc='upper right', prop={'family': 'Times New Roman', 'size': fontsz})

'''# Add color labels at the top right corner
plt.text(4.6, max(max(y1), max(y2)) + 0.5, 'Colors:', ha='right', fontsize=fontsz, fontname='Times New Roman')
plt.text(4.6, max(max(y1), max(y2)), 'Bit errors: Skyblue\nNr. of generated bits: Lightgreen', ha='right', fontsize=fontsz, fontname='Times New Roman')'''

'''# Add value labels on top of each bar
for i, j in enumerate(y1):
    plt.text(i, j - 0.2, str(j), ha='center', fontsize=fontsz, fontname='Times New Roman')
for i, j in enumerate(y2[1:]):
    plt.text(i + bar_width, j - 0.2, str(j), ha='center', fontsize=fontsz, fontname='Times New Roman')'''

# Adjust plot margins
plt.margins(0.1)

# Set font style and size for all text elements
font = font_manager.FontProperties(family='Times New Roman', size=fontsz)
for text in plt.gcf().get_axes()[0].texts:
    text.set_fontproperties(font)

# Display the plot
plt.legend()
plt.show()

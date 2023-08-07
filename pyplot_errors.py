import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager

# Sample data
#x = ['RSSI Mean', 'RSSI Median', 'CFO Mean', 'CFO Median', 'QE']
x= ['NF Mean', 'NF Median', 'US Mean', 'US Median', 'Gauss Mean', 'Gauss Median']
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
y1_mean=[23, 20, 32, 29, 53, 28, 45, 39, 35, 24, 26, 16, 30, 22, 19, 49]
y1_median=[28, 26, 28, 34, 48, 30, 46, 38, 52, 30, 28, 10, 36, 28, 18, 36]
y2_mean=[14, 2, 6, 15, 44, 7, 13, 7, 32, 8, 2, 1, 7, 0, 4, 9]
y3_mean=[7, 3, 4, 18, 32, 5, 7, 4, 7, 5, 3, 1, 4, 1, 6, 9]
y2_median=[12, 4, 10, 18, 20, 6, 14, 6, 14, 18, 2, 2, 6, 4, 4, 18]
y3_median=[22, 2, 12, 18, 12, 10, 4, 6, 12, 12, 4, 2, 8, 6, 4, 12]

yn=[1024]

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
data=[y1_mean, y1_median, y2_mean, y2_median, y3_mean, y3_median]
plt.boxplot(data, labels=x, patch_artist=True)

# Add labels and title
plt.xlabel('Filtering Techniques', fontsize=fontsz, fontname='Times New Roman')
plt.ylabel('Number of bits', fontsize=fontsz, fontname='Times New Roman')
#plt.title('Bit discrepencies for various CR generation techniques', fontsize=fontsz, fontname='Times New Roman')

# Customize tick parameters
#plt.xticks(x_pos + bar_width, x, fontname='Times New Roman', fontsize=fontsz)
plt.xticks(x_pos[1:], x, fontname='Times New Roman', fontsize=fontsz)
plt.yticks(fontsize=fontsz, fontname='Times New Roman')

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
plt.show()

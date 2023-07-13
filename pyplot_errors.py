import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager

# Sample data
x = ['Classic Mean', 'Classic Median', 'Quantum Entanglement']
y1 = [216, 210, 154]
y2= [1024, 1024, 1024]

# Set the style
plt.style.use('seaborn-darkgrid')

# Set the width of the bars
bar_width = 0.2

# Generate array for x-axis positions of the bars
x_pos = np.arange(len(x))
fontsz=30

# Create a bar plot
plt.bar(x_pos, y1, width=bar_width, label='Bit errors', color='skyblue')
plt.bar(x_pos + bar_width, y2, width=bar_width, label='Nr. of generated bits', color='lightgreen')

# Add labels and title
plt.xlabel('Categories', fontsize=fontsz, fontname='Times New Roman')
plt.ylabel('Number of bits', fontsize=fontsz, fontname='Times New Roman')
plt.title('Bit discrepencies for various CR generation techniques', fontsize=fontsz, fontname='Times New Roman')

# Customize tick parameters
plt.xticks(x_pos + bar_width, x, fontname='Times New Roman', fontsize=fontsz)
plt.yticks(fontsize=26, fontname='Times New Roman')

# Add a legend
plt.legend(loc='upper right', prop={'family': 'Times New Roman', 'size': fontsz})

# Add color labels at the top right corner
plt.text(4.6, max(max(y1), max(y2)) + 0.5, 'Colors:', ha='right', fontsize=fontsz, fontname='Times New Roman')
plt.text(4.6, max(max(y1), max(y2)), 'Bit errors: Skyblue\nNr. of generated bits: Lightgreen', ha='right', fontsize=fontsz, fontname='Times New Roman')

# Add value labels on top of each bar
for i, j in enumerate(y1):
    plt.text(i, j - 0.2, str(j), ha='center', fontsize=fontsz, fontname='Times New Roman')
for i, j in enumerate(y2[1:]):
    plt.text(i + bar_width, j - 0.2, str(j), ha='center', fontsize=fontsz, fontname='Times New Roman')

# Adjust plot margins
plt.margins(0.1)

# Set font style and size for all text elements
font = font_manager.FontProperties(family='Times New Roman', size=fontsz)
for text in plt.gcf().get_axes()[0].texts:
    text.set_fontproperties(font)

# Display the plot
plt.show()

import matplotlib.pyplot as plt
import numpy as np

# Sample data
labels = ['LQ(mean)', 'LQ(median)', 'WTQ(mean)', 'WTQ(median)', '2bit', '2bit(Gray)', '4bit', '4bit(Gray)', '8bit', '8bit(Gray)']
values1 = [14, 14, 15, 12, 36, 33, 123, 109, 328, 308]
values2 = [128, 128, 128, 128, 256, 256, 512, 512, 1024, 1024]

# Set the width of each bar
bar_width = 0.35

# Create a figure and axis object
fig, ax = plt.subplots()

# Set the position of the bars on the x-axis
x_pos = np.arange(len(labels))

# Create the first bar plot and set the color to blue
rects1 = ax.bar(x_pos - bar_width/2, values1, bar_width, color='blue', label='Number of errors')

# Create the second bar plot and set the color to green
rects2 = ax.bar(x_pos + bar_width/2, values2, bar_width, color='green', label='Number of bits generated')

# Add x-axis and y-axis labels
ax.set_xlabel('Category of Quantization')
ax.set_ylabel('Number of Bits')

# Add a title to the plot
ax.set_title('Two Bar Plot')

# Add x-axis ticks and labels
ax.set_xticks(x_pos)
ax.set_xticklabels(labels)

# Add a legend to the plot
ax.legend()

# Show the plot
plt.show()
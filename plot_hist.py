import numpy as np
import matplotlib.pyplot as plt

# Generate random integer data (replace these with your actual data arrays)
data1 = np.random.randint(1, 11, size=100)
data2 = np.random.randint(1, 11, size=150)
data3 = np.random.randint(1, 11, size=200)

# Create a histogram for each data set
plt.hist(data1, bins=np.arange(min(data1), max(data1) + 1.5) - 0.5, alpha=0.5, edgecolor='black', label='Data 1')
plt.hist(data2, bins=np.arange(min(data2), max(data2) + 1.5) - 0.5, alpha=0.5, edgecolor='black', label='Data 2')
plt.hist(data3, bins=np.arange(min(data3), max(data3) + 1.5) - 0.5, alpha=0.5, edgecolor='black', label='Data 3')

# Add a legend
plt.legend()

# Add labels and title
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('Histogram Comparison of Multiple Data Sets')

# Show the plot
plt.show()

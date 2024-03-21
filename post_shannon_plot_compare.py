import matplotlib.pyplot as plt
import numpy as np
import math

# Sample data for the bar plot
categories = ['Shannon', 'ID codes Local Randomness', 'ID codes CR error corrected using Reed Solomon', 'ID codes errorless Common Randomness']
values = [math.log2(1*256), math.log2(128*256), math.log2(146.28*256), math.log2(256*256)]

# Create a bar plot
plt.bar(categories, values, color='blue', alpha=0.7, label='Bar Plot')

# Add a red straight line (e.g., reference line, mean line, etc.)
red_line_value = 8  # Adjust this value as needed
plt.axhline(y=red_line_value, color='red', linestyle='--', label='Shannon Limit')

# Adding labels and title
plt.xlabel('Categories')
plt.ylabel('Transmission capacity in Bytes per frame in logarithmic scale')
plt.title('How common randomness helps ID')
plt.legend()

# Show the plot
plt.show()

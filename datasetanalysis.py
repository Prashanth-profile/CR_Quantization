
import numpy as np
from scipy.stats import entropy
import matplotlib.pyplot as plt
plt.rcParams['text.usetex'] = True
fontsz=50
plt.rcParams.update({'font.family': 'Times New Roman', 'font.size': fontsz, })

with open('C:/Users/prashanth/Desktop/CFO_SC_212_SDR1.txt', 'r') as fin:
    data_read_SDR1 = fin.read()
    last_char_SDR1 = data_read_SDR1[-1]
    if last_char_SDR1 == '\n':
        data_read_SDR1 = data_read_SDR1[:-1]
with open('C:/Users/prashanth/Desktop/CFO_SC_212_SDR2.txt', 'r') as fin:
    data_read_SDR2 = fin.read()
    last_char_SDR2 = data_read_SDR2[-1]
    if last_char_SDR2 == '\n':
        data_read_SDR2 = data_read_SDR2[:-1]



# Function to calculate metrics
def calculate_metrics(data):
    # Ensure data is numeric
    data = np.array(data, dtype=float)
    variance = np.var(data, ddof=1)  # Sample variance
    std_deviation = np.std(data, ddof=1)  # Sample standard deviation
    data_range = max(data) - min(data)
    data_probabilities = np.array(data) / sum(data)  # Normalize to probabilities
    data_entropy = entropy(data_probabilities, base=2)  # Entropy in bits
    return variance, std_deviation, data_range, data_entropy

RSSI_data_read_SDR1 = data_read_SDR1.replace(',', '.')
RSSI_data_read_SDR2 = data_read_SDR2.replace(',', '.')

# Split the data based on escape character \n
list_of_strings_SDR1 = RSSI_data_read_SDR1.split('\n')
list_of_strings_SDR2 = RSSI_data_read_SDR2.split('\n')

# Convert string to float
list_of_floats_SDR1 = [float(x) for x in list_of_strings_SDR1]
list_of_floats_SDR2 = [float(x) for x in list_of_strings_SDR2]
list_of_floats_SDR1 = list(map(lambda x: x * -1 if x < 0 else x, list_of_floats_SDR1))
list_of_floats_SDR2 = list(map(lambda x: x * -1 if x < 0 else x, list_of_floats_SDR2))


# Calculate metrics for both lists
metrics1 = calculate_metrics(list_of_floats_SDR1)
metrics2 = calculate_metrics(list_of_floats_SDR2)

# Metrics names
metric_names = ["Variance", "Standard Deviation", "Range", "Entropy"]

# Plotting
x = np.arange(len(metric_names))  # X-axis positions
width = 0.35  # Bar width

fig, ax = plt.subplots(figsize=(10, 6))

# Create bar plots
bars1 = ax.bar(x - width/2, metrics1, width, label='SDR1', color='blue', alpha=0.7)
bars2 = ax.bar(x + width/2, metrics2, width, label='SDR2', color='orange', alpha=0.7)

# Add labels and title
ax.set_xlabel("Metrics")
ax.set_ylabel("Values")
#ax.set_title("Comparison of Variance, Standard Deviation, Range, and Entropy")
ax.set_xticks(x)
ax.set_xticklabels(metric_names)
ax.legend()
ax.grid()

# Annotate bars with values
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # Offset above bar
                    textcoords="offset points",
                    ha='center', va='bottom')

# Show plot
plt.tight_layout()
plt.show()

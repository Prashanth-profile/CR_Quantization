import matplotlib.pyplot as plt
import matplotlib.pyplot as plt2
import seaborn as sns
import numpy as np
from scipy.stats import norm

def create_histogram(rssi_data, nbins, ax, titl, col):

    # Calculate histogram values
    #hist_values, bins, _ = ax.hist(rssi_data, bins=nbins, density=True, edgecolor='black')  # Adjust the number of bins as needed

    # Estimate distribution parameters
    #mu, sigma = np.mean(rssi_data), np.std(rssi_data)

    # Generate curve based on the fitted distribution
    #x = np.linspace(np.min(rssi_data), np.max(rssi_data), nbins+1)
    #pdf = norm.pdf(x, mu, sigma)

    # Generate curve based on distribution parameters
    #curve = norm.pdf(bins, mu, sigma)

    # Plot histogram
    #ax.plot(bins, curve, 'r-', linewidth=2)

    # Set labels and title
    ax.set(xlabel="Quantized Value", ylabel="PDF")
    #ax.legend(loc='upper left')
    #ax.title('Distribution')

    #legend_labels = ['SDR1', 'SDR2']
    #legend_colors = ['blue']

    sns.kdeplot(rssi_data, color=col, label=titl, fill=True, common_norm=True, legend=True, ax=ax)
    #legend_patches = [plt.Rectangle((0, 0), 1, 1, color=color) for color in legend_colors]
    ax.legend()

    # Show the plot
    #plt.show()

# Generate example RSSI data (replace this with your own data)
'''rssi_data = np.random.normal(loc=-70, scale=5, size=1000)  # Example: normal distribution, mean=-70, std=5
fig2, axis= plt.subplots()
create_histogram(rssi_data, 30, axis)
plt.show()'''

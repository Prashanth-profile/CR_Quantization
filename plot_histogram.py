import matplotlib.pyplot as plt
import matplotlib.pyplot as plt2
import seaborn as sns
import numpy as np
from scipy.stats import norm

def create_histogram(rssi_data, nbins, ax, titl):

    # Calculate histogram values
    #hist_values, bins, _ = ax.hist(rssi_data, bins=nbins, density=True, edgecolor='black')  # Adjust the number of bins as needed

    # Estimate distribution parameters
    #mu, sigma = np.mean(rssi_data), np.std(rssi_data)

    # Generate curve based on the fitted distribution
    #x = np.linspace(np.min(rssi_data), np.max(rssi_data), nbins+1)
    #pdf = norm.pdf(x, mu, sigma)

    sns.kdeplot(rssi_data, fill=True, common_norm=True, legend=True, ax=ax)

    # Generate curve based on distribution parameters
    #curve = norm.pdf(bins, mu, sigma)

    # Plot histogram
    #ax.plot(bins, curve, 'r-', linewidth=2)

    # Set labels and title
    ax.set(xlabel="Quantized value", ylabel="Density")
    #ax.legend(loc='upper left')
    #ax.title('Distribution')

    # Show the plot
    #plt.show()

# Generate example RSSI data (replace this with your own data)
'''rssi_data = np.random.normal(loc=-70, scale=5, size=1000)  # Example: normal distribution, mean=-70, std=5
fig2, axis= plt.subplots()
create_histogram(rssi_data, 30, axis)
plt.show()'''

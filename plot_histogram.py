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
    #Enable if using subplots
    #ax.set(xlabel="Bins")

    #ax.legend(loc='upper left')
    #ax.title('Distribution')

    #legend_labels = ['SDR1', 'SDR2']
    #legend_colors = ['blue']

    #Enable if using subplots
    #sns.kdeplot(rssi_data, color=col, label=titl, fill=True, common_norm=True, legend=True, ax=ax)
    #Enable if not using subplots
    #sns.kdeplot(rssi_data, color=col, label=titl, fill=True, common_norm=True, legend=True, ax=ax)
    #sorted_data=np.sort(rssi_data)
    ax.hist(rssi_data, bins=np.arange(min(rssi_data), max(rssi_data) + 2)-0.5, alpha=0.5, edgecolor='black', color=col, histtype='stepfilled')

    mu, sigma = np.mean(rssi_data), np.std(rssi_data)
    x = np.linspace(min(rssi_data), max(rssi_data), 100)
    curve = norm.pdf(x, mu, sigma)
    ax.plot(x, curve, color=col, label=titl)
    #legend_patches = [plt.Rectangle((0, 0), 1, 1, color=color) for color in legend_colors]

    #Enable if using subplots
    ax.legend()

    # Show the plot
    #plt.show()

def plot_with_kde(data, label):
    plt.figure()
    plt.grid()
    plt.plot(data, label=label)
    sns.kdeplot(data, color='r')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title(f'Plot with KDE Overlay - {label}')
    plt.legend()
    plt.show()

# Generate example RSSI data (replace this with your own data)
'''rssi_data = np.random.normal(loc=-70, scale=5, size=1000)  # Example: normal distribution, mean=-70, std=5
fig2, axis= plt.subplots()
create_histogram(rssi_data, 30, axis)
plt.show()'''

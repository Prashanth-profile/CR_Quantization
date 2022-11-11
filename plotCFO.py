def plot_RSSI(time, RSSI_SDR1, RSSI_SDR2, ax):
    ax.plot(time, RSSI_SDR1, 'k-', label='SDR1')
    ax.plot(time, RSSI_SDR2, 'g-', label='SDR2')
    ax.legend(loc='upper left')
    ax.set(xlabel="Number of samples", ylabel="CFO values")
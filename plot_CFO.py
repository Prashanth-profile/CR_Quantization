def plot_CFO(time, CFO_SDR1, CFO_SDR2, ax):
    ax.plot(time, CFO_SDR1, 'k-', label='SDR1')
    ax.scatter(time, CFO_SDR1, color='black')
    ax.plot(time, CFO_SDR2, 'g-', label='SDR2')
    ax.scatter(time, CFO_SDR2, color='green')
    ax.legend(loc='upper left')
    ax.set(xlabel="Frequency in MHz", ylabel="Frequency offset values in Hz")
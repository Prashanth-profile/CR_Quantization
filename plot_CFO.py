def plot_CFO(time, CFO_SDR1, CFO_SDR2, ax):
    ax.plot(time, CFO_SDR1, 'k-', label='SDR1')
    ax.scatter(time, CFO_SDR1, color='black')
    ax.plot(time, CFO_SDR2, 'g-', label='SDR2')
    ax.scatter(time, CFO_SDR2, color='green')
    ax.legend(loc='upper left')
    ax.set(xlabel="Time Index", ylabel="Frequency offset values in Hz")

def plot_CFO_grey(time, CFO_SDR1, CFO_SDR2, ax):
    ax.plot(time, CFO_SDR1, 'r-', label='SDR1g')
    ax.scatter(time, CFO_SDR1, color='red')
    ax.plot(time, CFO_SDR2, 'b-', label='SDR2g')
    ax.scatter(time, CFO_SDR2, color='blue')
    ax.legend(loc='upper left')
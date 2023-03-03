def plot_PO(time, PO_SDR1, PO_SDR2, ax):
    ax.plot(time, PO_SDR1, 'k-', label='SDR1')
    ax.scatter(time, PO_SDR1, color='black')
    ax.plot(time, PO_SDR2, 'g-', label='SDR2')
    ax.scatter(time, PO_SDR2, color='green')
    ax.legend(loc='upper left')
    ax.set(xlabel="Time Index", ylabel="Phase Offset values in rad")
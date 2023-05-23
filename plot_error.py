def plot_error(error_dist, ax, col):
    if col=='r-':
        lbl="Normal"
    else:
        lbl="Gray"
    ax.plot(range(len(error_dist)), error_dist, col, label=lbl)
    ax.legend(loc='upper left')
    ax.set(xlabel="Bit Position", ylabel="Error")
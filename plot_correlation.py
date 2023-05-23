def correlation_plot(time, corr_coeff, ax, colour):
    if colour=='r-':
        ax.plot(time, corr_coeff, colour, label='Correlation of RSSI')
        #ax.scatter(time, corr_coeff, color='red')
    else:
        ax.plot(time, corr_coeff, colour, label='Correlation of Frequency Offset')
        #ax.scatter(time, corr_coeff, color='blue')
    ax.legend(loc='upper right')
    ax.set(xlabel="Time Index", ylabel="Correlation coefficient")

def correlation_plot_lossy(time, corr_coeff, ax, colour, lbl):
    ax.plot(time, corr_coeff, colour, label=lbl)
    #ax.scatter(time, corr_coeff, color='red')
    ax.legend(loc='upper right')
    ax.set(xlabel="Time Index", ylabel="Correlation coefficient of lossy quantization")

def correlation_plot_lossless(time, corr_coeff, ax, colour, lbl):
    ax.plot(time, corr_coeff, colour, label=lbl)
    #ax.scatter(time, corr_coeff, color='red')
    ax.legend(loc='upper right')
    ax.set(xlabel="Time Index", ylabel="Correlation coefficient of 1 bit quantization")

def correlation_plot_multibit(time, corr_coeff, ax, colour, lbl):
    ax.plot(time, corr_coeff, colour, label=lbl)
    #ax.scatter(time, corr_coeff, color='red')
    ax.legend(loc='upper right')
    ax.set(xlabel="Time Index", ylabel="Correlation coefficient of several quantization techniques")
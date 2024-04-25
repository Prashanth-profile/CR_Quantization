def correlation_plot(time, corr_coeff, ax, colour, lbl):
    if colour=='r-':
        ax.plot(time, corr_coeff, colour, label=lbl, linewidth=3)
        #ax.scatter(time, corr_coeff, color='red')
    elif colour=='b-':
        ax.plot(time, corr_coeff, colour, label=lbl, linewidth=3)
    else:
        ax.plot(time, corr_coeff, colour, label=lbl, linewidth=3)
        #ax.scatter(time, corr_coeff, color='blue')
    ax.legend(loc='center right')
    ax.set(xlabel="Number n of samples", ylabel="Correlation coefficient")

def correlation_plot_lossy(time, corr_coeff, ax, colour, lbl):
    ax.plot(time, corr_coeff, colour, label=lbl)
    #ax.scatter(time, corr_coeff, color='red')
    ax.legend(loc='lower right')
    ax.set(xlabel="Time Index", ylabel="Correlation coefficient of lossy quantization", fontsize=40)

def correlation_plot_lossless(time, corr_coeff, ax, colour, lbl):
    ax.plot(time, corr_coeff, colour, label=lbl)
    #ax.scatter(time, corr_coeff, color='red')
    ax.legend(loc='lower right')
    ax.set(xlabel="Time Index", ylabel="Correlation coefficient of 1 bit quantization", fontsize=40)

def correlation_plot_multibit(time, corr_coeff, ax, colour, lbl):
    ax.plot(time, corr_coeff, colour, label=lbl)
    #ax.scatter(time, corr_coeff, color='red')
    ax.legend(loc='lower right', fontsize=25)
    ax.set(xlabel="Time Index", ylabel="Correlation coefficient of several quantization techniques", fontsize=40)
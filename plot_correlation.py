def correlation_plot(time, corr_coeff, ax, colour):
    if colour=='r-':
        ax.plot(time, corr_coeff, colour, label='Uniform Quantization')
        ax.scatter(time, corr_coeff, color='red')
    else:
        ax.plot(time, corr_coeff, colour, label='Threshold Detection')
        ax.scatter(time, corr_coeff, color='blue')
    ax.legend(loc='upper left')
    ax.set(xlabel="Window position", ylabel="Correlation coefficient")
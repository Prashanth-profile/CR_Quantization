def correlation_plot(time, corr_coeff, ax, colour):
    if colour=='r-':
        ax.plot(time, corr_coeff, colour, label='Uniform Quantization')
    else:
        ax.plot(time, corr_coeff, colour, label='Threshold Detection')
    ax.legend(loc='upper left')
    ax.set(xlabel="Number of samples", ylabel="Correlation coefficient")
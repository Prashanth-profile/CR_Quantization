def correlation_plot(time, corr_coeff, ax):
    ax.plot(time, corr_coeff, 'r-')
    ax.set(xlabel="Number of samples", ylabel="Correlation coefficient")
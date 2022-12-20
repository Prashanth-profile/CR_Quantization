def plot_equalbits(common_bits_array, ax, col):
    if col=='c-':
        #ax.plot(number_of_samples, common_bits_array, 'k-', label='SDR1')
        ax.bar(range(len(common_bits_array)), common_bits_array, color='cyan', label='Uniform Quantization')
        #ax.plot(time, RSSI_SDR2, 'g-', label='SDR2')
        #ax.legend(loc='upper left')
    else:
        ax.bar(range(len(common_bits_array)), common_bits_array, color='magenta', label='Threshold Quantization')
    ax.legend(loc='upper left')
    ax.set(xlabel="Number of samples", ylabel="Number of common bits between both SDRs")
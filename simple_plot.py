import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

def manual_plot():
    # Sample data
    labels = ['LQ(mean)', 'LQ(median)', 'WTQ(mean)', 'WTQ(median)', '2bit', '2bit(Gray)', '4bit', '4bit(Gray)', '8bit', '8bit(Gray)']

    print("Number of labels", len(labels))
    values1 = [14, 14, 15, 12, 36, 33, 123, 109, 328, 308]
    values2 = [128, 128, 128, 128, 256, 256, 512, 512, 1024, 1024]

    # Set the width of each bar
    bar_width = 0.35

    # Create a figure and axis object
    fig, ax = plt.subplots()

    # Set the position of the bars on the x-axis
    x_pos = np.arange(len(labels))

    # Create the first bar plot and set the color to blue
    rects1 = ax.bar(x_pos - bar_width/2, values1, bar_width, color='blue', label='Number of errors')

    # Create the second bar plot and set the color to green
    rects2 = ax.bar(x_pos + bar_width/2, values2, bar_width, color='green', label='Number of bits generated')

    # Add x-axis and y-axis labels
    ax.set_xlabel('Category of Quantization')
    ax.set_ylabel('Number of Bits')

    # Add a title to the plot
    ax.set_title('Two Bar Plot')

    # Add x-axis ticks and labels
    ax.set_xticks(x_pos)
    ax.set_xticklabels(labels)

    # Add a legend to the plot
    ax.legend()

    # Show the plot
    plt.show()

#manual_plot()

def auto_plot(values1, values2):
    labels = ['2bit(Gray)', '2bit', '3bit(Gray)', '3bit', '4bit(Gray)', '4bit', '5bit(Gray)', '5bit', '6bit(Gray)', '6bit', '7bit(Gray)', '7bit', '8bit(Gray)', '8bit']

    if len(values1)!=len(values2):
        raise ValueError("Arrays not equal")
    elif len(values1)!=len(labels):
        raise ValueError("Labels not matching with input for plotting")
    else:

        # Set the width of each bar
        bar_width = 0.35

        # Create a figure and axis object
        fig, ax = plt.subplots()

        # Set the position of the bars on the x-axis
        x_pos = np.arange(len(labels))

        # Create the first bar plot and set the color to blue
        rects1 = ax.bar(x_pos - bar_width / 2, values1, bar_width, color='blue', label='Number of errors')

        # Create the second bar plot and set the color to green
        rects2 = ax.bar(x_pos + bar_width / 2, values2, bar_width, color='green', label='Number of bits generated')

        # Add x-axis and y-axis labels
        ax.set_xlabel('Category of Quantization')
        ax.set_ylabel('Number of Bits')

        # Add a title to the plot
        ax.set_title('Two Bar Plot')

        # Add x-axis ticks and labels
        ax.set_xticks(x_pos)
        ax.set_xticklabels(labels)

        # Add a legend to the plot
        ax.legend()

        # Show the plot
        plt.show()

        percentage_plot(values1, values2)

def percentage_plot(values1, values2):
    labels = ['2bit(Gray)', '2bit', '3bit(Gray)', '3bit', '4bit(Gray)', '4bit', '5bit(Gray)', '5bit', '6bit(Gray)', '6bit', '7bit(Gray)', '7bit', '8bit(Gray)', '8bit']

    percentage_error = [(x * 100 / y) for x, y in zip(values1, values2)]

    # Create a figure and axis object
    fig, ax = plt.subplots()

    # Set the position of the bars on the x-axis
    x_pos = np.arange(len(labels))

    # Create the first bar plot and set the color to blue
    rects1 = ax.bar(x_pos, percentage_error, color='red', label='% error')

    # Add x-axis and y-axis labels
    ax.set_xlabel('Category of Quantization')
    ax.set_ylabel('% error')

    # Add a title to the plot
    ax.set_title('Percentage plot')

    # Add x-axis ticks and labels
    ax.set_xticks(x_pos)
    ax.set_xticklabels(labels)

    # Add a legend to the plot
    ax.legend()

    # Show the plot
    plt.show()

def percentage_plot_axis(values1, values2, labels, axis, c, leg, mark):
    #labels = ['2bit(Gray)', '2bit', '3bit(Gray)', '3bit', '4bit(Gray)', '4bit', '5bit(Gray)', '5bit', '6bit(Gray)',
    #          '6bit', '7bit(Gray)', '7bit', '8bit(Gray)', '8bit', '16bit(Gray)', '16bit', '32bit(Gray)', '32bit', '64bit(Gray)', '64bit']

    percentage_error = [(x * 100 / y) for x, y in zip(values1, values2)]

    # Set the position of the bars on the x-axis
    x_pos = np.arange(len(labels))

    # Create the first bar plot and set the color to blue
    if c=='r':
        col='red'
    elif c=='b':
        col='blue'
    axis.plot(x_pos, percentage_error, linestyle='-', marker=mark, color=c, label=leg)

    # Add x-axis and y-axis labels
    axis.set_xlabel('Order of Quantization', fontsize=40, fontname='Times New Roman')
    axis.set_ylabel('% error', fontsize=40, fontname='Times New Roman')

    # Add a title to the plot
    #axis.set_title('Percentage plot', fontsize=40, fontname='Times New Roman')

    # Add x-axis ticks and labels
    axis.set_xticks(x_pos)
    axis.set_xticklabels(labels)

    # Add a legend to the plot
    axis.legend()


def normal_plot_axis(values1, labels, axis, c, leg, mark):
    #labels = ['2bit(Gray)', '2bit', '3bit(Gray)', '3bit', '4bit(Gray)', '4bit', '5bit(Gray)', '5bit', '6bit(Gray)',
    #          '6bit', '7bit(Gray)', '7bit', '8bit(Gray)', '8bit', '16bit(Gray)', '16bit', '32bit(Gray)', '32bit', '64bit(Gray)', '64bit']

    y=values1

    # Set the position of the bars on the x-axis
    x_pos = np.arange(len(labels))

    # Create the first bar plot and set the color to blue
    if c=='r':
        col='red'
    elif c=='b':
        col='blue'
    axis.plot(x_pos, y, linestyle='-', marker=mark, color=c, label=leg)

    # Add x-axis and y-axis labels
    axis.set_xlabel('Order of Quantization', fontsize=40, fontname='Times New Roman')
    axis.set_ylabel('% error', fontsize=40, fontname='Times New Roman')

    # Add a title to the plot
    #axis.set_title('Percentage plot', fontsize=40, fontname='Times New Roman')

    # Add x-axis ticks and labels
    axis.set_xticks(x_pos)
    axis.set_xticklabels(labels)

    # Add a legend to the plot
    axis.legend()


def plot_pdf_error(array):
    """
    Plot the given array.

    Parameters:
        array (list or numpy array): The input array to be plotted.
    """
    plt.plot(array)
    plt.xlabel('Index position')
    plt.ylabel('Normalised error')
    #plt.title('Plot of Input Array')
    plt.grid(True)
    plt.show()
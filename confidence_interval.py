import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
plt.grid()
plt.rcParams.update({'font.family': 'Times New Roman', 'font.size': 24, })
def calculate_confidence_interval(matrix, value2):
    means = np.mean(matrix, axis=1)
    print("mean", means)
    std_errors = np.std(matrix, axis=1) / np.sqrt(matrix.shape[1])
    print("stad dev", std_errors)
    alph=1-0.95
    critical_value= scipy.stats.norm.ppf(1-alph /2)
    moe=critical_value*(std_errors/np.sqrt(len(means)))
    #confidence_interval = std_errors * scipy.stats.t.ppf((1 + 0.95) / 2., matrix.size-1)
    print("confidence interval",moe)
    #confidence_interval = 1.96 * std_errors  # 95% confidence interval

    upper_bounds = means + moe
    lower_bounds = means - moe

    #print("lower bound", lower_bounds)

    #Enable this for percentage error
    mean = [(x / y) for x, y in zip(means, value2)]
    lower_bound = [(x / y) for x, y in zip(lower_bounds, value2)]
    upper_bound = [(x / y) for x, y in zip(upper_bounds, value2)]

    return mean, lower_bound, upper_bound
    #return means, lower_bounds, upper_bounds

def plot_confidence_interval(matrix, value2, labl, axis, leg, col, mark):

    means, lower_bound, upper_bound = calculate_confidence_interval(matrix, value2)

    #num_rows = len(means)
    x_pos = np.arange(len(labl))


    #plt.figure(figsize=(10, 6))
    axis.plot(x_pos, means, alpha=0.7, label=leg, color=col, linestyle='-', marker=mark)
    axis.fill_between(x_pos, lower_bound, upper_bound, alpha=0.3, color=col)

    # Add x-axis and y-axis labels
    axis.set_xlabel('Order of Quantization', fontsize=24, fontname='Times New Roman')
    axis.set_ylabel('Bit error probability', fontsize=24, fontname='Times New Roman')

    # Add a title to the plot
    #axis.set_title('Percentage plot', fontsize=40, fontname='Times New Roman')

    # Add x-axis ticks and labels
    axis.set_xticks(x_pos)
    axis.set_xticklabels(labl)

    # Add a legend to the plot
    axis.legend()

#Plot Confidence interval and return mean
def mean_of_the_matrix(matrix):

    means, lower_bound, upper_bound = calculate_confidence_interval(matrix)

    return means
def plot_confidence_interval_crrate(matrix, value2, labl, axis, leg, col, mark):

    means, lower_bound, upper_bound = calculate_confidence_interval(matrix, value2)

    #num_rows = len(means)
    x_pos = np.arange(len(labl))


    #plt.figure(figsize=(10, 6))
    axis.plot(x_pos, means, alpha=0.7, label=leg, color=col, linestyle='-', marker=mark)
    axis.fill_between(x_pos, lower_bound, upper_bound, alpha=0.3, color=col)

    # Add x-axis and y-axis labels
    axis.set_xlabel('Order of Quantization', fontname='Times New Roman')
    axis.set_ylabel('Cost function', fontname='Times New Roman')

    # Add a title to the plot
    #axis.set_title('Percentage plot', fontsize=40, fontname='Times New Roman')

    # Add x-axis ticks and labels
    axis.set_xticks(x_pos)
    axis.set_xticklabels(labl)

    # Add a legend to the plot
    axis.legend()

# Example usage:
#matrix = np.random.randn(100, 10)  # Replace this with your actual matrix
#plot_confidence_interval(matrix)

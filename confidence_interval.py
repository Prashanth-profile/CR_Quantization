import numpy as np
import matplotlib.pyplot as plt

def calculate_confidence_interval(matrix):
    means = np.mean(matrix, axis=1)
    std_errors = np.std(matrix, axis=1) / np.sqrt(matrix.shape[1])
    confidence_interval = 1.96 * std_errors  # 95% confidence interval

    upper_bound = means + confidence_interval
    lower_bound = means - confidence_interval

    return means, lower_bound, upper_bound

def plot_confidence_interval(matrix):
    means, lower_bound, upper_bound = calculate_confidence_interval(matrix)

    num_rows = len(means)
    x = np.arange(num_rows)

    plt.figure(figsize=(10, 6))
    plt.plot(x, means, alpha=0.7)
    plt.fill_between(x, lower_bound, upper_bound, alpha=0.3, color='gray')
    plt.xlabel('Row index')
    plt.ylabel('Mean')

    plt.xticks(x)
    plt.grid(axis='y')
    plt.show()

# Example usage:
#matrix = np.random.randn(100, 10)  # Replace this with your actual matrix
#plot_confidence_interval(matrix)

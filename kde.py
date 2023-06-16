import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def seaborn_plot_to_function(data):
    # Create the Seaborn plot
    sns_plot = sns.kdeplot(data)

    # Extract plot data
    x = sns_plot.get_lines()[0].get_data()[0]
    y = sns_plot.get_lines()[0].get_data()[1]

    # Close the Seaborn plot
    plt.close()

    # Define the function
    def function_to_evaluate(x_value):
        # Find the corresponding y value for the given x value
        index = (np.abs(x - x_value)).argmin()
        return y[index]

    return function_to_evaluate

# Generate some random data for demonstration
data = np.random.randn(1000)

# Convert Seaborn plot to a function
kde_func = seaborn_plot_to_function(data)

# Test the function with some values
print(kde_func(-1))
print(kde_func(0))
print(kde_func(1))

import numpy as np
import matplotlib.pyplot as plt

# Input arrays
x1 = np.array([1, 1, 1, 1, 1])
x2 = np.array([1, 4, 7, 10, 11])

def empirical_cdf(x, data):
    return np.sum(data <= x) / len(data)

# Point to evaluate
x = 11
cdf_x1 = empirical_cdf(x, x1)
cdf_x2 = empirical_cdf(x, x2)

print(f"CDF_x1(5) = {cdf_x1}")
print(f"CDF_x2(5) = {cdf_x2}")

# Plotting
plt.figure()

# Sort data for plotting CDFs
for arr, label in [(x1, 'x1'), (x2, 'x2')]:
    sorted_data = np.sort(arr)
    yvals = np.arange(1, len(arr) + 1) / len(arr)
    plt.step(sorted_data, yvals, where='post', label=f'CDF of {label}')

# Mark the CDF values at x = 5
#plt.axvline(x, linestyle='--', color='gray')
#plt.scatter([x, x], [cdf_x1, cdf_x2], color=['blue', 'orange'])
#plt.text(x, cdf_x1, f"{cdf_x1:.2f}", color='blue', va='bottom')
#plt.text(x, cdf_x2, f"{cdf_x2:.2f}", color='orange', va='bottom')

plt.xlabel("x")
plt.ylabel("CDF")
plt.title("Empirical CDFs for x1 and x2")
plt.legend()
plt.grid(True)
plt.show()

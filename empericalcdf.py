import numpy as np
import matplotlib.pyplot as plt

def prefix_sum(arr):
    result = []
    running_total = 0
    for x in arr:
        running_total += x
        result.append(running_total)
    return result

def empirical_cdf(data):
    data = np.sort(data)
    n = len(data)
    #m=max(data)
    #n=4096
    # y values from 1/n to 1
    cdf_y = np.arange(1, n + 1) / n
    print("CDF", cdf_y)
    print("DATA", data)
    return data, cdf_y #x,y

def empirical_cdf_withthreshold(X, thresh):
    X = np.array(X)
    sorted_X = np.sort(X)
    n = len(X)

    def cdf(thresh):
        return np.sum(sorted_X <= thresh) / n

    return cdf, sorted_X

# Example usage:
#data = [4, 2, 1, 7, 3, 3, 9, 6]

#x, y = empirical_cdf(data)

#print("Sorted data:", x)
#print("CDF values:", y)

# Optional: Plot CDF
#plt.step(x, y, where='post')
#plt.xlabel("Value")
#plt.ylabel("CDF")
#plt.title("Empirical CDF")
#plt.grid(True)
#plt.show()

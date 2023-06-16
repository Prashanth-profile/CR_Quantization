import matplotlib.pyplot as plt

def error_distribution(arr1, arr2):
    # Ensure the arrays are of equal length
    if len(arr1) != len(arr2):
        raise ValueError("Arrays must be of equal length which is not in", len(arr1), len(arr2))

    # Initialize variables to store error count and distribution
    num_errors = 0
    error_dist = []

    # Iterate over the elements of the arrays and compare each bit
    for i in range(len(arr1)):
        # XOR the corresponding bytes and count the number of set bits in the result
        xor_result = arr1[i] ^ arr2[i]
        num_bits_not_equal = bin(xor_result).count('1')
        error_dist.append(num_bits_not_equal)

        # Update the error count and distribution
        num_errors += num_bits_not_equal
        '''for j in range(8):
            if (xor_result >> j) & 1:
                #print(xor_result >> j)
                error_dist[i * 8 + j] += 1'''

    return num_errors, error_dist


def plot_error_distribution(error_dist):
    # Compute the cumulative sum of errors
    cum_sum = [sum(error_dist[:i]) for i in range(1, len(error_dist) + 1)]
    total_errors = cum_sum[-1]

    # Convert the cumulative sum to percentages
    cum_perc = [100.0 * cs / total_errors for cs in cum_sum]

    # Plot the cumulative distribution function
    plt.plot(range(1, len(error_dist) + 1), cum_perc)
    plt.xlabel('Bit Position')
    plt.ylabel('Percentage of Errors')
    plt.title('Cumulative Distribution of Errors')
    plt.show()

#arr1 = b'\x51\x52\x53\x54\x52'
#arr2 = b'\x52\x52\x52\x54\x54'

arr1=[7, 5, 12]
arr2=[7, 6, 13]

error, error_dis=error_distribution(arr1, arr2)
print("Number of errors", error, error_dis)
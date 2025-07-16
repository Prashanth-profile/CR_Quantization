import random
import matplotlib.pyplot as plt
import numpy as np

# Set the seed for the Mersenne Twister PRNG
seed = 12345


# Generate the first 256 random numbers with the given seed
def generate_numbers(seed):
    random.seed(seed)  # Set the seed for reproducibility
    return [random.randint(0, 2 ** 32 - 1) for _ in range(256)]


# Generate the first sequence
original_sequence = generate_numbers(seed)


# Function to check if each generated sequence matches the original
def check_and_plot(seed, num_checks=32):
    probabilities = []

    for _ in range(num_checks):
        sequence = generate_numbers(seed)
        if sequence == original_sequence:
            probabilities.append(1)
        else:
            probabilities.append(0)

    return probabilities


# Get the conditional probability distribution
probabilities = check_and_plot(seed)

fontsz=40
#plt3.rcParams.update(plt.rcParamsDefault)
plt.rcParams['text.usetex'] = True
fig3, axis3 = plt.subplots()
plt.rcParams.update({'font.family': 'Times New Roman', 'font.size': fontsz, })
plt.grid()
# Plot the results
plt.figure(figsize=(10, 6))
plt.bar(range(1, 32 + 1), probabilities, color='b', alpha=0.7, label='MT')
plt.xlabel("Sequence Index")
plt.ylabel("Conditional Probability")
plt.title("Conditional Probability Distribution of Sequences (Mersenne Twister, Fixed Seed)")
plt.yticks([0, 1], ['0', '1'])
plt.xticks(range(1, 32 + 1, 2))  # Show every 2nd sequence index for readability
plt.grid(True)
plt.show()

import random
import matplotlib.pyplot as plt
import numpy as np
import math

# Set the seed for the Mersenne Twister PRNG
seed = 12345


# Generate the first 256 random numbers with the given seed
def generate_numbers(seed):
    random.seed(seed)  # Set the seed for reproducibility
    return [random.randint(0, 2 ** 32 - 1) for _ in range(256)]


# Generate the first sequence
original_sequence = generate_numbers(seed)


# Function to check the conditional entropy of the sequence
def calculate_conditional_entropy(seed, num_checks=256):
    probabilities = []

    for _ in range(num_checks):
        sequence = generate_numbers(seed)
        if sequence == original_sequence:
            probabilities.append(1)
        else:
            probabilities.append(0)

    # Calculate the conditional entropy
    p_match = np.mean(probabilities)  # Probability that the sequence matches
    if p_match == 1:
        return 0  # No uncertainty
    else:
        # If there's any uncertainty, compute entropy
        entropy = -p_match * math.log2(p_match) - (1 - p_match) * math.log2(1 - p_match)
        return entropy


# Calculate the conditional entropy
conditional_entropy = calculate_conditional_entropy(seed)

# Print the result
print(f"Conditional Entropy: {conditional_entropy} bits")

# To visualize entropy over checks, we'll create a plot with entropy = 0 throughout
entropy_values = [conditional_entropy] * 256  # Since entropy is 0 for each check

# Plotting the entropy values
plt.figure(figsize=(10, 6))
plt.plot(range(1, 257), entropy_values, 'bo-', label="Mersenne Twister")
plt.xlabel("Sequence Index")
plt.ylabel("Entropy (bits)")
plt.title("Conditional Entropy of Sequences (Mersenne Twister, Fixed Seed)")
plt.yticks([0], ['0'])
plt.xticks(np.arange(0, 257, 50))
plt.grid(True)
plt.legend()
plt.show()

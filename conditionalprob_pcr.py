import random
import numpy as np
import math
import matplotlib.pyplot as plt


# Generate `num_sequences` reference sequences with different seeds
def generate_multiple_sequences(num_sequences=32, sequence_length=256):
    sequences = []
    for seed in range(num_sequences):
        random.seed(seed)  # Use a different seed for each sequence
        sequences.append([random.randint(0, 2 ** 32 - 1) for _ in range(sequence_length)])
    return sequences


# Generate the 32 reference sequences
num_sequences = 32
sequence_length = 256
original_sequences = generate_multiple_sequences(num_sequences, sequence_length)


# Function to calculate the conditional probability of each sequence
def calculate_conditional_probabilities(num_sequences, num_checks, sequence):
    match_counts = np.zeros(num_sequences)  # Track matches per sequence


    for i in range(num_sequences):
        #random.seed(i % num_sequences)  # Cycle through the 32 seeds
        #test_sequence = [random.randint(0, 2 ** 32 - 1) for _ in range(sequence_length)]
        test_sequence=sequence[i]

        # Check which reference sequence matches
        for j in range(num_sequences):
            print("First sequence", test_sequence, "original sequence", original_sequences[j])
            if test_sequence == sequence[j]:
                match_counts[j] += 1

    # Convert counts to probabilities
    probabilities = match_counts / num_sequences
    return probabilities

def calculate_conditional_probabilities_priori(num_sequences, num_checks, eve_sequence, legit_sequence):
    match_counts = np.zeros(num_sequences)  # Track matches per sequence

    test_sequence = eve_sequence
    print("First sequence", test_sequence, "original sequence", legit_sequence)
    for i in range(num_sequences):
        #random.seed(i % num_sequences)  # Cycle through the 32 seeds
        #test_sequence = [random.randint(0, 2 ** 32 - 1) for _ in range(sequence_length)]
        if test_sequence[i] == legit_sequence[i]:
            #print("First sequence", test_sequence[i], "original sequence", legit_sequence[i])
            match_counts[i] += 1

    # Convert counts to probabilities
    probabilities = match_counts
    return probabilities

# Compute conditional entropy
def compute_conditional_entropy(probabilities):
    entropy = -sum(p * math.log2(p) for p in probabilities if p > 0)  # Ignore zero probabilities
    return entropy

'''
# Calculate the conditional probabilities
conditional_probabilities = calculate_conditional_probabilities(num_sequences)

# Print the probabilities
print("Conditional Probabilities of Each Sequence:")
for i, prob in enumerate(conditional_probabilities):
    print(f"Sequence {i + 1}: {prob:.6f}")

# Plot the conditional probabilities
plt.figure(figsize=(10, 6))
plt.bar(range(1, num_sequences + 1), conditional_probabilities, color='b', alpha=0.7)
plt.xlabel("Sequence Index")
plt.ylabel("Conditional Probability")
plt.title("Conditional Probability of 32 Different Sequences (Mersenne Twister, Different Seeds)")
plt.xticks(range(1, num_sequences + 1, 2))  # Show every 2nd sequence index for readability
plt.ylim(0, 1.1)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()'''

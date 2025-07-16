import numpy as np
import timeit

def generate_random_bytes(seed_list):
    results = {}

    for seed in seed_list:
        np.random.seed(seed)  # Set seed
        random_bytes = np.random.randint(0, 256, 256, dtype=np.uint8)  # Generate 256 random bytes
        results[seed] = random_bytes

    return results

def generate_random_bytes_speclen(seed_x, length_of_cr):
    results = {}

    np.random.seed(seed_x)  # Set seed
    random_bytes = np.random.randint(0, 256, length_of_cr, dtype=np.uint8)  # Generate 256 random bytes
    results[seed_x] = random_bytes

    return results







x_cr=[256, 2048, 16384, 131072, 405120]
randomseed=np.random.randint(0, 256, 5, dtype=np.uint8)

for i in range(len(np.array(x_cr))):
    print(i, x_cr[i])
    start_time = timeit.default_timer()
    key=generate_random_bytes_speclen(randomseed[i], x_cr[i])
    end_time = timeit.default_timer()

    print("Execution time", end_time-start_time)
    for seed, data in key.items():
        print(f"Seed: {seed}\nRandom Bytes: {data}\n")
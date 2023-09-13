import numpy as np

def kalman_filter(input_array):
    # Initial parameters
    initial_state = noisy_data[0]
    initial_covariance = 1.0
    process_variance = 0.01
    measurement_variance = 1.0

    filtered_state_estimates = []
    filtered_state_covariances = []

    current_state_estimate = initial_state
    current_covariance = initial_covariance

    for measurement in input_array:
        # Prediction step
        predicted_state = current_state_estimate
        predicted_covariance = current_covariance + process_variance

        # Update step
        kalman_gain = predicted_covariance / (predicted_covariance + measurement_variance)
        current_state_estimate = predicted_state + kalman_gain * (measurement - predicted_state)
        current_covariance = (1 - kalman_gain) * predicted_covariance

        filtered_state_estimates.append(current_state_estimate)
        filtered_state_covariances.append(current_covariance)

    return filtered_state_estimates

# Generate some example noisy data
np.random.seed(0)
true_values = np.linspace(0, 10, num=100)
noisy_data = true_values + np.random.normal(0, 1, size=len(true_values))

# Apply Kalman filter
filtered_estimates = kalman_filter(noisy_data)

print("True Values:", true_values, np.shape(true_values))
print("Noisy Data:", noisy_data, np.shape(noisy_data))
print("Filtered Estimates:", filtered_estimates, np.shape(filtered_estimates))

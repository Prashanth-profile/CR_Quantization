import numpy as np
import matplotlib.pyplot as plt

def kalman_filter_1d(signal, kalman_gain_scaling=1.0):
    A = np.array([[1, 1], [0, 1]])  # State transition matrix
    H = np.array([[1, 0]])          # Measurement matrix
    Q = np.array([[0.001, 0], [0, 0.001]])  # Process noise covariance
    R = np.array([[0.5]])                 # Measurement noise covariance
    x0 = np.array([0, 0])  # Initial position and velocity
    P0 = np.eye(2)         # Initial covariance matrix

    num_steps = len(signal)

    x_hat = np.zeros((2, num_steps))
    P = np.zeros((2, 2, num_steps))
    K = np.zeros((2, 1, num_steps))

    x_hat[:, 0] = x0
    #x_hat[:,0] = np.array(list(range(num_steps)))
    P[:, :, 0] = P0

    # Kalman filter loop
    for k in range(1, num_steps):
        # Prediction step
        x_hat[:, k] = np.dot(A, x_hat[:, k - 1])
        P[:, :, k] = np.dot(np.dot(A, P[:, :, k - 1]), A.T) + Q

        # Update step with scaled Kalman gain
        K[:, :, k] = kalman_gain_scaling * np.dot(np.dot(P[:, :, k], H.T), np.linalg.inv(np.dot(np.dot(H, P[:, :, k]), H.T) + R))
        x_hat[:, k] = x_hat[:, k] + np.dot(K[:, :, k], signal[k] - np.dot(H, x_hat[:, k]))
        P[:, :, k] = np.dot((np.eye(2) - np.dot(K[:, :, k], H)), P[:, :, k])

    # RTS Smoother
    x_smooth = np.zeros((2, num_steps))
    P_smooth = np.zeros((2, 2, num_steps))

    x_smooth[:, -1] = x_hat[:, -1]
    P_smooth[:, :, -1] = P[:, :, -1]

    for k in range(num_steps - 2, -1, -1):
        J = np.dot(np.dot(P[:, :, k], A.T), np.linalg.inv(P[:, :, k + 1]))
        x_smooth[:, k] = x_hat[:, k] + np.dot(J, (x_smooth[:, k + 1] - np.dot(A, x_hat[:, k])))
        P_smooth[:, :, k] = P[:, :, k] + np.dot(np.dot(J, (P_smooth[:, :, k + 1] - P[:, :, k + 1])), J.T)

    return x_smooth[0, :]

# Example with a 2048-sample signal
signal_2048_samples = np.random.randn(2048)  # Replace this with your own signal

# Apply Kalman filter and RTS smoother to the noisy signal
filtered_signal_rts = kalman_filter_1d(signal_2048_samples)

# Plotting results
plt.figure(figsize=(10, 6))

plt.plot(signal_2048_samples, label='Noisy Signal', linestyle='--', marker='x')
plt.plot(filtered_signal_rts, label='Filtered Signal with RTS Smoother', linestyle='-', marker='s')

plt.title('Kalman Filter with RTS Smoother - 1D Signal Filtering')
plt.xlabel('Time Steps')
plt.ylabel('Signal')
plt.legend()
plt.grid(True)
plt.show()

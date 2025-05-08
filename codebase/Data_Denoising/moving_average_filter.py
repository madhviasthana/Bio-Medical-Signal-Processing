from libaries import *
from global_parameters import *
from peak_to_peak_detection import *


# Uniform Moving Average
def apply_uniform_moving_average_filter(data, trial_idx=0, window_size=5):
    """
    Computes y(n) as the average of window_size samples centered around x(n).

    Args:
        data (np.ndarray): Input data of shape [100, 2, 16000].
        trial_idx (int): Index of the trial to process (default: 0).
        window_size (int): Number of samples in the moving average window (default: 5, must be odd).

    Returns:
        np.ndarray: Filtered data for channel 2 of the specified trial, shape [1, 16000].
    """
    # Validate inputs
    if trial_idx < 0 or trial_idx >= data.shape[0]:
        raise ValueError(f"Trial index {trial_idx} out of bounds for data with {data.shape[0]} trials.")
    if window_size < 1:
        raise ValueError("Window size must be positive.")
    if window_size % 2 == 0:
        window_size += 1  # Ensure it's odd

    # Extract channel 2 signal
    signal = data[trial_idx, 1, :]

    # Create uniform kernel and apply convolution
    kernel = np.ones(window_size) / window_size
    filtered_signal = convolve(signal, kernel, mode='same')

    return filtered_signal.reshape(1, -1)


#--------------------------------------------------------

# hanning filter (hann filter or integer filter or triangular filter)


def apply_hanning_filter(data, trial_idx=0, use_initial_conditions=False):
    """
    Applies Hanning filter: y(n) = 0.25*x(n) + 0.5*x(n-1) + 0.25*x(n-2)

    Args:
        data (np.ndarray): Input data of shape [100, 2, 16000].
        trial_idx (int): Index of the trial to process (default: 0).
        use_initial_conditions (bool): If True, use initial conditions to reduce edge transients (default: False).

    Returns:
        np.ndarray: Filtered signal for channel 2 of specified trial, shape [1, 16000].
    """
    # Validate inputs
    if trial_idx < 0 or trial_idx >= data.shape[0]:
        raise ValueError(f"Trial index {trial_idx} out of bounds for data with {data.shape[0]} trials.")

    # Extract signal
    signal = data[trial_idx, 1, :]

    # Hanning filter coefficients (FIR)
    b = [0.25, 0.5, 0.25]  # Numerator (filter weights)
    a = [1]                # Denominator (no feedback)

    # Apply FIR filter
    if use_initial_conditions:
        zi = lfilter_zi(b, a) * signal[0]  # Initial conditions based on first sample
        filtered_signal, _ = lfilter(b, a, signal, zi=zi)
    else:
        filtered_signal = lfilter(b, a, signal)

    return filtered_signal.reshape(1, -1)

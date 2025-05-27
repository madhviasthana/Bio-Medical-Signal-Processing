from libaries import *
from global_parameters import *
from peak_to_peak_detection import *


def moving_average_integrator(signal, window_size=30):
    # Zero-padding before the signal (to replicate MATLAB logic)
    padded = np.concatenate((np.zeros(window_size - 1), signal))

    # Moving average
    integrated = np.convolve(padded, np.ones(window_size)/window_size, mode='valid')

    # Normalize
    normalized_integrated = integrated / np.max(np.abs(integrated))
    return normalized_integrated

def apply_uniform_moving_average_filter(data, window_size=5):

    if data.ndim != 2:
        raise ValueError("Input data must be of shape (n_trials, n_samples)")
    
    if window_size < 1:
        raise ValueError("Window size must be positive.")
    if window_size % 2 == 0:
        window_size += 1  # Ensure odd window size

    kernel = np.ones(window_size) / window_size
    filtered_all = []

    for i in range(data.shape[0]):
        filtered = convolve(data[i], kernel, mode='same')
        filtered_all.append(filtered)

    return np.stack(filtered_all, axis=0)  # shape: (n_trials, n_samples)


#--------------------------------------------------------

# hanning filter (hann filter or integer filter or triangular filter)



def batch_apply_hanning_filter(data, use_initial_conditions=False):
    """
    Applies a Hanning filter to all trials in a 2D signal array.

    Hanning filter: y(n) = 0.25*x(n) + 0.5*x(n-1) + 0.25*x(n-2)

    Args:
        data (np.ndarray): Input signal of shape (n_trials, n_samples)
        use_initial_conditions (bool): Use initial conditions to reduce edge artifacts

    Returns:
        np.ndarray: Filtered data of shape (n_trials, n_samples)
    """
    if data.ndim != 2:
        raise ValueError("Expected input shape (n_trials, n_samples)")

    b = [0.25, 0.5, 0.25]
    a = [1]

    filtered_all = []

    for i in range(data.shape[0]):
        signal = data[i]

        if use_initial_conditions:
            zi = lfilter_zi(b, a) * signal[0]
            filtered_signal, _ = lfilter(b, a, signal, zi=zi)
        else:
            filtered_signal = lfilter(b, a, signal)

        filtered_all.append(filtered_signal)

    return np.stack(filtered_all, axis=0)  # shape: (n_trials, n_samples)

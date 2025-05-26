from libaries import *
from global_parameters import *
from peak_to_peak_detection import *

def apply_improved_derivative_filter(data, T=1.0):
    """
    Applies the improved derivative filter y(n) = (x(n) - x(n-2)) / (2T)
    to each trial in a 2D signal array (100, 16000).
    """
    if data.ndim != 2:
        raise ValueError("Expected input shape (n_trials, n_samples)")

    # Create output array
    filtered = np.zeros_like(data)

    # Apply vectorized filter across all trials
    filtered[:, 2:] = (data[:, 2:] - data[:, :-2]) / (2 * T)

    return filtered

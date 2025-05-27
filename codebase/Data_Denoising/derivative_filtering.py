from libaries import *
from global_parameters import *
from peak_to_peak_detection import *

def apply_improved_derivative_filter(data, T=1.0):
    """
    Applies the improved derivative filter: y(n) = (x(n) - x(n-2)) / (2T)

    Works for:
    - 1D signal: shape (n_samples,)
    - 2D signal: shape (n_trials, n_samples)

    Parameters:
    - data: numpy array of shape (n_samples,) or (n_trials, n_samples)
    - T: sampling interval (default = 1.0)

    Returns:
    - filtered signal of same shape as input
    """
    if data.ndim == 1:
        filtered = np.zeros_like(data)
        filtered[2:] = (data[2:] - data[:-2]) / (2 * T)
        return filtered

    elif data.ndim == 2:
        filtered = np.zeros_like(data)
        filtered[:, 2:] = (data[:, 2:] - data[:, :-2]) / (2 * T)
        return filtered

    else:
        raise ValueError("Expected input to be 1D or 2D (n_samples,) or (n_trials, n_samples)")

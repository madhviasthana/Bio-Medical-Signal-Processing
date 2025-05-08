from libaries import *
from global_parameters import *
from peak_to_peak_detection import *

def apply_improved_derivative_filter(data, channel=1, T=1.0):
    """
    Apply improved derivative filter to a specific channel of the data while preserving the original shape.
    
    Parameters:
    - data: numpy array of shape [100, 2, 16000] (trials, channels, samples)
    - channel: int, channel to process (default 1 for channel 2)
    - T: float, sampling period (default 1.0)
    
    Returns:
    - filtered_data: numpy array of shape [100, 2, 16000] with the specified channel filtered
    """
    # Create a copy of the input data to store the filtered result
    filtered_data = data.copy()
    
    # Extract the specified channel (all trials)
    channel_data = data[:, channel, :]  # Shape: [100, 16000]
    
    # Apply the filter: y_3(n) = (1/(2T)) * (x(n) - x(n-2))
    for trial in range(channel_data.shape[0]):
        for n in range(2, channel_data.shape[1]):
            filtered_data[trial, channel, n] = (1 / (2 * T)) * (channel_data[trial, n] - channel_data[trial, n - 2])
    
    return filtered_data
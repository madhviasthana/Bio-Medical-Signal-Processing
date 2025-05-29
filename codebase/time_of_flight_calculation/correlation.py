from utils.libaries import *
from utils.data_loading import findFiles,LoadDataSignals
from utils.global_parameters import *


def calculate_tof_cross_correlation(transmit_signal, receive_signal, fs=125e6):
    """
    Estimate Time-of-Flight (ToF) using cross-correlation between transmit and receive signals.

    Parameters:
    - transmit_signal (np.array): Transmitted signal (1D)
    - receive_signal (np.array): Received signal (1D)
    - fs (float): Sampling frequency in Hz (default=1.0)

    Returns:
    - tof (float): Estimated time-of-flight in seconds
    - sample_delay (int): Delay in number of samples
    - correlation (np.array): Cross-correlation array (for optional plotting)
    """

    # Step 1: Normalize both signals to zero mean and unit variance
    transmit_norm = (transmit_signal - np.mean(transmit_signal)) / np.std(transmit_signal)
    receive_norm  = (receive_signal - np.mean(receive_signal)) / np.std(receive_signal)

    # Step 2: Compute full cross-correlation (lag from -N to +N)
    correlation = correlate(receive_norm, transmit_norm, mode='full')

    # Step 3: Find the lag corresponding to the peak of the correlation
    max_corr_index = np.argmax(correlation)
    sample_delay = max_corr_index - len(transmit_signal) + 1

    # Step 4: Convert lag to time (in seconds)
    tof = sample_delay / fs if fs != 1.0 else sample_delay

    receive_start_index=6000
    adjusted_sample_delay = sample_delay + receive_start_index  # e.g., 6000
    tof = adjusted_sample_delay / fs


    return tof, adjusted_sample_delay, correlation

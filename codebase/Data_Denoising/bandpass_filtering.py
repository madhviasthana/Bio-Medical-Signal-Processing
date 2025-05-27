from libaries import *
from global_parameters import *

def apply_bandpass_filter(signal, fs, low_cutoff, high_cutoff, order=4):
    """
    Applies a Butterworth bandpass filter to a 1D signal.

    Parameters:
    - signal (1D array): The input signal (e.g., receive[0, start:end])
    - fs (float): Sampling frequency in Hz (e.g., 125e6)
    - low_cutoff (float): Low cutoff frequency in Hz (e.g., 4e6)
    - high_cutoff (float): High cutoff frequency in Hz (e.g., 6e6)
    - order (int): Filter order (default is 4)

    Returns:
    - filtered_signal (1D array): Bandpassed signal
    """
    nyquist = fs / 2
    low = low_cutoff / nyquist
    high = high_cutoff / nyquist
    b, a = butter(order, [low, high], btype='band')
    filtered_signal = filtfilt(b, a, signal)
    return filtered_signal

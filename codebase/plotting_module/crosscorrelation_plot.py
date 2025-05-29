from utils.libaries import *
from utils.data_loading import findFiles,LoadDataSignals
from utils.global_parameters import *

def plot_windowed_cross_correlation(correlation, lags, tof_ns):
    plt.figure(figsize=(12, 5))
    plt.plot(lags, correlation, color='purple')
    plt.axvline(x=lags[np.argmax(correlation)], color='red', linestyle='--',
                label=f"ToF ≈ {tof_ns:.2f} ns")
    plt.title("Windowed Cross-Correlation")
    plt.xlabel("Lag (samples)")
    plt.ylabel("Correlation")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_cross_correlation(transmit_signal, receive_signal, correlation, sample_delay, fs, concen, actual_waveform,receive_trim_offset=6000, receive_start_index=6000):
    """
    Compute ToF using cross-correlation with correct time labeling.
    """
    # Normalize both signals
    transmit_norm = (transmit_signal - np.mean(transmit_signal)) / np.std(transmit_signal)
    receive_norm = (receive_signal - np.mean(receive_signal)) / np.std(receive_signal)



    # Full cross-correlation
    correlation = correlate(receive_norm, transmit_norm, mode='full')

    # Lags (negative to positive sample delays)
    lags = np.arange(-len(transmit_signal)+1, len(receive_signal))

    # Find the peak correlation lag (in samples)
    max_corr_index = np.argmax(correlation)
    sample_delay = lags[max_corr_index]

    # ✅ Correct for trimming
    adjusted_sample_delay = sample_delay + receive_trim_offset
    tof_ns = adjusted_sample_delay / fs * 1e9  # convert to nanoseconds



    # Time axis for plotting
    time_axis_ns = lags

    # Plot
    plt.figure(figsize=(14, 6))
    plt.plot(time_axis_ns, correlation, color='purple', linewidth=1.5)
    plt.axvline(tof_ns, color='red', linestyle='--', label=f"Estimated ToF = {tof_ns:.2f} ns")
    plt.title("Cross-Correlation for ToF Estimation")
    plt.xlabel("Time Lag (ns)")
    plt.ylabel("Correlation Amplitude")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    return tof_ns, sample_delay, correlation


import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import correlate

def calculate_windowed_tof_cross_correlation(transmit_signal, receive_signal,
                                              t_start_idx, r_start_idx,
                                              fs=125e6, window_size=500):
    """
    Estimate ToF using windowed cross-correlation around known transmit and receive echo start indices.

    Parameters:
        transmit_signal (1D np.array): The transmit channel signal.
        receive_signal (1D np.array): The receive channel signal.
        t_start_idx (int): Start index of the main transmit echo.
        r_start_idx (int): Start index of the main receive echo.
        fs (float): Sampling frequency in Hz. Default is 125 MHz.
        window_size (int): Number of samples around the echo to consider for correlation.

    Returns:
        tof_ns (float): Estimated ToF in nanoseconds.
        sample_delay (int): Estimated ToF in samples.
        correlation (np.array): Correlation output (optional for plotting).
    """

    # Define correlation windows
    tx_window = transmit_signal[t_start_idx : t_start_idx + window_size]
    rx_window = receive_signal[r_start_idx : r_start_idx + window_size]

    # Normalize signals
    tx_norm = (tx_window - np.mean(tx_window)) / np.std(tx_window)
    rx_norm = (rx_window - np.mean(rx_window)) / np.std(rx_window)

    # Cross-correlation
    correlation = correlate(rx_norm, tx_norm, mode='full')
    lags = np.arange(-len(tx_norm)+1, len(rx_norm))

    # Find peak in correlation
    max_corr_idx = np.argmax(correlation)
    lag_at_max = lags[max_corr_idx]

    # Calculate actual ToF in samples and ns
    sample_delay = lag_at_max + (r_start_idx - t_start_idx)
    tof_ns = sample_delay 




    return tof_ns, sample_delay, correlation, lags



import numpy as np
from scipy.fft import fft, ifft
from scipy.signal import welch

def apply_psd_based_wiener_filter(signal, noise_region, fs=125_000_000, lambda_value=0.1):
    """
    Applies the Wiener filter using the formulation:
        A(w, λ) = F(w) / (1 + λ * S_n(w))
    where:
        - F(w) is the FFT of the noisy signal
        - S_n(w) is the power spectral density (PSD) of the noise
        - λ is a scalar controlling suppression strength

    Parameters:
        signal (np.ndarray): The full signal (e.g., averaged signal), shape (N,)
        noise_region (np.ndarray): Region from the signal assumed to be noise only
        fs (int): Sampling frequency in Hz
        lambda_value (float): Suppression strength scalar (λ)

    Returns:
        np.ndarray: Filtered signal (same length as input)
    """
    N = len(signal)

    # Step 1: FFT of the signal
    signal_fft = fft(signal)

    # Step 2: Estimate noise PSD using Welch’s method
    f_noise, psd_noise = welch(noise_region, fs=fs, nperseg=512)

    # Step 3: Prepare for frequency domain filtering
    # Interpolate noise PSD to match full FFT length
    freq_full = np.fft.fftfreq(N, d=1/fs)
    psd_noise_interp = np.interp(np.abs(freq_full), f_noise, psd_noise)

    # Step 4: Apply Wiener filtering
    H_wiener = 1 / (1 + lambda_value * psd_noise_interp)
    filtered_fft = signal_fft * H_wiener
    filtered_signal = ifft(filtered_fft).real

    return filtered_signal


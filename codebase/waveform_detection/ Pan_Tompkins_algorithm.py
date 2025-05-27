from libaries import *
from data_loading import findFiles,LoadDataSignals
from global_parameters import *
from peak_to_peak_detection import *
from Data_Denoising.data_denoising import *
from Data_Denoising.time_synchronization import *
from Data_Denoising.moving_average_filter import *
from Data_Denoising.derivative_filtering import apply_improved_derivative_filter
from Data_Denoising.dc_offset_removal import *
from plotting_module.signal_plot import *
from Data_Denoising.bandpass_filtering import *
from detect_waveform import *

def normalize_min_max(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))


def apply_pan_tompkins(transmit,recieve,T,low_cutoff, high_cutoff, order=4, window_size=11):

    bandpass_recieve= apply_bandpass_filter(signal, fs=fs, low_cutoff=low_cutoff, high_cutoff=high_cutoff, order=order)
    signal_plot(bandpass_recieve[:],start=0,end=len(bandpass_recieve),title="Recieve Channel: Band Pass Filtering")

    echo_derivative_filtered_data=apply_improved_derivative_filter(bandpass_recieve,T=T)
    signal_plot(echo_derivative_filtered_data[:],start=0,end=16000,title="Recieve Channel:Derivative Filtering")
    normalized_echo = normalize_min_max(echo_derivative_filtered_data)
    signal_plot(normalized_echo[:],start=0,end=16000,title="Recieve Channel: Normalized Derivative Filtering")

    squared_output = normalized_echo ** 2
    signal_plot(squared_output[:],start=0,end=16000,title="Recieve Channel:Squared")
    normalized_squared_output = squared_output / np.max(np.abs(squared_output))
    signal_plot(normalized_squared_output[:],start=0,end=16000,title="Recieve Channel:Squared Normalized")

    integrated_output = moving_average_integrator(normalized_squared_output, window_size)
    signal_plot(integrated_output[:],start=0,end=16000,title="Recieve Channel:Integrated Moving Average")



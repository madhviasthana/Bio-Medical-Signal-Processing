from utils.libaries import *
from utils.data_loading import findFiles,LoadDataSignals
from utils.global_parameters import *
from time_of_flight_calculation.peak_to_peak_detection import *
from Data_Denoising.data_denoising import *
from Data_Denoising.time_synchronization import *
from Data_Denoising.moving_average_filter import *
from Data_Denoising.derivative_filtering import apply_improved_derivative_filter
from Data_Denoising.dc_offset_removal import *
from plotting_module.signal_plot import *
from Data_Denoising.bandpass_filtering import *
from waveform_detection.detect_waveform import *

def normalize_min_max(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))

def find_min_max_echo_list(signal, buffer_size , min_prominence , start_threshold, end_threshold):
    """_summary_

    Args:
        signal (_type_): _description_
        buffer_size (_type_): _description_
        min_prominence (_type_): _description_
        start_threshold (_type_): this is the min max diff value which atleast be larger than the threshold
        end_threshold (_type_): this is min max diff value atleast smaller than certain value which we can consider the echo has ended

    Returns:
        _type_: _description_
    """
    min_max_pairs = find_minima_maxima_pairs(signal,min_prominence) 

    # Calculate difference
    pair_diff=calculate_value_differences(signal, min_max_pairs)

    echo_list=minmax_echolist(signal,pair_diff,buffer_size, start_threshold, end_threshold)

    return echo_list,min_max_pairs

def apply_pan_algorithm(transmit,recieve,periods,T,low_cutoff, high_cutoff, order=4, window_size=11,min_prominence=500,threshold_transmit=600000,threshold_recieve=1500000,comp_index=3,buffer_size=100):
    transmit_part = []
    receive_part = []
    #signal_plot(transmit[:],start=0,end=len(recieve),title="Transmit Channel: Raw Signal")
    #signal_plot(recieve[:],start=0,end=len(recieve),title="Recieve Channel: Raw Signal")

    # Filtering steps
    bandpass_recieve= apply_bandpass_filter(recieve, fs=fs, low_cutoff=low_cutoff, high_cutoff=high_cutoff, order=order)
    #signal_plot(bandpass_recieve[:],start=0,end=len(bandpass_recieve),title="Recieve Channel: Band Pass Filtering")

    echo_derivative_filtered_data=apply_improved_derivative_filter(bandpass_recieve,T=T)
    #signal_plot(echo_derivative_filtered_data[:],start=0,end=16000,title="Recieve Channel:Derivative Filtering")
    normalized_echo = normalize_min_max(echo_derivative_filtered_data)
    #signal_plot(normalized_echo[:],start=0,end=16000,title="Recieve Channel: Normalized Derivative Filtering")

    squared_output = normalized_echo ** 2
    #signal_plot(squared_output[:],start=0,end=16000,title="Recieve Channel:Squared")


    integrated_output = moving_average_integrator(squared_output, window_size)
    #signal_plot(integrated_output[:],start=0,end=16000,title="Recieve Channel:Integrated Moving Average")

    # wave detection begins here by keeping a threshold
    
    normalized_transmit = normalize_min_max(transmit)

    signal_plot(normalized_transmit,start=0,end=240,title="Transmit Channel")
    signal_plot(integrated_output,start=0,end=8000,title="Recieve Channel")
    signal_plot(integrated_output,start=6000,end=12000,title="Recieve Channel")
    
    signal_plot(integrated_output,start=6271-100,end=6342+100,title="Recieve Channel")

    transmit_echo_list,transmit_min_max_pairs = find_min_max_echo_list(signal=normalized_transmit ,buffer_size=100 ,min_prominence= 0.05, start_threshold=0.5 , end_threshold=0.2)

    recieve_echo_list,recieve_min_max_pairs = find_min_max_echo_list(signal=integrated_output[4000:] ,buffer_size= 100 ,min_prominence= 0.05, start_threshold= 0.01 , end_threshold= 0.005)
    recieve_echo_list = [(i+4000, j+4000) for (i,j) in recieve_echo_list]
    print("Transmit" , transmit_echo_list)
    print("Recieve" , recieve_echo_list)
    

    return transmit_echo_list,recieve_echo_list,transmit_min_max_pairs,recieve_min_max_pairs











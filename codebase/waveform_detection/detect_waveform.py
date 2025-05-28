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


def find_minima_maxima_pairs(signal, min_prominence=500):
    """
    Find minima and maxima pairs in the signal with a prominence filter.
    """
    pairs = []
    n = len(signal)
    i = 0

    while i < n - 1:
        # Check for maxima
        if signal[i] < signal[i + 1]:
            start = i
            while i < n - 1 and signal[i] <= signal[i + 1]:
                i += 1
            end = i
            # Apply prominence filter
            if abs(signal[end] - signal[start]) >= min_prominence:
                pairs.append((start, end))
        # Check for minima
        elif signal[i] > signal[i + 1]:
            start = i
            while i < n - 1 and signal[i] >= signal[i + 1]:
                i += 1
            end = i
            # Apply prominence filter
            if abs(signal[end] - signal[start]) >= min_prominence:
                pairs.append((start, end))
        else:
            i += 1  # Skip if the signal is flat

    return pairs


def find_MinMaxDict(raw_signal,transmit_part,receive_part):
    max_min_dict = {"transmit" : { "max_list" : [] , "min_list" : []}, "receive" : { "max_list" : [] , "min_list" : []}}

    for pair in transmit_part: # subdivide transmit part extrema in maxima and minima
        if raw_signal[pair[0]] > 0 :
            max_min_dict["transmit"]["max_list"].append((pair[0], int(raw_signal[pair[0]])))
            max_min_dict["transmit"]["min_list"].append((pair[1], int(raw_signal[pair[1]])))
        else:
            max_min_dict["transmit"]["max_list"].append((pair[1], int(raw_signal[pair[1]])))
            max_min_dict["transmit"]["min_list"].append((pair[0], int(raw_signal[pair[0]])))
    for pair in receive_part: # subdivide receive part extrema in maxima and minima
        if raw_signal[pair[0]] > 0 :
            max_min_dict["receive"]["max_list"].append((pair[0], int(raw_signal[pair[0]])))
            max_min_dict["receive"]["min_list"].append((pair[1], int(raw_signal[pair[1]])))
        else:
            max_min_dict["receive"]["max_list"].append((pair[1], int(raw_signal[pair[1]])))
            max_min_dict["receive"]["min_list"].append((pair[0], int(raw_signal[pair[0]])))
    return max_min_dict


def calculate_value_differences(signal, pairs):
    '''Once we found the pairs of maxima and minima we can find the difference between those points, parameters (pairs) 
    are found from minima maxima pairs function'''
    differences = []
    for  (start, end) in pairs:
        # Calculate the difference between the end and start values
        difference = signal[end] - signal[start]
        differences.append(((start, end), abs(difference)))
    return differences


def minmax_echolist(signal,min_max_dif,buffer_size, start_threshold, end_threshold):
    
    echo_list = []
    echo_start = None
    echo_end = None
    temp_end = None
    consecutive_count=0

 # Calculate dynamic thresholds
    dynamic_start_threshold = start_threshold# np.mean(signal) + 2 * np.std(signal)  
    dynamic_end_threshold = end_threshold# np.mean(signal) + 0.5 * np.std(signal)  

    print(f"Dynamic Start Threshold: {dynamic_start_threshold}")
    print(f"Dynamic End Threshold: {dynamic_end_threshold}")
    
    for  (start_i,end_i), diff in min_max_dif : 
        # in this we are finding the echo start by comparing difference of min and maxima it to start threshold
        if echo_start is None and diff > dynamic_start_threshold :
            echo_start = start_i 
            continue

        if echo_start is not None:
            if diff <  dynamic_end_threshold:
                if temp_end is not None:
                    consecutive_count = abs(temp_end-end_i)
                else:
                    temp_end = end_i
            else:
                consecutive_count = 0  # Reset counter if condition is not met
                temp_end = None
            # If buffer_size consecutive values satisfy the condition, end the segment
            if consecutive_count >= buffer_size:
                echo_list.append((echo_start, temp_end))
                echo_start = None
                consecutive_count = 0
    if echo_start is not None and temp_end is None:
        echo_list.append((echo_start, min_max_dif[-1][0][1]))
                
    return echo_list


 
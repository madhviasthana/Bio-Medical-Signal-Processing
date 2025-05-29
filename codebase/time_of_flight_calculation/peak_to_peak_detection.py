from utils.libaries import *
from utils.data_loading import findFiles,LoadDataSignals
from utils.global_parameters import *
# Find the echo starting points

def get_echo_start_points(receive_signal):
    # Compute the first derivative (difference between consecutive values)
    print(receive_signal)
    diff_signal = np.diff(receive_signal)
    diff_threshold = 10000
    # Find all indices where the value increases (i.e., difference is positive and grater than threshold)
    increasing_indices = np.where(diff_signal > diff_threshold)[0]   # +1 to shift to original signal index

    # Find the first occurrence in each increasing segment
    valid_indices = []
    for i in range(len(increasing_indices) - 1):
        if i == 0 or increasing_indices[i] != increasing_indices[i - 1] + 1:
            valid_indices.append(increasing_indices[i])

    print("Indices where the signal starts increasing:", valid_indices)
    return valid_indices

#-----------------------------------------------------

# Find minima and maxima points 

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

#-----------------------------------------------------


def find_MinMaxDict(raw_signal,transmit_part,recieve_part):
    max_min_dict = {"transmit" : { "max_list" : [] , "min_list" : []}, "recieve" : { "max_list" : [] , "min_list" : []}}

    for pair in transmit_part:
        if raw_signal[pair[0]] > 0 :
            max_min_dict["transmit"]["max_list"].append((pair[0], int(raw_signal[pair[0]])))
            max_min_dict["transmit"]["min_list"].append((pair[1], int(raw_signal[pair[1]])))
        else:
            max_min_dict["transmit"]["max_list"].append((pair[1], int(raw_signal[pair[1]])))
            max_min_dict["transmit"]["min_list"].append((pair[0], int(raw_signal[pair[0]])))
    for pair in recieve_part:
        if raw_signal[pair[0]] > 0 :
            max_min_dict["recieve"]["max_list"].append((pair[0], int(raw_signal[pair[0]])))
            max_min_dict["recieve"]["min_list"].append((pair[1], int(raw_signal[pair[1]])))
        else:
            max_min_dict["recieve"]["max_list"].append((pair[1], int(raw_signal[pair[1]])))
            max_min_dict["recieve"]["min_list"].append((pair[0], int(raw_signal[pair[0]])))
    return max_min_dict

#-----------------------------------------------------



def find_transmit_and_receive_max_points(raw,periods,min_prominence=1500000,time_axis_start=0,time_axis_end=16000):
    transmit_selected_index_list=[] #peak to peak calc
    receive_selected_index_list=[] #peak to peak calc    
    transmit_part = []
    recieve_part = []
    raw_transmit_signal=raw[0,0,time_axis_start:time_axis_end]
    raw_receive_signal=raw[0,1,time_axis_start:time_axis_end]

    raw_signal=raw_receive_signal
    min_max_pairs = find_minima_maxima_pairs(raw_signal, min_prominence)

    for i in min_max_pairs[::2]:
        if i[0] < 5000:
            transmit_part.append(i)
        else:
            recieve_part.append(i)
    max_min_dict=find_MinMaxDict(raw_signal,transmit_part,recieve_part)

    transmit_max = max_min_dict['transmit']["max_list"][:periods]
    recieve_max = max_min_dict['recieve']["max_list"][:periods]

    return transmit_max,recieve_max



def find_start_index(signal_values, threshold=500000):
    """
    Finds the indices where the signal crosses above a given threshold.

    Parameters:
    - signal_values (list or iterable of float): The signal data.
    - threshold (float): The threshold value to detect crossings.

    Returns:
    - List[int]: Indices where signal crosses from below to above the threshold.
    """
    crossings = []

    for i in range(1, len(signal_values)):
        if signal_values[i-1] <= threshold < signal_values[i]:
            crossings.append(i-1)
    return crossings

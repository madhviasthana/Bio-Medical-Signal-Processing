from libaries import *
from global_parameters import *
from peak_to_peak_detection import *



def find_reference_points_transmit_start(transmit,recieve, threshold):
    """
    Find reference points for transmit start in the signal. If transmit start doesn't exist or the
    transmit signal is invalid, it won't be considered a valid experiment.

    Parameters:
        raw (np.ndarray): The dataset of shape [100, 2, 16000].
        threshold (int): The threshold value to determine the start of the transmit signal.

    Returns:
        list: List of reference points for each experiment (or 0 if invalid).
    """
    reference_points = []
    
    for i in range(transmit.shape[0]):
        transmit_signal=transmit[i,:]
        # Find the start index of the transmit signal
        transmit_start = find_start_index(transmit_signal, threshold)
        # If a valid transmit start is found, append it, otherwise append 0
        if transmit_start:
            reference_points.append(transmit_start[0])
        else:
            reference_points.append(0)
        
    
    # Remove experiments where the reference point is 0 (invalid)
    valid_experiments = [i for i, point in enumerate(reference_points) if point != 0]
    
    
    return valid_experiments, reference_points

#----------------------------



"""def find_reference_points_transmit_max(raw,periods,time_axis_start=0,time_axis_end=16000):
    reference_points=[]
    for i in range(raw.shape[0]):
        transmit_max,recieve_max=find_transmit_and_receive_max_points(raw,periods)
        transmit_max=transmit_max[0][0]
        reference_points.append(transmit_max)

    return reference_points

#----------------------------


def find_reference_points_transmit_start(raw,threshold=500000):
    reference_points=[]
    for i in range(raw.shape[0]):
        transmit_signal=raw[i,1,:]
        transmit_start=find_start_index(transmit_signal,threshold)
        if transmit_start:
            reference_points.append(transmit_start[0])
        else : 
            reference_points.append(0)

    return reference_points 

    """

#----------------------------

def get_align_signals(transmit_filtered_raw, recieve_filtered_raw, reference_points):
    max_start_value = max(reference_points)
    transmit_aligned_signal_list = []
    recieve_aligned_signal_list = []
    
    for i in range(transmit_filtered_raw.shape[0]):
        # Process the i-th experiment
        difference = max_start_value - reference_points[i]
        # Pad the i-th signal
        padded_transmit = np.pad(transmit_filtered_raw[i], (difference, 0), mode='constant', constant_values=0)
        # Trim to ensure length of 16000
        padded_transmit = padded_transmit[:16000]
        transmit_aligned_signal_list.append(padded_transmit)

        padded_receive = np.pad(recieve_filtered_raw[i], (difference, 0), mode='constant', constant_values=0)
        padded_receive = padded_receive[:16000]
        recieve_aligned_signal_list.append(padded_receive)
    
    # Convert lists to NumPy arrays
    return np.array(transmit_aligned_signal_list), np.array(recieve_aligned_signal_list)

#----------------------------

def synchronized_averaging(transmit,recieve,threshold=500000):
    #reference_points= find_reference_points_transmit_start(raw,threshold)
    valid_experiments, reference_points = find_reference_points_transmit_start(transmit,recieve, threshold=500000)

    # Filter only valid samples
    transmit_valid = transmit[valid_experiments]
    recieve_valid  = recieve[valid_experiments]

    print("Transmit Valid signals after filtering:", transmit_valid.shape)
    print("Recieve Valid signals after filtering:", recieve_valid.shape)


    tx_aligned, rx_aligned = get_align_signals(transmit_valid, recieve_valid, reference_points)

    tx_avg = np.mean(tx_aligned, axis=0, keepdims=True)
    rx_avg = np.mean(rx_aligned, axis=0, keepdims=True)

    return tx_avg, rx_avg
    

from libaries import *
from global_parameters import *
from peak_to_peak_detection import *



def find_reference_points_transmit_start(raw, threshold=500000):
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
    
    for i in range(raw.shape[0]):
        transmit_signal = raw[i, 1, :]
        
        # Find the start index of the transmit signal
        transmit_start = find_start_index(transmit_signal, threshold)
        
        # If a valid transmit start is found, append it, otherwise append 0
        if transmit_start:
            reference_points.append(transmit_start[0])
        else:
            reference_points.append(0)
    
    # Remove experiments where the reference point is 0 (invalid)
    valid_experiments = [i for i, point in enumerate(reference_points) if point != 0]
    
    # Filter raw data based on valid experiments
    filtered_raw = raw[valid_experiments]
    
    return filtered_raw, reference_points

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

def get_align_signals(raw,reference_points):
    max_start_value=max(reference_points)
    alligned_signal_list = []
    for i in range(raw.shape[0]):
        difference=max_start_value-reference_points[i]
        raw_signal=raw[i,1,:] #for now data is in channel 2 only
        padded_signal = np.pad(raw_signal, (difference, 0), mode='constant', constant_values=0)
        padded_signal = padded_signal[:16000] # trim signal for same shape
        alligned_signal_list.append(padded_signal)
    return alligned_signal_list


#----------------------------

def synchronized_averaging(raw,threshold=500000):
   #reference_points= find_reference_points_transmit_start(raw,threshold)
   filtered_raw, reference_points=find_reference_points_transmit_start(raw, threshold)
   print("Raw After Null Experiments Removal: ",filtered_raw.shape)
   alligned_signal_list=get_align_signals(filtered_raw,reference_points)
   #averaging the signal
   averaged_signal=np.mean(alligned_signal_list,axis=0,keepdims=True)
   return averaged_signal
    

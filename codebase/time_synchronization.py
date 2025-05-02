from libaries import *
from global_parameters import *
from peak_to_peak_detection import *


def find_reference_points_transmit_max(raw,periods,time_axis_start=0,time_axis_end=16000):
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
   reference_points= find_reference_points_transmit_start(raw,threshold)
   alligned_signal_list=get_align_signals(raw,reference_points)
   #averaging the signal
   averaged_signal=np.mean(alligned_signal_list,axis=0,keepdims=True)
   return averaged_signal
    

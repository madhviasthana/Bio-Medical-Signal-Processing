from libaries import *
from global_parameters import *
from peak_to_peak_detection import *
from time_synchronization import *

def time_synchronized_averaging(raw,threshold):
    #dc offset removal
    dc_corrected_raw=dc_offset_removal(raw)
    #time averaging
    average_signal=synchronized_averaging(dc_corrected_raw,threshold)
    return average_signal

def dc_offset_removal(raw):
    # Convert to float32 to ensure proper subtraction
    dc_corrected = np.copy(raw).astype(np.float32)
    
    # Apply DC offset correction only to channel 2
    dc_corrected[:, 1, :] -= np.mean(dc_corrected[:, 1, :], axis=1, keepdims=True)
    
    print(dc_corrected.shape)
    return dc_corrected


def data_denoising():
    pass


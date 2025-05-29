from libaries import *
from global_parameters import *
from peak_to_peak_detection import *
from Data_Denoising.time_synchronization import *

def dc_offset_removal(raw):
    """
    Removes the DC offset from the receive channel (channel 1) only.

    """
    # Extract transmit channel (channel 0)
    transmit = raw[:, 0, :].astype(np.float32)
    transmit -= np.mean(transmit, axis=1, keepdims=True)


    # Extract and correct receive channel (channel 1)
    receive = raw[:, 1, :].astype(np.float32)
    receive -= np.mean(receive, axis=1, keepdims=True)

    print("DC Offset Removal - Transmit:", transmit.shape, " | Receive:", receive.shape)
    return transmit, receive

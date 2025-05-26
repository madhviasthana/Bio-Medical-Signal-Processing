from libaries import *
from global_parameters import *
from peak_to_peak_detection import *
from Data_Denoising.time_synchronization import *

def time_synchronized_averaging(transmit,recieve,threshold):
    #time averaging
    tx_avg, rx_avg=synchronized_averaging(transmit,recieve,threshold)

    return tx_avg, rx_avg


def data_denoising():
    pass


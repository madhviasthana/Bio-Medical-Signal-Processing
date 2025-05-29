from utils.libaries import *
from utils.data_loading import findFiles,LoadDataSignals
from utils.global_parameters import *
from Data_Denoising.time_synchronization import *

def time_synchronized_averaging(transmit,recieve,threshold):
    #time averaging
    tx_avg, rx_avg=synchronized_averaging(transmit,recieve,threshold)

    return tx_avg, rx_avg


def data_denoising():
    pass


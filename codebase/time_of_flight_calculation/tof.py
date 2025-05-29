from utils.libaries import *
from utils.data_loading import findFiles,LoadDataSignals
from utils.global_parameters import *

def findTOF(transmit_max_pair,receive_max_pair):
    sampling_frequency = 125e6  # 125 MHz
    time_per_sample = 1 / sampling_frequency  # Time per sample in seconds
    tof1 = transmit_max_pair[0]
    tof2 = receive_max_pair[0]
    print("Time of Flight Indices",tof1,tof2)
    tof = tof2-tof1
    tof = tof*time_per_sample
    print("Time of flight in seconds: ",tof)

    return tof
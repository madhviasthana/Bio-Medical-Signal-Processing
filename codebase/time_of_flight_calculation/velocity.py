from utils.libaries import *
from utils.data_loading import findFiles,LoadDataSignals
from utils.global_parameters import *

def find_Velocity(tof, distance=0.083):  # distance in meters
    if tof is None or tof == 0:
        print("Invalid TOF value. Skipping velocity calculation.")
        return None

    velocity = distance / tof
    return velocity

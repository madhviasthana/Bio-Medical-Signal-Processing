from utils.libaries import *
from utils.data_loading import findFiles,LoadDataSignals
from utils.global_parameters import *

def design_highpass_filter(cutoff_hz, fs_hz, order=2):
    nyquist = fs_hz / 2
    normalized_cutoff = cutoff_hz / nyquist
    sos = butter(order, normalized_cutoff, btype='highpass', output='sos')
    return sos

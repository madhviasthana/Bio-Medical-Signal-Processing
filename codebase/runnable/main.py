from utils.libaries import *
from utils.data_loading import findFiles,LoadDataSignals
from utils.global_parameters import *
from codebase.Data_Denoising.data_denoising import *


# Extract relevant files for processing
expected_waveform="sin"
expected_periods="9"
unique_file_list= findFiles(expected_waveform,expected_periods,sample_number=1)
print(unique_file_list)

# Data Denoising

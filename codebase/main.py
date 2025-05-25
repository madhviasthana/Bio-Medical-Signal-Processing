from libaries import *
from codebase.Data_Denoising.data_denoising import *
from data_loading import *
from global_parameters import *

# Extract relevant files for processing
expected_waveform="sin"
expected_periods="9"
unique_file_list= findFiles(expected_waveform,expected_periods,sample_number=1)
print(unique_file_list)

# Data Denoising

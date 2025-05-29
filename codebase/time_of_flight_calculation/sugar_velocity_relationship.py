from utils.libaries import *
from utils.data_loading import findFiles,LoadDataSignals
from utils.global_parameters import *
from Data_Denoising.data_denoising import *
from Data_Denoising.time_synchronization import *
from Data_Denoising.moving_average_filter import *
from Data_Denoising.derivative_filtering import apply_improved_derivative_filter
from Data_Denoising.dc_offset_removal import *
from plotting_module.signal_plot import *
from Data_Denoising.bandpass_filtering import *
from waveform_detection.detect_waveform import *
from waveform_detection.pan_algorithm import *
from time_of_flight_calculation.zero_crossings import *
from time_of_flight_calculation.tof import *
from time_of_flight_calculation.velocity import *
from time_of_flight_calculation.sugar_velocity_relationship import *

def calculate_sugar_percentage(sugar_mg, water_quantity_ml):
    """
    Calculate the sugar percentage based on the amount of sugar (in mg) and water quantity (in ml).
    
    :param sugar_mg: Amount of sugar in milligrams (mg)
    :param water_quantity_ml: Amount of water in milliliters (ml)
    :return: Sugar concentration as a fraction (e.g., 0.1 for 0.1%)
    """
    # 1700 mg of sugar in 1700 ml of water corresponds to 0.1%
    return (sugar_mg / water_quantity_ml) * 0.1

# Function to convert mg to percentages in velocities list
def convert_mg_to_percent(velocities, water_quantity_ml):
    converted_velocities = []
    for item in velocities:
        mg_value, velocity = item
        # Calculate the sugar concentration as a fraction
        percent_value = calculate_sugar_percentage(mg_value, water_quantity_ml)
        converted_velocities.append([percent_value, velocity])
    return converted_velocities

def process_signals(unique_file_list, comp_index=3):
    velocities = []
    concentrations = []
    tofs = []
    file_paths = []
    transmit_selected_index_list = [] #peak to peak calc
    receive_selected_index_list = [] #peak to peak calc
    receive_selected_amplitude = []
    transmit_selected_amplitude = []
    first_echo_start = []
    first_echo_end = []
    refractometer_readings = [0,1,2,3,4,5,6,7,8,9,10,11]
    selected_index_list = []

    start=0
    end=16000


    for file in unique_file_list:
        print("\n\n File Name:",file)
        raw,concentration,actual_waveform,periods=LoadDataSignals(file,time_axis_start=0,time_axis_end=16000)

        print("shape of raw signal: ",raw.shape)

        print("Period: ", periods)
        print("Concentration: ",concentration)

        # Dc offset removal
        transmit, receive= dc_offset_removal(raw)

        # Pan Tompkins Algorithm
        _receive = receive[0, start:end]
        _transmit = transmit[0, start:end]
        transmit_echo_list,recieve_echo_list,transmit_min_max_pairs,recieve_min_max_pairs=apply_pan_algorithm(_transmit,_receive,periods,T,low_cutoff, high_cutoff, order=4, window_size=11,min_prominence=0.05)

        # Zero Crossing
        
        # Get the first transmit echo pair
        transmit_max_pair = transmit_echo_list[0]
        t_start_index = transmit_max_pair[0]
        # Get the first recieve echo pair
        recieve_max_pair = recieve_echo_list[0]
        r_start_index = recieve_max_pair[0]

        transmit_zero_pair = find_next_zero_crossings(transmit[0,:], [t_start_index])
        receive_zero_pair = find_next_zero_crossings(receive[0,:], [r_start_index])

        tof = findTOF(transmit_zero_pair, receive_zero_pair) 

        tofs.append(tof)
        velocity = find_Velocity(tof, distance = 0.083)
        velocities.append(velocity)
        concentrations.append(int(concentration))
        print("Velocity: ", velocity)

    zipped_data = list(zip(concentrations,velocities))
    converted_velocity = convert_mg_to_percent(zipped_data, water_quantity)
    time_of_flight = list(zip(concentrations,tofs))
    receive_selected_index_list = list(zip(concentrations,file_paths,receive_selected_index_list,receive_selected_amplitude))
    transmit_selected_index_list = list(zip(concentrations,file_paths,transmit_selected_index_list,transmit_selected_amplitude))

    print("Selectd Index", receive_selected_index_list)

    return converted_velocity,time_of_flight,actual_waveform,receive_selected_index_list,transmit_selected_index_list #min(first_echo_start),max(first_echo_end)
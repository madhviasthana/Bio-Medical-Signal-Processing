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
from time_of_flight_calculation.correlation import *
from plotting_module.crosscorrelation_plot import *

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

def process_signals(unique_file_list, tof_method_index=1, comp_index=3):
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

    tof_methods = ['peak_to_peak', 'zero_crossing', 'cross_correlation']
    selected_method = tof_methods[tof_method_index]
    print("Selected Method is: ", selected_method)

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






        if selected_method == 'zero_crossing':
            #transmit_averaged_signal,recieve_averaged_signal=time_synchronized_averaging(raw[:,0,:],receive,threshold=500000)

            """#using time synchronized signal
            transmit_averaged_signal,recieve_averaged_signal=time_synchronized_averaging(raw[:,0,:],receive,threshold=500000)
            transmit_zero_pair = find_next_zero_crossings(transmit_averaged_signal[0], [t_start_index])
            receive_zero_pair = find_next_zero_crossings(recieve_averaged_signal[0], [r_start_index])"""
        
            """#using bandpass filter
            bandpassed_transmit = apply_bandpass_filter(transmit[0, start:end], fs, 1e6, 6.5e6)
            bandpassed_receive = apply_bandpass_filter(receive[0, start:end], fs, 1e6, 6.5e6)
            transmit_zero_pair = find_next_zero_crossings(bandpassed_transmit, [t_start_index])
            receive_zero_pair = find_next_zero_crossings(bandpassed_receive, [r_start_index])"""
            

            transmit_filtered_hanning = batch_apply_hanning_filter(transmit)
            recieve_filtered_hanning = batch_apply_hanning_filter(receive)

            #transmit_filtered_derivative=apply_improved_derivative_filter(transmit, T=T)
            #eceive_filtered_derivative=apply_improved_derivative_filter(receive, T=T)

            # using dc offset removed orignal signals

            transmit_zero_pair = find_next_zero_crossings(transmit_filtered_hanning[0,:], [t_start_index])
            receive_zero_pair = find_next_zero_crossings(recieve_filtered_hanning[0,:], [r_start_index])

            tof = findTOF(transmit_zero_pair, receive_zero_pair) 
        

        if selected_method == 'cross_correlation':
    
            #transmit_averaged_signal,recieve_averaged_signal=time_synchronized_averaging(raw[:,0,:],receive,threshold=500000)
            #bandpassed_transmit = apply_bandpass_filter(transmit_averaged_signal[0], fs, 12e6, 18e6)
            #bandpassed_receive = apply_bandpass_filter(recieve_averaged_signal[0], fs, 12e6, 18e6)

            bandpassed_transmit = apply_bandpass_filter(transmit[0, start:end], fs, 3e6, 7e6)
            bandpassed_receive = apply_bandpass_filter(receive[0, start:end], fs, 3e6, 7e6)

            transmit_filtered_derivative=apply_improved_derivative_filter(transmit, T=T)
            receive_filtered_derivative=apply_improved_derivative_filter(receive, T=T)


            
            #tof, sample_delay, corr = calculate_tof_cross_correlation(bandpassed_transmit[:3000], bandpassed_receive[6000:], fs=125e6)

            try:
                tof, delay_samples, corr, lags = calculate_windowed_tof_cross_correlation(
                    bandpassed_transmit, bandpassed_receive,
                    t_start_index, r_start_index-100,
                    fs=125e6, window_size=600
                )
                print("TOF calculated:", tof)
                plot_windowed_cross_correlation(corr, lags, tof)
            except Exception as e:
                print(f"[ERROR] Cross-correlation TOF calculation failed: {e}")
                continue  # skip to next file

            #plot_cross_correlation(bandpassed_transmit[:3000], bandpassed_receive[6000:], corr, sample_delay, fs, concentration, actual_waveform, receive_start_index=6000)





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


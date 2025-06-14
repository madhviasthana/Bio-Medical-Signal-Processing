
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
from plotting_module.signal_veclocity_plot import *
from time_of_flight_calculation.correlation import *
from time_of_flight_calculation.metrics import *

def process_experiments(unique_file_list, time_axis_start=0, time_axis_end=16000, num_files_to_plot=5, experiments_per_file=5):
    """
    Process ultrasonic CMUT signals for statistical analysis, extract echoes, and visualize signals.
    Prints the starting point of the receive echo for each experiment.
    
    Parameters:
    - unique_file_list: List of file paths to .mat files (from findFiles).
    - time_axis_start: Start index for time axis (default: 0).
    - time_axis_end: End index for time axis (default: 16000).
    - num_files_to_plot: Number of files to visualize (default: 3).
    - experiments_per_file: Number of experiments to plot per file (default: 3).
    
    Returns:
    - all_signals: List of raw signal arrays (100, 2, 16000) for each file.
    - all_concentrations: List of concentration values (mg) for each file.
    - all_echo_data: List of extracted echo signals [(experiment, channel, samples), ...] for each file.
    - all_echo_starts: List of echo start indices (100, 2) for each file.
    - all_echo_ends: List of echo end indices (100, 2) for each file.
    - all_waveforms: List of waveform types (e.g., 'squ') for each file.
    - all_periods: List of period values for each file.
    """
    
    # Initialize lists to store results
    all_signals = []
    all_concentrations = []
    all_echo_data = []
    all_echo_starts = []
    all_echo_ends = []
    all_waveforms = []
    all_periods = []
    
    # Sampling frequency and time axis
    fs = 125_000_000  # 125 MHz
    time = np.arange(time_axis_start, time_axis_end) / fs * 1e9  # Time in nanoseconds
    
    for file_idx, file_path in enumerate(unique_file_list):
        print(f"\nProcessing File: {file_path}")
        
        # Load data using your function
        raw, concentration, waveform, periods = LoadDataSignals(file_path, time_axis_start, time_axis_end)
        print(f"Shape of raw signal: {raw.shape}")
        print(f"Concentration: {concentration} mg, Waveform: {waveform}, Period: {periods}")
        
        # Store raw signals and metadata
        all_signals.append(raw)
        all_concentrations.append(int(concentration))
        all_waveforms.append(waveform)
        all_periods.append(periods)
        
        # DC offset removal
        transmit, receive = dc_offset_removal(raw)
        
        # Initialize arrays for echo start/end indices
        echo_starts = np.zeros((100, 2), dtype=int)
        echo_ends = np.zeros((100, 2), dtype=int)
        file_echo_data = []
        
        # Process each experiment in the file
        for exp in range(100):
            # Extract signals for this experiment
            _transmit = transmit[exp, time_axis_start:time_axis_end]
            _receive = receive[exp, time_axis_start:time_axis_end]
            
            # Apply Pan-Tompkins algorithm
            transmit_echo_list, receive_echo_list, transmit_min_max_pairs, receive_min_max_pairs = apply_pan_algorithm(
                _transmit, _receive, periods, T, low_cutoff, high_cutoff, order=4, window_size=11, min_prominence=0.05
            )
            
            # Get first echo start/end indices
            if transmit_echo_list and receive_echo_list:
                # Transmit channel (Channel 0)
                transmit_max_pair = transmit_echo_list[0]
                echo_starts[exp, 0] = transmit_max_pair[0]  # Start index
                echo_ends[exp, 0] = transmit_max_pair[1] if len(transmit_max_pair) > 1 else transmit_max_pair[0] + 200  # Fallback end
                file_echo_data.append(transmit[exp, echo_starts[exp, 0]:echo_ends[exp, 0]])
                
                # Receive channel (Channel 1)
                receive_max_pair = receive_echo_list[0]
                echo_starts[exp, 1] = receive_max_pair[0]  # Start index
                echo_ends[exp, 1] = receive_max_pair[1] if len(receive_max_pair) > 1 else receive_max_pair[0] + 200  # Fallback end
                file_echo_data.append(receive[exp, echo_starts[exp, 1]:echo_ends[exp, 1]])
            else:
                # Fallback if no echoes detected
                echo_starts[exp, :] = time_axis_start
                echo_ends[exp, :] = time_axis_start + 200
                file_echo_data.append(transmit[exp, time_axis_start:time_axis_start + 200])
                file_echo_data.append(receive[exp, time_axis_start:time_axis_start + 200])
            
            # Print the starting point of the receive echo in microseconds
            receive_echo_start_time = echo_starts[exp, 1] / fs * 1e9
            print(f"Experiment {exp + 1} - Receive Echo Start: {receive_echo_start_time:.1f} µs")
        
        # Store echo data and indices for this file
        all_echo_data.append(file_echo_data)
        all_echo_starts.append(echo_starts)
        all_echo_ends.append(echo_ends)
        
        # Visualize signals for a subset of files
        if file_idx < num_files_to_plot:
            plt.figure(figsize=(10, 16))
            for exp in range(min(experiments_per_file, 100)):
                plt.subplot(experiments_per_file, 1, exp + 1)
                plt.plot(time, transmit[exp, :], label="Transmit (Ch 1)", alpha=0.7)
                plt.plot(time, receive[exp, :], label="Receive (Ch 2)", alpha=0.7)
                plt.axvline(x=time[echo_starts[exp, 0]], color='r', linestyle='--', alpha=0.5, label="Transmit Echo")
                plt.axvline(x=time[echo_ends[exp, 0]], color='r', linestyle='--', alpha=0.5)
                plt.axvline(x=time[echo_starts[exp, 1]], color='g', linestyle='--', alpha=0.5, label="Receive Echo")
                plt.axvline(x=time[echo_ends[exp, 1]], color='g', linestyle='--', alpha=0.5)
                plt.xlabel("Time (ns)")
                plt.ylabel("Amplitude")
                plt.title(f"Experiment {exp + 1} - Concentration: {concentration} mg ({waveform}, Period {periods})")
                plt.legend()
                plt.tight_layout()
            plt.show()
    
    return all_signals, all_concentrations, all_echo_data, all_echo_starts, all_echo_ends, all_waveforms, all_periods


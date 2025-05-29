
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





def plot_velocity_refractometer(velocities, actual_waveform):
    """
    Plots Velocity vs Concentration with a very faint dotted line for Refractometer vs. Concentration.
    
    velocities: List of tuples with (concentration, velocity)
    actual_waveform: String representing the waveform type.
    """
    waveform=actual_waveform[0:3]
    if waveform=='sin':
        waveform='Sinusoidal'
    else:
        waveform='Square'
    
    burst_size=actual_waveform[-1]

    #velocities = sorted(velocities, key=lambda x: float(x[0].rstrip('%')))
    velocities = sorted(velocities, key=lambda x: x[0])


    concentrations = [item[0] for item in velocities]
    velocity_values = [item[1] for item in velocities]

    # Refractometer values should be a direct mapping (0% -> 0, 1% -> 1, ..., 10% -> 10)
    refractometer_values = [conc for conc in concentrations]

    # Plotting
    fig, ax1 = plt.subplots(figsize=(10, 6))

    ax1.set_xlabel('Concentration (%)')
    ax1.set_ylabel('Velocity (m/s)', color='tab:blue')
    ax1.plot(concentrations, velocity_values, marker='o', linestyle='-', color='tab:blue', label='Velocity')
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    # ax1.set_ylim([min(velocity_values)-1.4,max(velocity_values)+2])

    ax2 = ax1.twinx()
    ax2.set_ylabel('Refractometer Reading', color='tab:red')  # Faint axis label
    ax2.plot(concentrations, refractometer_values, marker='s', linestyle=':', color='tab:red', alpha = 0.3)  
    ax2.tick_params(axis='y', labelcolor='tab:red')  # Keeping it standard without 'alpha'

    plt.title(f'Velocity vs Sugar Concentration of ({waveform}) waveform with Burst Size {burst_size}', fontsize = 12, fontweight='normal')
    ax1.grid(True)

    # Show Plot
    plt.show()
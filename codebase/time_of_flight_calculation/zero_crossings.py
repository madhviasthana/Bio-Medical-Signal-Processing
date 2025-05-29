from libaries import *
from global_parameters import *


def find_next_zero_crossings(signal, extrema_indices):
    """
    Find the indices of the next zero-crossing after each given extrema point.
    
    Parameters:
        signal (list or array-like): The input signal array.
        extrema_indices (list): List of indices of extrema points.
        
    Returns:
        list: List of indices of the next zero-crossing for each extrema point.
               Returns the exact interpolated value (float) when possible.
               None is returned for an extrema if no zero-crossing is found.
    """
    zero_crossings = []
    print("extrema_indices: ",extrema_indices)
    print(f"Signal at index 2: {signal[2]} (sign: {np.sign(signal[2])})")
    print(f"Signal slice after index 2: {signal[3:10]}")  # or more depending on length

    
    for extrema_index in extrema_indices:
        # Check if we're already at the end of the signal
        if extrema_index >= len(signal) - 1:
            zero_crossings.append(None)
            continue


        
        print("extrema_index:", extrema_index, "type:", type(extrema_index))

        # Get the sign of the current value
        #current_sign = np.sign(signal[extrema_index])
        index = extrema_index 
        current_sign = np.sign(signal[int(extrema_index)])


        
        # Initialize with None in case no zero-crossing is found
        crossing_index = None
        
        # Search for sign change
        for i in range(extrema_index + 1, len(signal)):
            next_sign = np.sign(signal[i])

            
            # Check if we've found a zero-crossing (sign change or exact zero)
            if next_sign != current_sign or next_sign == 0:
                # For exact crossing (when the value equals zero)
                if next_sign == 0:
                    crossing_index = float(i)
                    break
                
                # For crossing between two points, find the more precise crossing
                # using linear interpolation
                if i > extrema_index + 1:
                    # Calculate the interpolated index where the signal crosses zero
                    x1, y1 = i-1, signal[i-1]
                    x2, y2 = i, signal[i]
                    
                    # Avoid division by zero
                    if y1 != y2:
                        crossing_index = x1 + (0 - y1) * (x2 - x1) / (y2 - y1)
                        break
                
                crossing_index = float(i)
                break
        
        zero_crossings.append(crossing_index)
    
    return zero_crossings
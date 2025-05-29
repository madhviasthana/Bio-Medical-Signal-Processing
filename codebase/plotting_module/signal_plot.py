from utils.libaries import *
from utils.data_loading import findFiles,LoadDataSignals
from utils.global_parameters import *
def signal_plot(signal, start=0, end=16000, Fs=125e6, title="Signal",x_buffer=100):
    
    # Plots a signal in time domain, adapting to input shape (single or batch).

    Ts_ns = 1e9 / Fs  # Sampling period in nanoseconds
    time = np.arange(start, end) #* Ts_ns

    plt.figure(figsize=(10, 4))

    if signal.ndim == 1:
        # Single signal
        plt.plot(time, signal[start:end], label="Signal", color="steelblue")

    elif signal.ndim == 2:
        # Batch of signals
        for i in range(min(5, signal.shape[0])):  # Limit to 5 plots for clarity
            plt.plot(time, signal[i, start:end], label=f"Sample {i+1}", alpha=0.7)

    else:
        raise ValueError("Signal must be either 1D or 2D with shape (batch, time)")

    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel("Time Sample (ns)")
    plt.ylabel("Relative Amplitude")
    plt.grid(True, linestyle='--', alpha=0.3)

    plt.legend()
    plt.tight_layout()
    plt.show()

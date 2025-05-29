from scipy import signal
from numpy.random import default_rng
from scipy.fft import fft, ifft
import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
from scipy.signal import find_peaks #NEW
import os
import math
from os.path import exists
from scipy.ndimage import uniform_filter
from scipy.ndimage import median_filter
from scipy.signal import convolve
from scipy.signal import lfilter, lfilter_zi
import matplotlib.pyplot as plt
from numpy.fft import fft, fftfreq
from scipy.signal import butter, sosfilt
from scipy.signal import filtfilt
from scipy.signal import correlate
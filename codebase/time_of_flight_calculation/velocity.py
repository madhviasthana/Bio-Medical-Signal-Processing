from libaries import *
from global_parameters import *

def find_Velocity(tof, distance = 0.083): # distance in meters?
    velocity = distance/tof
    return velocity
from utils.libaries import *
from utils.global_parameters import *


def findFiles(expected_waveform,expected_periods,sample_number=1):
    """_summary_

    Args:
        expected_waveform (_type_): It takes the waveform that you expect type of that.
        expected_periods (_type_): how many bursts or periods you need.
        sample_number (int, optional): There are many samples which sample you may want to consider but for simplicity I am just considering the sample number =1

    Returns:
        _type_: a list of files extracted
    """
    unique_file_list=[]
    for i in os.listdir(root_folder):
        print(i)
        if os.path.isdir(root_folder+'//'+i):

            for j in os.listdir(root_folder+'//'+i):
                if j.endswith('mat'):
                    actual_waveform=j.split("-")[-2][0:3]
                    actual_periods=j.split("-")[-2][3:4]
                    sample=j.split("_")[-1].split('.')[0]

                    if actual_waveform==expected_waveform and actual_periods==expected_periods and sample_number==int(sample):
                        unique_file_list.append(root_folder+'/'+i+"/"+j)      

    return unique_file_list       


def LoadDataSignals(file_path,time_axis_start=0,time_axis_end=16000):    

    fs=125000000 # Sampling frequency in HZ

    #Extracting the values from file path


    actual_waveform=file_path.split("-")[-2]
    #Concentration=file_path.split("/")[-2]
    Concentration= file_path.split("-")[-3].strip("mg")

    periods=int(actual_waveform[-1])
    waveform=actual_waveform=file_path.split("-")[-2][0:3]


    title=Concentration +" " +"("+actual_waveform +")"

    #Loading mat file data
    mat_data = loadmat(file_path)        
    raw = np.squeeze(mat_data['raw_data']) #remove single dimension [100,2,16000]

    # Raw transmit and receive signals
    #raw_transmit_signal=raw[0,0,time_axis_start:time_axis_end]
    #raw_receive_signal=raw[0,1,time_axis_start:time_axis_end]

    return raw,Concentration,waveform,periods
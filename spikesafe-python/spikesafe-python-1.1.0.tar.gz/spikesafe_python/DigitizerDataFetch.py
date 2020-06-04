# Goal: Read all new voltage readings from SpikeSafe SMU Digitizer
# SCPI Command: VOLT:FETC?
# Array of voltage readings are parsed into DigitizerData class
# Example data return: b'9.9712145e-01,1.0005457e+00,3.2105038e+01\n'

import sys
import logging
from .DigitizerData import DigitizerData
from .Threading import wait
from .ReadAllEvents import read_all_events
from .MemoryTableReadData import log_memory_table_read

log = logging.getLogger(__name__)

def fetch_voltage_data(spike_safe_socket):
    """Returns an array of voltage readings from the digitizer obtained through a fetch query 

    Parameters
    ----------
    spike_safe_socket : TcpSocket
        Socket object used to communicate with SpikeSafe
    
    Returns
    -------
    digitizer_data_collection: DigitizerData[]
        Contains an array of DigitizerData objects which each have a Sample Number and Voltage Reading

    Raises
    ------
    Exception
        On any error
    """
    try:
        # fetch the Digitizer voltage readings
        spike_safe_socket.send_scpi_command('VOLT:FETC?')
        digitizer_data_string = spike_safe_socket.read_data()

        # set up the DigitizerData array to be returned
        digitizer_data_collection = []

        # put the fetched data in a plottable data format
        voltage_reading_strings = digitizer_data_string.split(",")
        sample = 1
        for v in voltage_reading_strings:
            data_point = DigitizerData()
            data_point.voltage_reading = float(v)
            data_point.sample_number = sample

            digitizer_data_collection.append(data_point)
            sample += 1

        return digitizer_data_collection

    except Exception as err:
        # print any error to the log file and raise error to function caller
        log.error("Error fetching digitizer voltage data: {}".format(err))                                     
        raise

def wait_for_new_voltage_data(spike_safe_socket, wait_time = 0.0):
    """Queries the SpikeSafe SMU digitizer until it responds that it has acquired new data

    This is a useful function to call prior to sending a fetch query, because it determines whether fetched data will be freshly acquired

    Parameters
    ----------
    spike_safe_socket : TcpSocket
        Socket object used to communicate with SpikeSafe
    wait_time: float
        Wait time in between each set of queries, in seconds
    
    Raises
    ------
    Exception
        On any error
    """
    try:
        digitizer_has_new_data = ''
        while digitizer_has_new_data != 'TRUE':                       
            
            # check for new digitizer data
            spike_safe_socket.send_scpi_command('VOLT:NDAT?')
            digitizer_has_new_data = spike_safe_socket.read_data()

            # update SpikeSafe status every time we check for new data
            read_all_events(spike_safe_socket)
            log_memory_table_read(spike_safe_socket)

            wait(wait_time)

    except Exception as err:
        # print any error to the log file and raise error to function caller
        log.error("Error waiting for new digitizer voltage data: {}".format(err))                                     
        raise
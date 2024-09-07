# import pandas as pd
# import numpy as np
# import matplotlib
# import obd
# import time
# import datetime
# import requests
# import serial

# obd_connector="/dev/ttyACM0"
# # obd_connector = '/dev/pts/2'
# connection = obd.Async(obd_connector)

# # a callback that prints every new value to the console
# def new_rpm(r):
#     print(r)

# connection.watch(obd.commands.PIDS_A, callback=new_rpm)
# connection.watch(obd.commands.PIDS_B, callback=new_rpm)
# connection.watch(obd.commands.PIDS_C, callback=new_rpm)
# connection.start()

# # the callback will now be fired upon receipt of new values

# time.sleep(10)
# connection.stop()

import pandas as pd
import numpy as np
import matplotlib
import obd
import time
import datetime
import requests
import serial

# Global variables to store the supported PID values
supported_pids_A = []
supported_pids_B = []
supported_pids_C = []

# Function to map binary strings to supported PIDs
def map_binary_to_pids(binary_string, start_pid):
    supported_pids = []

    for i, bit in enumerate(binary_string):
        if bit == '1':
            # Calculate the actual PID number without the 0x prefix
            pid = start_pid + i
            supported_pids.append(f"{pid:02X}")

    return supported_pids

# Dictionary to store the PID responses
pid_responses = {
    'PIDS_A': None,
    'PIDS_B': None,
    'PIDS_C': None
}

# Callback function that stores values for PIDS_A, PIDS_B, PIDS_C
def pid_callback(response):
    if not response.is_null():
        cmd_name = response.command.name
        pid_responses[cmd_name] = response.value.bits  # Store the binary value

# Connect to OBD-II interface
obd_connector = "/dev/ttyACM0"  # Replace with your OBD-II port
connection = obd.Async(obd_connector)

# Watch the PIDS_A, PIDS_B, PIDS_C commands and store their results
connection.watch(obd.commands.PIDS_A, callback=pid_callback)
connection.watch(obd.commands.PIDS_B, callback=pid_callback)
connection.watch(obd.commands.PIDS_C, callback=pid_callback)
connection.start()

# Wait for 10 seconds to receive data
time.sleep(10)

# Stop the connection
connection.stop()

# Process and store the supported PIDs from stored binary strings in global variables
if pid_responses['PIDS_A']:
    supported_pids_A = map_binary_to_pids(pid_responses['PIDS_A'], 0x01)
    print(f"Supported PIDs (01 - 20): {supported_pids_A}")

if pid_responses['PIDS_B']:
    supported_pids_B = map_binary_to_pids(pid_responses['PIDS_B'], 0x21)
    print(f"Supported PIDs (21 - 40): {supported_pids_B}")

if pid_responses['PIDS_C']:
    supported_pids_C = map_binary_to_pids(pid_responses['PIDS_C'], 0x41)
    print(f"Supported PIDs (41 - 60): {supported_pids_C}")

# Now you can use supported_pids_A, supported_pids_B, and supported_pids_C globally in your code

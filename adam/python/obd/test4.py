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
import os
import time
import datetime
import requests
import serial

# Dictionary mapping PID numbers to their descriptions
pid_descriptions = {
    "00": "PIDS_A",
    "01": "STATUS",
    "02": "FREEZE_DTC",
    "03": "FUEL_STATUS",
    "04": "ENGINE_LOAD",
    "05": "COOLANT_TEMP",
    "06": "SHORT_FUEL_TRIM_1",
    "07": "LONG_FUEL_TRIM_1",
    "08": "SHORT_FUEL_TRIM_2",
    "09": "LONG_FUEL_TRIM_2",
    "0A": "FUEL_PRESSURE",
    "0B": "INTAKE_PRESSURE",
    "0C": "RPM",
    "0D": "SPEED",
    "0E": "TIMING_ADVANCE",
    "0F": "INTAKE_TEMP",
    "10": "MAF",
    "11": "THROTTLE_POS",
    "12": "AIR_STATUS",
    "13": "O2_SENSORS",
    "14": "O2_B1S1",
    "15": "O2_B1S2",
    "16": "O2_B1S3",
    "17": "O2_B1S4",
    "18": "O2_B2S1",
    "19": "O2_B2S2",
    "1A": "O2_B2S3",
    "1B": "O2_B2S4",
    "1C": "OBD_COMPLIANCE",
    "1D": "O2_SENSORS_ALT",
    "1E": "AUX_INPUT_STATUS",
    "1F": "RUN_TIME",
    "20": "PIDS_B",
    "21": "DISTANCE_W_MIL",
    "22": "FUEL_RAIL_PRESSURE_VAC",
    "23": "FUEL_RAIL_PRESSURE_DIRECT",
    "24": "O2_S1_WR_VOLTAGE",
    "25": "O2_S2_WR_VOLTAGE",
    "26": "O2_S3_WR_VOLTAGE",
    "27": "O2_S4_WR_VOLTAGE",
    "28": "O2_S5_WR_VOLTAGE",
    "29": "O2_S6_WR_VOLTAGE",
    "2A": "O2_S7_WR_VOLTAGE",
    "2B": "O2_S8_WR_VOLTAGE",
    "2C": "COMMANDED_EGR",
    "2D": "EGR_ERROR",
    "2E": "EVAPORATIVE_PURGE",
    "2F": "FUEL_LEVEL",
    "30": "WARMUPS_SINCE_DTC_CLEAR",
    "31": "DISTANCE_SINCE_DTC_CLEAR",
    "32": "EVAP_VAPOR_PRESSURE",
    "33": "BAROMETRIC_PRESSURE",
    "34": "O2_S1_WR_CURRENT",
    "35": "O2_S2_WR_CURRENT",
    "36": "O2_S3_WR_CURRENT",
    "37": "O2_S4_WR_CURRENT",
    "38": "O2_S5_WR_CURRENT",
    "39": "O2_S6_WR_CURRENT",
    "3A": "O2_S7_WR_CURRENT",
    "3B": "O2_S8_WR_CURRENT",
    "3C": "CATALYST_TEMP_B1S1",
    "3D": "CATALYST_TEMP_B2S1",
    "3E": "CATALYST_TEMP_B1S2",
    "3F": "CATALYST_TEMP_B2S2",
    "40": "PIDS_C",
    "41": "STATUS_DRIVE_CYCLE",
    "42": "CONTROL_MODULE_VOLTAGE",
    "43": "ABSOLUTE_LOAD",
    "44": "COMMANDED_EQUIV_RATIO",
    "45": "RELATIVE_THROTTLE_POS",
    "46": "AMBIANT_AIR_TEMP",
    "47": "THROTTLE_POS_B",
    "48": "THROTTLE_POS_C",
    "49": "ACCELERATOR_POS_D",
    "4A": "ACCELERATOR_POS_E",
    "4B": "ACCELERATOR_POS_F",
    "4C": "THROTTLE_ACTUATOR",
    "4D": "RUN_TIME_MIL",
    "4E": "TIME_SINCE_DTC_CLEARED",
    "4F": "unsupported",
    "50": "MAX_MAF",
    "51": "FUEL_TYPE",
    "52": "ETHANOL_PERCENT",
    "53": "EVAP_VAPOR_PRESSURE_ABS",
    "54": "EVAP_VAPOR_PRESSURE_ALT",
    "55": "SHORT_O2_TRIM_B1",
    "56": "LONG_O2_TRIM_B1",
    "57": "SHORT_O2_TRIM_B2",
    "58": "LONG_O2_TRIM_B2",
    "59": "FUEL_RAIL_PRESSURE_ABS",
    "5A": "RELATIVE_ACCEL_POS",
    "5B": "HYBRID_BATTERY_REMAINING",
    "5C": "OIL_TEMP",
    "5D": "FUEL_INJECT_TIMING",
    "5E": "FUEL_RATE",
    "5F": "unsupported"
}

# Single global variable to store all supported PID values
supported_pids = []

# Function to map binary strings to supported PIDs
def map_binary_to_pids(binary_string, start_pid):
    pids = []
    for i, bit in enumerate(binary_string):
        if bit == '1':
            # Calculate the actual PID number without the 0x prefix
            pid = start_pid + i
            pids.append(f"{pid:02X}")
    return pids

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
# obd_connector = "/dev/pts/2"  # Replace with your OBD-II port?
obd_connector = "/dev/ttyACM0"
connection = obd.Async(obd_connector)


# Watch the PIDS_A, PIDS_B, PIDS_C commands and store their results
connection.watch(obd.commands.PIDS_A, callback=pid_callback)
connection.watch(obd.commands.PIDS_B, callback=pid_callback)
connection.watch(obd.commands.PIDS_C, callback=pid_callback)

connection.start()

# Wait for 10 seconds to receive data
time.sleep(5)

# Stop the connection
connection.stop()

# Process and store all supported PIDs in the single global variable
if pid_responses['PIDS_A']:
    supported_pids.extend(map_binary_to_pids(pid_responses['PIDS_A'], 0x01))
    print(f"Added PIDs (01 - 20)")

if pid_responses['PIDS_B']:
    supported_pids.extend(map_binary_to_pids(pid_responses['PIDS_B'], 0x21))
    print(f"Added PIDs (21 - 40)")

if pid_responses['PIDS_C']:
    supported_pids.extend(map_binary_to_pids(pid_responses['PIDS_C'], 0x41))
    print(f"Added PIDs (41 - 60)")

# Print all supported PIDs
print(f"All supported PIDs: {supported_pids}")

# Now you can use the supported_pids variable globally in your code

# Use the updated dictionary in the rest of your code


def get_pid_names(supported_pids):
    pid_names = []
    for pid in supported_pids:
        if pid in pid_descriptions:
            pid_names.append(f"{pid_descriptions[pid]}")
        else:
            pid_names.append(f"Unknown")
    return pid_names

# Get the names of the supported PIDs
supported_pid_names = get_pid_names(supported_pids)
print(len(supported_pid_names))
df = pd.DataFrame(columns=supported_pid_names)

# Print the names of supported PIDs
print("Supported PIDs and their descriptions:")
for pid_name in supported_pid_names:
    print(pid_name)

# Get the first and last elements dynamically from the list
first_pid = supported_pid_names[0]  # First element (replace "SPEED")
last_pid = supported_pid_names[-1]  # Last element (replace "THROTTLE_POS")


def pid_data_callback(response):
    global df
    command_name = response.command.name
    value = response.value.magnitude if hasattr(response.value, 'magnitude') else response.value
    print(command_name,value)

    if command_name == first_pid:
            # Create a new row with the PID name and value
            new_row = {col: np.nan for col in df.columns}
            new_row[first_pid] = value
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            # print(f"Speed: {value}")
    else:
        # Update the last row with the current PID value
        if command_name in df.columns:
            df.at[len(df) - 1, command_name] = value
            # print(f"{command_name}: {value}")
        else:
            print(f"Warning: {command_name} not found in DataFrame columns")

# Path to store the dataset
# file_path = 'dataset/async_log_single_row.csv'

if supported_pids:
    connection = obd.Async(obd_connector)
    for pid in supported_pids:
        command = obd.commands[1][int(pid, 16)]
        connection.watch(command, callback=pid_data_callback)

    connection.start()
    time.sleep(25)
    connection.stop()
else:
    print("No supported PIDs found.")
# pd.set_option('display.max_columns', None)
# Replace NaNs with None
# df = df.where(pd.notnull(df), None)
print(df)

# Path to store the dataset
file_path = 'dataset/real_car.csv'

file_exists = os.path.isfile(file_path)
# Save the DataFrame to a CSV file
df.to_csv(file_path, mode='a', index=False, header=not file_exists)

print(f"DataFrame saved to {file_path}")

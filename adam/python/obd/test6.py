import pandas as pd
import numpy as np
import obd
import time
import os

# Initialize OBD connection
# obd_connector = "/dev/ttyACM0"  # Replace with your OBD-II port
obd_connector = "/dev/pts/2"  # Replace with your OBD-II port
connection = obd.Async(obd_connector)

# Global variables for supported PIDs and DataFrame
supported_pids_A = []
supported_pids_B = []
supported_pids_C = []
pid_responses = {'PIDS_A': None, 'PIDS_B': None, 'PIDS_C': None}

# Path to store the dataset
file_path = 'dataset/async_log_single_row.csv'

# Initialize DataFrame with the new list of columns
columns = [
    "Start_Time", "STATUS", "FUEL_STATUS", "ENGINE_LOAD", "COOLANT_TEMP", "SHORT_FUEL_TRIM_1",
    "LONG_FUEL_TRIM_1", "INTAKE_PRESSURE", "RPM", "SPEED", "TIMING_ADVANCE", "INTAKE_TEMP",
    "THROTTLE_POS", "O2_SENSORS", "O2_B1S1", "O2_B1S2", "OBD_COMPLIANCE", "RUN_TIME", "PIDS_B",
    "DISTANCE_W_MIL", "EVAPORATIVE_PURGE", "WARMUPS_SINCE_DTC_CLEAR", "DISTANCE_SINCE_DTC_CLEAR",
    "BAROMETRIC_PRESSURE", "PIDS_C", "CONTROL_MODULE_VOLTAGE", "ABSOLUTE_LOAD", "RELATIVE_THROTTLE_POS",
    "THROTTLE_POS_B", "ACCELERATOR_POS_D", "ACCELERATOR_POS_E", "THROTTLE_ACTUATOR", "End_Time"
]
df = pd.DataFrame(columns=columns)

# Function to map binary strings to supported PIDs
def map_binary_to_pids(binary_string, start_pid):
    supported_pids = []
    for i, bit in enumerate(binary_string):
        if bit == '1':
            pid = start_pid + i
            supported_pids.append(f"{pid:02X}")
    return supported_pids

# Callback function for initial PID discovery
def pid_callback_initial(response):
    if not response.is_null():
        cmd_name = response.command.name
        pid_responses[cmd_name] = response.value.bits

# Updated callback function to collect real-time data
def pid_data_callback(response):
    global df
    command_name = response.command.name
    value = response.value
    timestamp = time.time()

    # Add the timestamp and the value to the DataFrame
    df.loc[len(df), 'Time'] = timestamp

    # Handle cases where the value is a list (e.g., O2 sensors)
    if isinstance(value, list):
        # Ensure there are enough columns for the list elements
        for i in range(len(value)):
            column_name = f"{command_name}_{i+1}"  # Create dynamic column names
            if column_name not in df.columns:
                df[column_name] = np.nan  # Add new column if needed
            df.loc[len(df) - 1, column_name] = value[i]
    else:
        df.loc[len(df) - 1, command_name] = value

    print(f"{command_name}: {value}")

# Steps 1-3: Discover supported PIDs and process them
connection.watch(obd.commands.PIDS_A, callback=pid_callback_initial)
connection.watch(obd.commands.PIDS_B, callback=pid_callback_initial)
connection.watch(obd.commands.PIDS_C, callback=pid_callback_initial)
connection.start()
time.sleep(10)
connection.stop()

# Process supported PIDs
if pid_responses['PIDS_A']:
    supported_pids_A = map_binary_to_pids(pid_responses['PIDS_A'], 0x01)
if pid_responses['PIDS_B']:
    supported_pids_B = map_binary_to_pids(pid_responses['PIDS_B'], 0x21)
if pid_responses['PIDS_C']:
    supported_pids_C = map_binary_to_pids(pid_responses['PIDS_C'], 0x41)

all_supported_pids = supported_pids_A + supported_pids_B + supported_pids_C

# Step 4: Start monitoring and collecting real-time data for supported PIDs
if all_supported_pids:
    connection = obd.Async(obd_connector)
    for pid in all_supported_pids:
        command = obd.commands[1][int(pid, 16)]
        connection.watch(command, callback=pid_data_callback)

    connection.start()
    time.sleep(20)
    connection.stop()

    # Save collected data to a CSV file
    df.to_csv(file_path, mode='a', header=not os.path.exists(file_path), index=False)
    print("Data collection complete. Data saved to CSV.")
    print(df)
else:
    print("No supported PIDs found.")


# import pandas as pd
# import numpy as np
# import obd
# import time
# import os

# # Initialize OBD connection
# obd_connector = "/dev/ttyACM0"  # Replace with your OBD-II port
# connection = obd.Async(obd_connector)

# # Global variables for supported PIDs and DataFrame
# supported_pids_A = []
# supported_pids_B = []
# supported_pids_C = []
# pid_responses = {'PIDS_A': None, 'PIDS_B': None, 'PIDS_C': None}

# # Dictionary to store the latest data for each PID
# latest_data = {}

# # Path to store the dataset
# file_path = 'dataset/async_log_single_row.csv'

# # Function to map binary strings to supported PIDs
# def map_binary_to_pids(binary_string, start_pid):
#     supported_pids = []
#     for i, bit in enumerate(binary_string):
#         if bit == '1':
#             pid = start_pid + i
#             supported_pids.append(f"{pid:02X}")
#     return supported_pids

# # Callback function for initial PID discovery
# def pid_callback_initial(response):
#     if not response.is_null():
#         cmd_name = response.command.name
#         pid_responses[cmd_name] = response.value.bits

# # Callback function to collect real-time data
# def pid_data_callback(response):
#     command_name = response.command.name
#     value = response.value
#     latest_data[command_name] = value
#     print(f"{command_name}: {value}")

# # Steps 1-3: Discover supported PIDs and process them
# connection.watch(obd.commands.PIDS_A, callback=pid_callback_initial)
# connection.watch(obd.commands.PIDS_B, callback=pid_callback_initial)
# connection.watch(obd.commands.PIDS_C, callback=pid_callback_initial)
# connection.start()
# time.sleep(10)
# connection.stop()

# if pid_responses['PIDS_A']:
#     supported_pids_A = map_binary_to_pids(pid_responses['PIDS_A'], 0x01)
# if pid_responses['PIDS_B']:
#     supported_pids_B = map_binary_to_pids(pid_responses['PIDS_B'], 0x21)
# if pid_responses['PIDS_C']:
#     supported_pids_C = map_binary_to_pids(pid_responses['PIDS_C'], 0x41)

# all_supported_pids = supported_pids_A + supported_pids_B + supported_pids_C

# # Step 4: Start monitoring and collecting real-time data for supported PIDs
# if all_supported_pids:
#     connection = obd.Async(obd_connector)
#     for pid in all_supported_pids:
#         command = obd.commands[1][int(pid, 16)]
#         connection.watch(command, callback=pid_data_callback)

#     connection.start()
#     time.sleep(20)
#     connection.stop()

#     # Prepare the data for a single row
#     row_data = {'Time': time.time()}
#     row_data.update(latest_data)

#     # Create a DataFrame with a single row
#     df = pd.DataFrame([row_data])

#     # Save collected data to a CSV file
#     df.to_csv(file_path, mode='a', header=not os.path.exists(file_path), index=False)
#     print("Data collection complete. Data saved to CSV.")
#     print(df)
# else:
#     print("No supported PIDs found.")


# import pandas as pd
# import numpy as np
# import obd
# import time
# import os

# # Initialize OBD connection
# obd_connector = "/dev/ttyACM0"  # Replace with your OBD-II port
# connection = obd.Async(obd_connector)

# # Global variables for supported PIDs and DataFrame
# supported_pids_A = []
# supported_pids_B = []
# supported_pids_C = []
# pid_responses = {'PIDS_A': None, 'PIDS_B': None, 'PIDS_C': None}

# # Empty DataFrame for storing OBD data (will populate with supported PIDs later)
# df = pd.DataFrame()

# # Path to store the dataset
# file_path = 'dataset/async_log.csv'

# # Function to map binary strings to supported PIDs
# def map_binary_to_pids(binary_string, start_pid):
#     supported_pids = []
#     for i, bit in enumerate(binary_string):
#         if bit == '1':
#             # Calculate the actual PID number without the 0x prefix
#             pid = start_pid + i
#             supported_pids.append(f"{pid:02X}")
#     return supported_pids

# # Callback function for initial PID discovery
# def pid_callback_initial(response):
#     if not response.is_null():
#         cmd_name = response.command.name
#         pid_responses[cmd_name] = response.value.bits  # Store the binary value

# # Callback function to collect real-time data
# def pid_data_callback(response):
#     global df
#     command_name = response.command.name
#     value = response.value
#     timestamp = time.time()

#     # Add the timestamp and the value to the DataFrame
#     df.loc[len(df), 'Time'] = timestamp
#     df.loc[len(df) - 1, command_name] = value
#     print(f"{command_name}: {value}")

# # Step 1: Discover supported PIDs
# connection.watch(obd.commands.PIDS_A, callback=pid_callback_initial)
# connection.watch(obd.commands.PIDS_B, callback=pid_callback_initial)
# connection.watch(obd.commands.PIDS_C, callback=pid_callback_initial)
# connection.start()

# # Wait for 10 seconds to gather PID data
# time.sleep(10)

# # Stop connection after collecting PID information
# connection.stop()

# # Step 2: Process and store supported PIDs
# if pid_responses['PIDS_A']:
#     supported_pids_A = map_binary_to_pids(pid_responses['PIDS_A'], 0x01)
#     print(f"Supported PIDs (01 - 20): {supported_pids_A}")

# if pid_responses['PIDS_B']:
#     supported_pids_B = map_binary_to_pids(pid_responses['PIDS_B'], 0x21)
#     print(f"Supported PIDs (21 - 40): {supported_pids_B}")

# if pid_responses['PIDS_C']:
#     supported_pids_C = map_binary_to_pids(pid_responses['PIDS_C'], 0x41)
#     print(f"Supported PIDs (41 - 60): {supported_pids_C}")

# # Combine all supported PIDs
# all_supported_pids = supported_pids_A + supported_pids_B + supported_pids_C

# # Step 3: Dynamically build the DataFrame with supported PIDs as columns
# columns = ['Time'] + [obd.commands[1][int(pid, 16)].name for pid in all_supported_pids]
# df = pd.DataFrame(columns=columns)

# # Step 4: Start monitoring and collecting real-time data for supported PIDs
# if all_supported_pids:
#     # Connect again for real-time data collection
#     connection = obd.Async(obd_connector)

#     # Watch all the supported PIDs
#     for pid in all_supported_pids:
#         command = obd.commands[1][int(pid, 16)]
#         connection.watch(command, callback=pid_data_callback)

#     # Start watching the PIDs
#     connection.start()

#     # Collect data for 20 seconds
#     time.sleep(20)

#     # Stop the connection
#     connection.stop()

#     # Save collected data to a CSV file
#     df.to_csv(file_path, mode='a', header=not os.path.exists(file_path))

#     print("Data collection complete. Data saved to CSV.")
#     print(df)
# else:
#     print("No supported PIDs found.")

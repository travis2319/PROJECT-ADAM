import pandas as pd
import obd
import time

# Global variables to store the supported PID values
supported_pids_A = []
supported_pids_B = []
supported_pids_C = []

# List of OBD-II parameters we want to collect
OBD_PARAMETERS = [
    'STATUS', 'FUEL_STATUS', 'ENGINE_LOAD', 'COOLANT_TEMP', 'SHORT_FUEL_TRIM_1',
    'LONG_FUEL_TRIM_1', 'INTAKE_PRESSURE', 'RPM', 'SPEED', 'TIMING_ADVANCE',
    'INTAKE_TEMP', 'THROTTLE_POS', 'O2_SENSORS', 'O2_B1S1', 'O2_B1S2',
    'OBD_COMPLIANCE', 'RUN_TIME', 'PIDS_B', 'DISTANCE_W_MIL', 'EVAPORATIVE_PURGE',
    'WARMUPS_SINCE_DTC_CLEAR', 'DISTANCE_SINCE_DTC_CLEAR', 'BAROMETRIC_PRESSURE',
    'PIDS_C', 'CONTROL_MODULE_VOLTAGE', 'ABSOLUTE_LOAD', 'RELATIVE_THROTTLE_POS',
    'THROTTLE_POS_B', 'ACCELERATOR_POS_D', 'ACCELERATOR_POS_E', 'THROTTLE_ACTUATOR'
]

# Dictionary to store the latest values for each parameter
latest_values = {param: None for param in OBD_PARAMETERS}

df = pd.DataFrame(columns=['Time'] + OBD_PARAMETERS)

# Dictionary to store the PID responses
pid_responses = {
    'PIDS_A': None,
    'PIDS_B': None,
    'PIDS_C': None
}

# Function to map binary strings to supported PIDs
def map_binary_to_pids(binary_string, start_pid):
    supported_pids = []
    for i, bit in enumerate(binary_string):
        if bit == '1':
            # Calculate the actual PID number without the 0x prefix
            pid = start_pid + i
            supported_pids.append(f"{pid:02X}")
    return supported_pids

# Callback function that stores values for PIDS_A, PIDS_B, PIDS_C
def pid_callback_initial(response):
    if not response.is_null():
        cmd_name = response.command.name
        pid_responses[cmd_name] = response.value.bits  # Store the binary value

# Callback function to handle real-time PID values
def pid_callback(response):
    if not response.is_null():
        print(f"{response.command.name}: {response.value}")
        if param_name in latest_values:
            latest_values[param_name] = response.value.magnitude if hasattr(response.value, 'magnitude') else response.value


# Function to dynamically create and watch commands based on supported PIDs
def watch_supported_pids(connection, supported_pids, mode=1):
    for pid in supported_pids:
        # Create the OBD command dynamically (mode 1, PID X)
        command = obd.commands[1][int(pid, 16)]  # Use mode 1 and the PID in hexadecimal
        connection.watch(command, callback=pid_callback)

# Connect to OBD-II interface
obd_connector = "/dev/ttyACM0"  # Replace with your OBD-II port
connection = obd.Async(obd_connector)

# Step 1: Watch PIDS_A, PIDS_B, PIDS_C to determine supported PIDs
connection.watch(obd.commands.PIDS_A, callback=pid_callback_initial)
connection.watch(obd.commands.PIDS_B, callback=pid_callback_initial)
connection.watch(obd.commands.PIDS_C, callback=pid_callback_initial)
connection.start()

# Wait for 10 seconds to gather PID data
time.sleep(10)

# Stop the initial connection
connection.stop()

# Step 2: Process and store the supported PIDs from stored binary strings
if pid_responses['PIDS_A']:
    supported_pids_A = map_binary_to_pids(pid_responses['PIDS_A'], 0x01)
    print(f"Supported PIDs (01 - 20): {supported_pids_A}")

if pid_responses['PIDS_B']:
    supported_pids_B = map_binary_to_pids(pid_responses['PIDS_B'], 0x21)
    print(f"Supported PIDs (21 - 40): {supported_pids_B}")

if pid_responses['PIDS_C']:
    supported_pids_C = map_binary_to_pids(pid_responses['PIDS_C'], 0x41)
    print(f"Supported PIDs (41 - 60): {supported_pids_C}")

# Step 3: Start watching the supported PIDs
if supported_pids_A or supported_pids_B or supported_pids_C:
    # Connect again for the actual data collection
    connection = obd.Async(obd_connector)

    if supported_pids_A:
        watch_supported_pids(connection, supported_pids_A, mode=1)
    if supported_pids_B:
        watch_supported_pids(connection, supported_pids_B, mode=1)
    if supported_pids_C:
        watch_supported_pids(connection, supported_pids_C, mode=1)

    # Start watching the PIDs
    connection.start()

    # Wait for 20 seconds to gather data
    time.sleep(20)

    # Stop the connection
    connection.stop()
else:
    print("No supported PIDs found.")



# import obd
# import time

# # Connect to OBD-II interface
# obd_connector = "/dev/ttyACM0"  # Replace with your OBD-II port
# connection = obd.Async(obd_connector)

# # Global variable to store supported PIDs
# supported_pids = []

# # Function to map binary strings to supported PIDs
# def map_binary_to_pids(binary_string, start_pid):
#     supported_pids = []
#     for i, bit in enumerate(binary_string):
#         if bit == '1':
#             pid = start_pid + i
#             supported_pids.append(f"{pid:02X}")
#     return supported_pids

# # Callback function to store supported PIDs
# def handle_supported_pids(response):
#     if not response.is_null():
#         pids = response.value.bits
#         global supported_pids
#         supported_pids = map_binary_to_pids(pids, 0x01)  # Adjust the starting PID based on mode

# # Function to determine supported PIDs
# def determine_supported_pids():
#     # Watch supported PID commands
#     connection.watch(obd.commands.PIDS_A, callback=handle_supported_pids)
#     connection.watch(obd.commands.PIDS_B, callback=handle_supported_pids)
#     connection.watch(obd.commands.PIDS_C, callback=handle_supported_pids)

#     # Start the connection
#     connection.start()

#     # Wait for a while to receive data
#     time.sleep(10)

#     # Stop the connection
#     connection.stop()

#     # Print the supported PIDs
#     print(f"Supported PIDs: {supported_pids}")

# def query_pids():
#     for pid in supported_pids:
#         # Convert hex PID to decimal
#         pid_decimal = int(pid, 16)

#         # Check if the PID is within the valid range
#         if 0 <= pid_decimal < len(obd.commands[1]):
#             cmd = obd.commands[1][pid_decimal]  # Access command directly

#             if cmd:
#                 response = connection.query(cmd)
#                 print(f"PID {pid}: {response.value}")
#                 time.sleep(0.5)  # Wait for 0.5 seconds between queries
#         else:
#             print(f"PID {pid} is out of range.")

# # Run the process
# determine_supported_pids()
# # query_pids()

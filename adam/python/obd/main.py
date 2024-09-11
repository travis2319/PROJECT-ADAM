import pandas as pd
import numpy as np
import obd
import os
import time

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

# Function to connect to the OBD-II interface
def connect_obd(obd_connector):
    try:
        connection = obd.Async(obd_connector)
        return connection
    except Exception as e:
        print(f"Error connecting to OBD-II: {e}")
        return None

# Function to initialize supported PIDs
def initialize_supported_pids(connection):
    connection.watch(obd.commands.PIDS_A, callback=pid_callback)
    connection.watch(obd.commands.PIDS_B, callback=pid_callback)
    connection.watch(obd.commands.PIDS_C, callback=pid_callback)

    connection.start()
    time.sleep(5)
    connection.stop()

    if pid_responses['PIDS_A']:
        supported_pids.extend(map_binary_to_pids(pid_responses['PIDS_A'], 0x01))
        print(f"Added PIDs (01 - 20)")

    if pid_responses['PIDS_B']:
        supported_pids.extend(map_binary_to_pids(pid_responses['PIDS_B'], 0x21))
        print(f"Added PIDs (21 - 40)")

    if pid_responses['PIDS_C']:
        supported_pids.extend(map_binary_to_pids(pid_responses['PIDS_C'], 0x41))
        print(f"Added PIDs (41 - 60)")

    print(f"All supported PIDs: {supported_pids}")

# Function to get PID names from the supported PIDs
def get_pid_names(supported_pids):
    pid_names = []
    for pid in supported_pids:
        if pid in pid_descriptions:
            pid_names.append(f"{pid_descriptions[pid]}")
        else:
            pid_names.append(f"Unknown")
    print(pid_names)
    return pid_names

# Callback function for handling PID data
def pid_data_callback(response):
    global df
    command_name = response.command.name
    value = response.value.magnitude if hasattr(response.value, 'magnitude') else response.value
    print(command_name, value)

    if command_name == df.columns[1]:  # First element in columns
        # Create a new row with the PID name and value
        new_row = {col: np.nan for col in df.columns}
        new_row['Timestamp'] = time.time() # Add current timestamp
        new_row[command_name] = value
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    else:
        # Update the last row with the current PID value
        if command_name in df.columns:
            df.at[len(df) - 1, command_name] = value
        else:
            print(f"Warning: {command_name} not found in DataFrame columns")

# Main loop function
def main(obd_connector, sleep_interval=30):
    """
    Main loop for continuous data retrieval and storage.

    Parameters:
    - obd_connector: The OBD-II port.
    - sleep_interval: Time (in seconds) to wait between iterations.
    """
    print("Starting OBD-II data collection cycle...")
    connection = connect_obd(obd_connector)
    # Initialize supported PIDs if not already done
    initialize_supported_pids(connection)
    supported_pid_names = get_pid_names(supported_pids)

    # Prepare DataFrame to store PID data
    global df
    df = pd.DataFrame(columns=['Timestamp'] + supported_pid_names)
    try:
        while True:

            if not connection:
                print("Unable to establish connection. Retrying...")
                time.sleep(sleep_interval)
                continue

            if supported_pids:
                for pid in supported_pids:
                    command = obd.commands[1][int(pid, 16)]
                    connection.watch(command, callback=pid_data_callback)

                connection.start()
                time.sleep(25)  # Data collection period
                connection.stop()

                print(df)

                # Save DataFrame to CSV
                file_path = 'dataset/new_data.csv'
                file_exists = os.path.isfile(file_path)
                df.to_csv(file_path, mode='a', index=False, header=not file_exists)
                print(f"DataFrame saved to {file_path}")
            else:
                print("No supported PIDs found.")

            # Wait for a specified time before the next iteration
            print(f"Waiting for {sleep_interval} seconds before the next cycle...")
            time.sleep(sleep_interval)

    except KeyboardInterrupt:
        print("\nData collection stopped by user.")
        if connection:
            connection.stop()  # Ensure the OBD connection is closed
        print("Program terminated.")

if __name__ == "__main__":
    obd_connector = "/dev/pts/2"  # Replace with your actual OBD-II port
    main(obd_connector, sleep_interval=25)  # 30-second interval between cycles

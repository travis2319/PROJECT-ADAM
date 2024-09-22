#!/usr/bin/env python3
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
mid_descriptions={
    '00' : 'MIDS_A',
    '01' :	'MONITOR_O2_B1S1',
    '02' :	'MONITOR_O2_B1S2',
    '03' :	'MONITOR_O2_B1S3',
    '04' :	'MONITOR_O2_B1S4',
    '05' :	'MONITOR_O2_B2S1',
    '06' :	'MONITOR_O2_B2S2',
    '07' :	'MONITOR_O2_B2S3',
    '08' :	'MONITOR_O2_B2S4',
    '09' :	'MONITOR_O2_B3S1',
    '0A' :	'MONITOR_O2_B3S2',
    '0B' :	'MONITOR_O2_B3S3',
    '0C' :	'MONITOR_O2_B3S4',
    '0D' :	'MONITOR_O2_B4S1',
    '0E' :	'MONITOR_O2_B4S2',
    '0F' :	'MONITOR_O2_B4S3',
    '10' :	'MONITOR_O2_B4S4',
    '20' :	'MIDS_B',
    '21' :	'MONITOR_CATALYST_B1',
    '22' :	'MONITOR_CATALYST_B2',
    '23' :	'MONITOR_CATALYST_B3',
    '24' :	'MONITOR_CATALYST_B4',
    '31' :	'MONITOR_EGR_B1',
    '32' :	'MONITOR_EGR_B2',
    '33' :	'MONITOR_EGR_B3',
    '34' : 	'MONITOR_EGR_B4',
    '35' : 	'MONITOR_VVT_B1',
    '36' : 	'MONITOR_VVT_B2',
    '37' : 	'MONITOR_VVT_B3',
    '38' : 	'MONITOR_VVT_B4',
    '39' : 	'MONITOR_EVAP_150',
    '3A' : 	'MONITOR_EVAP_090',
    '3B' : 	'MONITOR_EVAP_040',
    '3C' : 	'MONITOR_EVAP_020',
    '3D' : 	'MONITOR_PURGE_FLOW',
    '40' : 	'MIDS_C',
    '41' : 	'MONITOR_O2_HEATER_B1S1',
    '42' :  'MONITOR_O2_HEATER_B1S2',
    '43' : 	'MONITOR_O2_HEATER_B1S3',
    '44' : 	'MONITOR_O2_HEATER_B1S4',
    '45' : 	'MONITOR_O2_HEATER_B2S1',
    '46' : 	'MONITOR_O2_HEATER_B2S2',
    '47' : 	'MONITOR_O2_HEATER_B2S3',
    '48' : 	'MONITOR_O2_HEATER_B2S4',
    '49' :	'MONITOR_O2_HEATER_B3S1',
    '4A' :	'MONITOR_O2_HEATER_B3S2',
    '4B' :	'MONITOR_O2_HEATER_B3S3',
    '4C' :	'MONITOR_O2_HEATER_B3S4',
    '4D' :	'MONITOR_O2_HEATER_B4S1',
    '4E' :	'MONITOR_O2_HEATER_B4S2',
    '4F' :	'MONITOR_O2_HEATER_B4S3',
    '50' :	'MONITOR_O2_HEATER_B4S4',
    '60' :	'MIDS_D',
    '61' :	'MONITOR_HEATED_CATALYST_B1',
    '62' :	'MONITOR_HEATED_CATALYST_B2',
    '63' :	'MONITOR_HEATED_CATALYST_B3',
    '64' :	'MONITOR_HEATED_CATALYST_B4',
    '71' :	'MONITOR_SECONDARY_AIR_1',
    '72' :	'MONITOR_SECONDARY_AIR_2',
    '73' :	'MONITOR_SECONDARY_AIR_3',
    '74' :	'MONITOR_SECONDARY_AIR_4',
    '80' :	'MIDS_E',
    '81' :	'MONITOR_FUEL_SYSTEM_B1',
    '82' :	'MONITOR_FUEL_SYSTEM_B2',
    '83' :	'MONITOR_FUEL_SYSTEM_B3',
    '84' :	'MONITOR_FUEL_SYSTEM_B4',
    '85' :	'MONITOR_BOOST_PRESSURE_B1',
    '86' :	'MONITOR_BOOST_PRESSURE_B2',
    '90' :	'MONITOR_NOX_ABSORBER_B1',
    '91' :	'MONITOR_NOX_ABSORBER_B2',
    '98' :	'MONITOR_NOX_CATALYST_B1',
    '99' :	'MONITOR_NOX_CATALYST_B2',
    'A0' :	'MIDS_F',
    'A1' :	'MONITOR_MISFIRE_GENERAL',
    'A2' :	'MONITOR_MISFIRE_CYLINDER_1',
    'A3' :	'MONITOR_MISFIRE_CYLINDER_2',
    'A4' :	'MONITOR_MISFIRE_CYLINDER_3',
    'A5' :	'MONITOR_MISFIRE_CYLINDER_4',
    'A6' :	'MONITOR_MISFIRE_CYLINDER_5',
    'A7' :	'MONITOR_MISFIRE_CYLINDER_6',
    'A8' :	'MONITOR_MISFIRE_CYLINDER_7',
    'A9' :	'MONITOR_MISFIRE_CYLINDER_8',
    'AA' : 	'MONITOR_MISFIRE_CYLINDER_9',
    'AB' : 	'MONITOR_MISFIRE_CYLINDER_10',
    'AC' : 	'MONITOR_MISFIRE_CYLINDER_11',
    'AD' : 	'MONITOR_MISFIRE_CYLINDER_12',
    'B0' : 	'MONITOR_PM_FILTER_B1',
    'B1' : 	'MONITOR_PM_FILTER_B2'
}

# Single global variable to store all supported PID values
supported_pids = []
supported_mids=[]

# Function to map binary strings to supported PIDs
def map_binary_to_pids(binary_string, start_pid):
    pids = []
    for i, bit in enumerate(binary_string):
        if bit == '1':
            # Calculate the actual PID number without the 0x prefix
            pid = start_pid + i
            pids.append(f"{pid:02X}")
    return pids

def map_binary_to_mids(binary_string, mid_id):
    print(f"Mapping MIDs for {mid_id:02X}: {binary_string}")
    mid_ranges = {
        0x01: (0x00, 0x20),  # MID_A: 00 - 20
        0x02: (0x21, 0x40),  # MID_B: 21 - 40
        0x03: (0x41, 0x60),  # MID_C: 41 - 60
        0x04: (0x61, 0x80),  # MID_D: 61 - 80
        0x05: (0x81, 0xA0),  # MID_E: 81 - A0
        0x06: (0xA1, 0xC0)   # MID_F: A1 - C0
    }

    start, end = mid_ranges.get(mid_id, (None, None))
    if start is None:
        return []

    hex_mids = []
    for i, bit in enumerate(binary_string):
        if bit == '1':
            mid_value = start + i
            if mid_value <= end:
                hex_mids.append(f"{mid_value:02X}")

    return hex_mids

# Dictionary to store the PID responses
pid_responses = {
    'PIDS_A': None,
    'PIDS_B': None,
    'PIDS_C': None,
}

mid_responses={
    'MIDS_A': None,
    'MIDS_B': None,
    'MIDS_C': None,
    'MIDS_D': None,
    'MIDS_E': None,
    'MIDS_F': None
}

# Function to connect to the OBD-II interface
def async_connection(obd_connector):
    try:
        connection = obd.Async(obd_connector)
        return connection
    except Exception as e:
        print(f"Error connecting to OBD-II: {e}")
        return None

# Function to initialize supported PIDs
def initialize_supported_pids(connection):
    global supported_pids, supported_mids
    # Query for supported PIDs and MIDs
    for cmd_name in ['PIDS_A', 'PIDS_B', 'PIDS_C', 'MIDS_A', 'MIDS_B', 'MIDS_C', 'MIDS_D', 'MIDS_E', 'MIDS_F']:
        response = connection.query(getattr(obd.commands, cmd_name))
        if not response.is_null():
            if cmd_name.startswith('PIDS_'):
                pid_responses[cmd_name] = response.value.bits
                print(f"{cmd_name}: {pid_responses[cmd_name]}")
            elif cmd_name.startswith('MIDS_'):
                mid_responses[cmd_name] = response.value.bits
                print(f"{cmd_name}: {mid_responses[cmd_name]}")

    # Map binary responses to PIDs
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

    # Map binary responses to MIDs
    if mid_responses['MIDS_A']:
        supported_mids.extend(map_binary_to_mids(mid_responses['MIDS_A'], 0x01))
        print(f"Added MIDs (01 - 10): {supported_mids}")
    if mid_responses['MIDS_B']:
        supported_mids.extend(map_binary_to_mids(mid_responses['MIDS_B'], 0x02))
        print(f"Added MIDs (21 - 3D)")
    if mid_responses['MIDS_C']:
        supported_mids.extend(map_binary_to_mids(mid_responses['MIDS_C'], 0x03))
        print(f"Added MIDs (41 - 50)")
    if mid_responses['MIDS_D']:
        supported_mids.extend(map_binary_to_mids(mid_responses['MIDS_D'], 0x04))
        print(f"Added MIDs (61 - 74)")
    if mid_responses['MIDS_E']:
        supported_mids.extend(map_binary_to_mids(mid_responses['MIDS_E'], 0x05))
        print(f"Added MIDs (81 - 99)")
    if mid_responses['MIDS_F']:
        supported_mids.extend(map_binary_to_mids(mid_responses['MIDS_F'], 0x06))
        print(f"Added MIDs (A1 - B1)")
    print(f"All supported MIDs: {supported_mids}")


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
    # print(command_name, value,response.time)
    if hasattr(response.value, 'MIL'):
        print("MIL (Check Engine Light):", response.value.MIL)
    if hasattr(response.value, 'DTC_count'):
        print("DTC Count:", response.value.DTC_count)
    if hasattr(response.value, 'ignition_type'):
        print("Ignition Type:", response.value.ignition_type)

    if command_name == df.columns[1]:  # First element in columns
        # Create a new row with the PID name and value
        new_row = {col: np.nan for col in df.columns}
        new_row['Timestamp'] = response.time # Add current timestamp
        new_row[command_name] = value
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    else:
        # Update the last row with the current PID value
        if command_name == df.columns[27]:
            print(df.iloc[-1])
        if not df.empty and command_name in df.columns:
                    df.at[len(df) - 1, command_name] = value
        else:
            print(f"Warning: {command_name} not found in DataFrame columns")

# Main loop function
def main(obd_connector, sleep_interval=30):
    print("Starting OBD-II data collection cycle...")
    connection = obd.OBD(obd_connector) # auto-connects to USB or RF port
    # Initialize supported PIDs if not already done
    initialize_supported_pids(connection)
    supported_pid_names = get_pid_names(supported_pids)

    connection = async_connection(obd_connector)
    # Prepare DataFrame to store PID data
    global df
    df = pd.DataFrame(columns=['Timestamp'] + supported_pid_names)
    try:
        while True:

            if not connection:
                print("Unable to establish connection. Retrying...")
                time.sleep(sleep_interval)
                continue

            if supported_pid_names:
                for pid in supported_pid_names:
                    # command = obd.commands[1][int(pid, 16)]
                    # connection.watch(command, callback=pid_data_callback)
                    command = getattr(obd.commands, pid, None)
                    if command:
                        connection.watch(command, callback=pid_data_callback)
                    else:
                        print(f"Command {pid} is not supported.")

                connection.start()
                time.sleep(25)  # Data collection period
                connection.stop()

                print(df)

                # Save DataFrame to CSV
                file_path = 'dataset/test8.csv'
                file_exists = os.path.isfile(file_path)
                df.to_csv(file_path, mode='a', index=False, header=not file_exists)
                print(f"DataFrame saved to {file_path}")
                df = df[0:0]
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
    # obd_connector = "/dev/pts/2/  # Replace with your actual OBD-II port
    obd_connector="/dev/ttyACM0"
    main(obd_connector, sleep_interval=10)  # 30-second interval between cycles

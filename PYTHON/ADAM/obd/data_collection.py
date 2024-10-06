import obd
import pandas as pd
import numpy as np
from .pid_mapping import pid_descriptions, mid_descriptions, map_binary_to_pids, map_binary_to_mids

supported_pids = []
supported_mids = []
df = pd.DataFrame()

def initialize_supported_pids(connection):
    global supported_pids, supported_mids
    pid_responses = {'PIDS_A': None, 'PIDS_B': None, 'PIDS_C': None}
    mid_responses = {'MIDS_A': None, 'MIDS_B': None, 'MIDS_C': None, 'MIDS_D': None, 'MIDS_E': None, 'MIDS_F': None}

    # Query for supported PIDs and MIDs
    for cmd_name in ['PIDS_A', 'PIDS_B', 'PIDS_C', 'MIDS_A', 'MIDS_B', 'MIDS_C', 'MIDS_D', 'MIDS_E', 'MIDS_F']:
        response = connection.query(getattr(obd.commands, cmd_name))
        if not response.is_null():
            if cmd_name.startswith('PIDS_'):
                pid_responses[cmd_name] = response.value.bits
            elif cmd_name.startswith('MIDS_'):
                mid_responses[cmd_name] = response.value.bits

    # Map binary responses to PIDs and MIDs
    for pid_name, response in pid_responses.items():
        if response:
            start_pid = int(pid_name[-1], 16) * 0x20 + 1
            supported_pids.extend(map_binary_to_pids(response, start_pid))

    for mid_name, response in mid_responses.items():
        if response:
            mid_id = ord(mid_name[-1]) - ord('A') + 1
            supported_mids.extend(map_binary_to_mids(response, mid_id))

    print(f"All supported PIDs: {supported_pids}")
    print(f"All supported MIDs: {supported_mids}")

def get_pid_names(supported_pids):
    return [pid_descriptions.get(pid, "Unknown") for pid in supported_pids]

def pid_data_callback(response):
    global df
    command_name = response.command.name
    value = response.value.magnitude if hasattr(response.value, 'magnitude') else response.value

    if command_name == df.columns[1]:
        new_row = {col: np.nan for col in df.columns}
        new_row['Timestamp'] = response.time
        new_row[command_name] = value
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    else:
        if not df.empty and command_name in df.columns:
            df.at[len(df) - 1, command_name] = value
        else:
            print(f"Warning: {command_name} not found in DataFrame columns")

def collect_data(connection):
    global df
    supported_pid_names = get_pid_names(supported_pids)
    df = pd.DataFrame(columns=['Timestamp'] + supported_pid_names)

    for pid in supported_pid_names:
        command = getattr(obd.commands, pid, None)
        if command:
            connection.watch(command, callback=pid_data_callback)
        else:
            print(f"Command {pid} is not supported.")

    connection.start()
    time.sleep(25)  # Data collection period
    connection.stop()

    return df
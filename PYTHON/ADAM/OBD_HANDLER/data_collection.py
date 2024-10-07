import pandas as pd
import numpy as np
import obd
from .utils import df

def pid_data_callback(response):
    global df
    command_name = response.command.name
    value = response.value.magnitude if hasattr(response.value, 'magnitude') else response.value

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

def setup_data_collection(connection, supported_pid_names):
    global df
    df = pd.DataFrame(columns=['Timestamp'] + supported_pid_names)
    for pid in supported_pid_names:
        command = getattr(obd.commands, pid, None)
        if command:
            connection.watch(command, callback=pid_data_callback)
        else:
            print(f"Command {pid} is not supported.")
    return df

def start_data_collection(connection, duration):
    connection.start()
    import time
    time.sleep(duration)
    connection.stop()
    return df  # Return the DataFrame after collection
import pandas as pd
import numpy as np
import obd
from .utils import df  # Note: Importing df from utils might cause issues

# Global variable
df = None  # It's better to initialize this here

def pid_data_callback(response):
    global df
    command_name = response.command.name
    value = response.value.magnitude if hasattr(response.value, 'magnitude') else response.value

    # Special attribute handling
    attributes_to_check = {
        'MIL': 'Check Engine Light',
        'DTC_count': 'DTC Count',
        'ignition_type': 'Ignition Type'
    }

    for attr, display_name in attributes_to_check.items():
        if hasattr(response.value, attr):
            print(f"{display_name}:", getattr(response.value, attr))

    if command_name == df.columns[1]:  # First PID in columns
        # Create a new row
        new_row = {col: np.nan for col in df.columns}
        new_row['Timestamp_OBD'] = response.time
        new_row[command_name] = value
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    else:
        # Update existing row
        if len(df.columns) > 27 and command_name == df.columns[27]:
            print(df.iloc[-1])
        if not df.empty and command_name in df.columns:
            df.at[len(df) - 1, command_name] = value
        else:
            print(f"Warning: {command_name} not found in DataFrame columns")

def setup_data_collection(connection, supported_pid_names):
    global df
    df = pd.DataFrame(columns=['Timestamp_OBD'] + supported_pid_names)

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
    return df

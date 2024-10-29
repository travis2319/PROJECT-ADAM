# import pandas as pd
# import numpy as np
# import obd
# import time
# import os
# from datetime import date

# # Initialize connection
# connection = obd.Async('/dev/ttyACM0')
# # connection = obd.Async('/dev/pts/2')

# # Define DataFrame
# df = pd.DataFrame(columns=[
#     "Start_Time",
#     "SPEED",
#     "Engine Load",
#     "Coolant Temp",
#     "MAF",
#     "Timing Advance",
#     #"Short Trim B1",
#     #"Long Trim B1",
#     "Throttle_pos",
#     "End_Time"
# ])

# def generic_callback(responses):
#     global df
#     command_name = responses.command.name
#     value = responses.value

#     if command_name == "SPEED":
#         start_timestamp = time.time()
#         df.loc[len(df)] = [
#             start_timestamp,
#             value,
#             np.nan,
#             np.nan,
#             np.nan,
#             np.nan,
#             np.nan,
#             np.nan,
#             np.nan,
#             np.nan
#             ]
#         print(f"Speed: {value}")
#     else:
#         if command_name == "THROTTLE_POS":
#             end_timestamp = time.time()
#             df.loc[len(df) - 1, "End_Time"] = end_timestamp
#         df.loc[len(df) - 1, command_name] = value
#         print(f"{command_name}: {value}")

# # Watch commands
# commands_to_watch = {
#     obd.commands.SPEED: "SPEED",
#     obd.commands.COOLANT_TEMP: "Coolant Temp",
#     obd.commands.ENGINE_LOAD: "Engine Load",
#     obd.commands.TIMING_ADVANCE: "Timing Advance",
#     obd.commands.SHORT_O2_TRIM_B1: "Short Trim B1",
#     obd.commands.LONG_O2_TRIM_B1: "Long Trim B1",
#     obd.commands.MAF: "MAF",
#     obd.commands.THROTTLE_POS: "Throttle_pos"
# }

# for command, column_name in commands_to_watch.items():
#     connection.watch(command, callback=generic_callback)

# # Function to check if a file exists in the folder
# def file_exists_in_folder(folder_path, file_name):
#     file_path = os.path.join(folder_path, file_name)
#     return os.path.exists(file_path)

# # Function to upload the file (placeholder, you'll need to implement this)
# def upload_file(file_path):
#     # Replace this with your actual upload logic
#     print(f"Uploading file: {file_path}")

# # Send all files in the folder first
# folder_path = 'dataset'
# for file_name in os.listdir(folder_path):
#     file_path = os.path.join(folder_path, file_name)
#     if os.path.isfile(file_path):
#         upload_file(file_path)

# # Start connection (data logging starts here)
# connection.start()

# # Run for a period of time
# time.sleep(20)

# # Stop connection
# connection.stop()

# # Save to CSV
# today = date.today().strftime("%Y-%m-%d")
# file_name = f'log_{today}.csv'
# file_path = os.path.join(folder_path, file_name)
# df.to_csv(file_path, mode='a', header=not os.path.exists(file_path))

# print(df)

# import pandas as pd
# import numpy as np
# import obd
# import time
# import datetime
# import os

# # Initialize connection
# # connection = obd.Async('/dev/ttyACM0')
# connection = obd.Async('/dev/pts/2')

# # var pids = []string{
# # 	"010C", // RPM-
# # 	"010D", // Speed
# # 	"0104", // Engine Load
# # 	"0105", // Coolant Temperature
# # 	"010F", // Intake Air Temperature
# # 	"0110", // Mass Airflow
# # 	"0107", // Fuel Trim 1
# # 	"0108", // Fuel Trim 2
# # 	"0111", // Throttle Position
# # 	"0100", // Supported PIDs
# # }

# # Define DataFrame with correct column names
# df = pd.DataFrame(columns=[
#     "Start_Time", "SPEED", "Engine Load", "Coolant Temp", "MAF",  "Timing Advance",
#     "Short Trim B1", "Long Trim B1", "Throttle_pos", "End_Time"
# ])

# def new_rpm(responses):
#     start_timestamp = time.time()
#     speed = responses.value
#     print(f"Speed: {speed}")
#     df.loc[len(df)] = [start_timestamp, speed, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]

# def coolant_temp(responses):
#     temp = responses.value
#     print(f"Coolant Temp: {temp}")
#     df.loc[len(df) - 1, "Coolant Temp"] = temp

# def engine_load(responses):
#     load = responses.value
#     print(f"Engine Load: {load}")
#     df.loc[len(df) - 1, "Engine Load"] = load

# def timing_advance(responses):
#     advance = responses.value
#     print(f"Timing Advance: {advance}")
#     df.loc[len(df) - 1, "Timing Advance"] = advance

# def short_trim_b1(responses):
#     trim = responses.value
#     print(f"Short Trim B1: {trim}")
#     df.loc[len(df) - 1, "Short Trim B1"] = trim

# def long_trim_b1(responses):
#     trim = responses.value
#     print(f"Long Trim B1: {trim}")
#     df.loc[len(df) - 1, "Long Trim B1"] = trim

# def maf(responses):
#     maf_value = responses.value
#     print(f"MAF: {maf_value}")
#     df.loc[len(df) - 1, "MAF"] = maf_value

# def throttle_pos(responses):
#     end_timestamp = time.time()
#     throttle = responses.value
#     print(f"Throttle Position: {throttle}")
#     df.loc[len(df) - 1, "Throttle_pos"] = throttle
#     df.loc[len(df) - 1, "End_Time"] = end_timestamp

# # Watch commands
# connection.watch(obd.commands.SPEED, callback=new_rpm)
# connection.watch(obd.commands.COOLANT_TEMP, callback=coolant_temp)
# connection.watch(obd.commands.ENGINE_LOAD, callback=engine_load)
# connection.watch(obd.commands.TIMING_ADVANCE, callback=timing_advance)
# connection.watch(obd.commands.SHORT_O2_TRIM_B1, callback=short_trim_b1)
# connection.watch(obd.commands.LONG_O2_TRIM_B1, callback=long_trim_b1)
# connection.watch(obd.commands.MAF, callback=maf)
# connection.watch(obd.commands.THROTTLE_POS, callback=throttle_pos)

# # Start connection
# connection.start()

# # Run for a period of time
# time.sleep(20)

# # Stop connection
# connection.stop()

# # Define the file path
# file_path = 'async_log_real.csv'

# # Save to CSV
# df.to_csv(file_path, mode='a', header=not os.path.exists(file_path))

# print(df)

import pandas as pd
import numpy as np
import obd
import time
import os

# Initialize connection
connection = obd.Async('/dev/ttyACM0')

# Define DataFrame
df = pd.DataFrame(columns=[
    "Start_Time",
    "SPEED",
    "Engine Load",
    "Coolant Temp",
    "MAF",
    "Timing Advance",
    "Short Trim B1",
    "Long Trim B1",
    "Throttle_pos",
    "End_Time"
])

def generic_callback(responses):
    global df
    command_name = responses.command.name
    value = responses.value

    if command_name == "SPEED":
        start_timestamp = time.time()
        df.loc[len(df)] = [
            start_timestamp,
            value,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan
            ]
        print(f"Speed: {value}")
    else:
        if command_name == "THROTTLE_POS":
            end_timestamp = time.time()
            df.loc[len(df) - 1, "End_Time"] = end_timestamp
        df.loc[len(df) - 1, command_name] = value
        print(f"{command_name}: {value}")

# Watch commands
commands_to_watch = {
    obd.commands.SPEED: "SPEED",
    obd.commands.COOLANT_TEMP: "Coolant Temp",
    obd.commands.ENGINE_LOAD: "Engine Load",
    obd.commands.TIMING_ADVANCE: "Timing Advance",
    obd.commands.SHORT_O2_TRIM_B1: "Short Trim B1",
    obd.commands.LONG_O2_TRIM_B1: "Long Trim B1",
    obd.commands.MAF: "MAF",
    obd.commands.THROTTLE_POS: "Throttle_pos"
}

for command, column_name in commands_to_watch.items():
    connection.watch(command, callback=generic_callback)

# Start connection
connection.start()

# Run for a period of time
time.sleep(20)

# Stop connection
connection.stop()

# Save to CSV
file_path = '/dataset/async_log.csv'
df.to_csv(file_path, mode='a', header=not os.path.exists(file_path))

print(df)

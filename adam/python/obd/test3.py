import pandas as pd
import numpy as np
import obd
import time
import datetime
import os

# Initialize connection
connection = obd.Async('/dev/ttyACM0')

# Define DataFrame with correct column names
df = pd.DataFrame(columns=[
    "Start_Time", "SPEED", "Coolant Temp", "Engine Load", "Timing Advance",
    "Short Trim B1", "Long Trim B1", "MAF", "Throttle_pos", "End_Time"
])

def new_rpm(responses):
    start_timestamp = time.time()
    speed = responses.value
    print(f"Speed: {speed}")
    df.loc[len(df)] = [start_timestamp, speed, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]

def coolant_temp(responses):
    temp = responses.value
    print(f"Coolant Temp: {temp}")
    df.loc[len(df) - 1, "Coolant Temp"] = temp

def engine_load(responses):
    load = responses.value
    print(f"Engine Load: {load}")
    df.loc[len(df) - 1, "Engine Load"] = load

def timing_advance(responses):
    advance = responses.value
    print(f"Timing Advance: {advance}")
    df.loc[len(df) - 1, "Timing Advance"] = advance

def short_trim_b1(responses):
    trim = responses.value
    print(f"Short Trim B1: {trim}")
    df.loc[len(df) - 1, "Short Trim B1"] = trim

def long_trim_b1(responses):
    trim = responses.value
    print(f"Long Trim B1: {trim}")
    df.loc[len(df) - 1, "Long Trim B1"] = trim

def maf(responses):
    maf_value = responses.value
    print(f"MAF: {maf_value}")
    df.loc[len(df) - 1, "MAF"] = maf_value

def throttle_pos(responses):
    end_timestamp = time.time()
    throttle = responses.value
    print(f"Throttle Position: {throttle}")
    df.loc[len(df) - 1, "Throttle_pos"] = throttle
    df.loc[len(df) - 1, "End_Time"] = end_timestamp

# Watch commands
connection.watch(obd.commands.SPEED, callback=new_rpm)
connection.watch(obd.commands.COOLANT_TEMP, callback=coolant_temp)
connection.watch(obd.commands.ENGINE_LOAD, callback=engine_load)
connection.watch(obd.commands.TIMING_ADVANCE, callback=timing_advance)
connection.watch(obd.commands.SHORT_O2_TRIM_B1, callback=short_trim_b1)
connection.watch(obd.commands.LONG_O2_TRIM_B1, callback=long_trim_b1)
connection.watch(obd.commands.MAF, callback=maf)
connection.watch(obd.commands.THROTTLE_POS, callback=throttle_pos)

# Start connection
connection.start()

# Run for a period of time
time.sleep(20)

# Stop connection
connection.stop()

# Define the file path
file_path = 'async_log.csv'

# Save to CSV
df.to_csv(file_path, mode='a', header=not os.path.exists(file_path))

print(df)

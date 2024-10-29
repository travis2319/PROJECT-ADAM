import pandas as pd
import numpy as np
import matplotlib
import obd
import time
import datetime
import requests

connection = obd.Async('/dev/ttyACM0')
df = pd.DataFrame(columns=["Start_Time", "SPEED", "Coolant Temp", "Engine Load", "Throttle_pos_b", "End_Time"])

def new_rpm(responses):
    start_timestamp = time.time()
    speed = responses.value
    print(speed)
    df.loc[len(df)] = [start_timestamp, speed, np.nan, np.nan, np.nan, np.nan]

def coolant_temp(responses):
    temp = responses.value
    print(temp)
    df.loc[len(df) - 1, "Coolant Temp"] = temp

def engine_load(responses):
    load = responses.value
    print(load)
    df.loc[len(df) - 1, "Engine Load"] = load

def throttle_pos(responses):
    end_timestamp = time.time()
    throttle = responses.value
    print(throttle)
    df.loc[len(df) - 1, "Throttle_pos_b"] = throttle
    df.loc[len(df) - 1, "End_Time"] = end_timestamp

connection.watch(obd.commands.SPEED, callback=new_rpm)
connection.watch(obd.commands.COOLANT_TEMP, callback=coolant_temp)
connection.watch(obd.commands.ENGINE_LOAD, callback=engine_load)
connection.watch(obd.commands.THROTTLE_POS_B, callback=throttle_pos)
connection.start()

time.sleep(20)
connection.stop()

print(df)
df.to_csv('async_log.csv', mode='a')


# The base URL of your Google Apps Script web app
base_url = "https://script.google.com/macros/s/AKfycbwVR6GLTTL99a4dFJazRhK-0fBl9YMY6kkyGrdJoYbXsVs_bp8xJo_tQgKcxvoMO46CLw/exec"

# Loop through each row in the DataFrame
for index, row in df.iterrows():
    # Extract values from the current row
    speed = row["SPEED"]
    coolant_temp = row["Coolant Temp"]
    engine_load = row["Engine Load"]

    # Construct the full URL with query parameters
    full_url = f"{base_url}?value1={coolant_temp}&value2={speed}&value3={engine_load}"

    # Send the GET request
    response = requests.get(full_url)

    # Check if the request was successful
    if response.status_code == 200:
        print(f"Data for row {index + 1} successfully sent to Google Sheets")
    else:
        print(f"Failed to send data for row {index + 1}. Status code: {response.status_code}")
        print(f"Response content: {response.text}")

print("All data sent. DataFrame contents:")
print(df)


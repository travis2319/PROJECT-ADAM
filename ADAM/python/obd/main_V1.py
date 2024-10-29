import pandas as pd
#import numpy as np
import obd
import time
import requests
from obd import OBDStatus
import os
import logging

# # Set up logging
# log_dir = os.path.join(os.path.dirname(__file__), 'logs')
# if not os.path.exists(log_dir):
#     os.makedirs(log_dir)
# log_file = os.path.join(log_dir, 'app.log')

# Set up logging
# Assuming the logs folder is one level up from the blackbox folder
#log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
#log_file = os.path.join(log_dir, 'app.log')

#logging.basicConfig(filename=log_file, level=logging.INFO,
#                    format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize DataFrame
def initialize_dataframe():
    return pd.DataFrame(columns=["Start_Time", "SPEED", "Coolant Temp", "Engine Load", "Throttle_pos_b", "End_Time"])

# Callback functions
def new_rpm(responses):
    start_timestamp = time.time()
    speed = responses.value if responses.value is not None else 0
    logging.info(f"Speed: {speed}")
    df.loc[len(df)] = [start_timestamp, speed, np.nan, np.nan, np.nan, np.nan]

def coolant_temp(responses):
    temp = responses.value if responses.value is not None else 0
    logging.info(f"Coolant Temp: {temp}")
    df.loc[len(df) - 1, "Coolant Temp"] = temp

def engine_load(responses):
    load = responses.value if responses.value is not None else 0
    logging.info(f"Engine Load: {load}")
    df.loc[len(df) - 1, "Engine Load"] = load

def throttle_pos(responses):
    end_timestamp = time.time()
    throttle = responses.value if responses.value is not None else 0
    logging.info(f"Throttle Position: {throttle}")
    df.loc[len(df) - 1, "Throttle_pos_b"] = throttle
    df.loc[len(df) - 1, "End_Time"] = end_timestamp

# OBD connection setup
def setup_obd_connection():
    obd_connector = "/dev/ttyACM0"
    logging.info(f"OBD Connector: {obd_connector}")
    connection = obd.Async(obd_connector)
    logging.info("OBD connector working in setup_obd_connection function")
    return connection

# Watch OBD commands
def watch_obd_commands(connection):
    connection.watch(obd.commands.SPEED, callback=new_rpm)
    connection.watch(obd.commands.COOLANT_TEMP, callback=coolant_temp)
    connection.watch(obd.commands.ENGINE_LOAD, callback=engine_load)
    connection.watch(obd.commands.THROTTLE_POS_B, callback=throttle_pos)

# Run OBD connection
def run_obd_connection(connection):
    connection.start()
    time.sleep(20)
    connection.stop()

# Save data to CSV
def save_to_csv(df):
    file_exists = os.path.isfile('async_log.csv')
    df.to_csv('async_log.csv', mode='a', header=not file_exists, index=False)
    logging.info("Data saved to CSV")

# Send data to Google Sheets
def send_to_google_sheets(df):
    base_url = "https://script.google.com/macros/s/AKfycbwVR6GLTTL99a4dFJazRhK-0fBl9YMY6kkyGrdJoYbXsVs_bp8xJo_tQgKcxvoMO46CLw/exec"

    for index, row in df.iterrows():
        speed = row["SPEED"]
        coolant_temp = row["Coolant Temp"]
        engine_load = row["Engine Load"]

        full_url = f"{base_url}?value1={coolant_temp}&value2={speed}&value3={engine_load}"

        response = requests.get(full_url)

        if response.status_code == 200:
            logging.info(f"Data for row {index + 1} successfully sent to Google Sheets")
        else:
            logging.error(f"Failed to send data for row {index + 1}. Status code: {response.status_code}")
            logging.error(f"Response content: {response.text}")

    logging.info("All data sent. DataFrame contents:")
    logging.info(df)

def main():
    global df
    df = initialize_dataframe()
    connection = setup_obd_connection()
    #logging.info(f"NOT_CONNECTED: {connection.status() == OBDStatus.NOT_CONNECTED}")
    #logging.info(f"OBD_CONNECTED: {connection.status() == OBDStatus.OBD_CONNECTED}")
    #logging.info(f"CAR_CONNECTED: {connection.status() == OBDStatus.CAR_CONNECTED}")
    if(connection.status() == OBDStatus.CAR_CONNECTED):
        #logging.info("Car connected!!")
        print("car connected")
        watch_obd_commands(connection)
        run_obd_connection(connection)
        save_to_csv(df)
        send_to_google_sheets(df)
    else:
        #logging.warning("Not connected!!")
        print("not connected")
        
if __name__ == "__main__" :
    main()


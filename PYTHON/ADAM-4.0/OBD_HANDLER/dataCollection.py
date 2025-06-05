#OBD_HANDLER/dataCollection.py
from datetime import datetime
import obd  # type: ignore
import pandas as pd # type: ignore

def setup_data_collection(conn, sensor_file):
    try:
        with open(sensor_file, "r") as file:
            sensors = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"{sensor_file} not found.")
        return None
    if not sensors:
        print("No sensors found in the file.")
        return None
        
    # Identify the first sensor from the list
    first_sensor = sensors[0]
    
    # Dictionary to store sensor data including timestamp
    sensor_data = {sensor: [] for sensor in sensors}
    sensor_data['TIMESTAMP_OBD'] = []  # Add timestamp column

    # Callback function to store data with timestamp
    def callback(r, sensor):
        print(sensor, r)
        if r is not None:
            sensor_data[sensor].append(r.value)
            # Add timestamp only when processing the first sensor to avoid duplicates
            if sensor == first_sensor:
                sensor_data['TIMESTAMP_OBD'].append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        else:
            sensor_data[sensor].append(None)
            # Add timestamp even if reading failed for first sensor
            if sensor == first_sensor:
                sensor_data['TIMESTAMP_OBD'].append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            print(f"Failed to read {sensor}")

    # Send the sensor commands to the OBD-II adapter
    for sensor in sensors:
        conn.watch(obd.commands[sensor], callback=lambda r, sensor=sensor: callback(r, sensor))
    
    return sensor_data

def start_data_collection(connection, duration, sensor_file):
    sensor_data = setup_data_collection(connection, sensor_file)
    if sensor_data is None:
        return None
    
    connection.start()
    import time
    time.sleep(duration)
    connection.stop()
    
    # Convert the sensor data dictionary to a DataFrame
    df = pd.DataFrame(sensor_data)
    return df
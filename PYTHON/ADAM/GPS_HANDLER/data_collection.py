import pandas as pd
import time
import re

def read_gps_data(ser):
    if ser.in_waiting > 0:
        data = ser.readline().decode('utf-8', errors='ignore').strip()
        return data
    return None

def parse_gps_data(gps_raw_data):
    match = re.search(r'Location:\s*([-\d.]+),\s*([-\d.]+)', gps_raw_data)
    if match:
        lat = match.group(1)
        lon = match.group(2)
        return lat, lon
    return None, None

def collect_gps_data(ser, duration):
    df = pd.DataFrame(columns=['Timestamp', 'Latitude', 'Longitude'])
    end_time = time.time() + duration

    while time.time() < end_time:
        gps_raw_data = read_gps_data(ser)
        if gps_raw_data:
            lat, lon = parse_gps_data(gps_raw_data)
            if lat and lon:
                new_row = pd.DataFrame({
                    'Timestamp': [time.time()],
                    'Latitude': [lat],
                    'Longitude': [lon]
                })
                df = pd.concat([df, new_row], ignore_index=True)
        time.sleep(0.1)  # Read every 0.5 seconds

    return df

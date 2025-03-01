import serial
import re
import pandas as pd
from datetime import datetime

def read_data(ser):
    if ser and ser.in_waiting > 0:
        return ser.readline().decode('utf-8', errors='ignore').strip()
    return None

def parse_data(raw_data):
    gps_status = "No Signal" if "No GPS Signal" in raw_data else "Signal Acquired"
    
    gps_match = re.search(r"GPS: Lat: ([0-9.-]+) Lon: ([0-9.-]+)", raw_data)
    latitude, longitude = map(float, gps_match.groups()) if gps_match else (None, None)
    
    accel_match = re.search(r"ACC \(m/s²\) X:\s*([-0-9.]+) Y:\s*([-0-9.]+) Z:\s*([-0-9.]+)", raw_data)
    acc_x, acc_y, acc_z = map(float, accel_match.groups()) if accel_match else (None, None, None)
    
    gyro_match = re.search(r"GYRO \(°/s\) X:\s*([-0-9.]+) Y:\s*([-0-9.]+) Z:\s*([-0-9.]+)", raw_data)
    gyro_x, gyro_y, gyro_z = map(float, gyro_match.groups()) if gyro_match else (None, None, None)
    
    vibration_match = re.search(r"VIBRATION:\s*(DETECTED|NO)", raw_data)
    vibration_status = vibration_match.group(1) if vibration_match else None
    
    return {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "GPS_Status": gps_status,
        "Latitude": latitude,
        "Longitude": longitude,
        "Acc_X": acc_x,
        "Acc_Y": acc_y,
        "Acc_Z": acc_z,
        "Gyro_X": gyro_x,
        "Gyro_Y": gyro_y,
        "Gyro_Z": gyro_z,
        "Vibration_Status": vibration_status
    }

def collect_data(ser, duration, output_file="sensor_data.csv"):
    df = pd.DataFrame(columns=["Timestamp", "GPS_Status", "Latitude", "Longitude", "Acc_X", "Acc_Y", "Acc_Z",
                               "Gyro_X", "Gyro_Y", "Gyro_Z", "Vibration_Status"])
    end_time = datetime.now().timestamp() + duration
    
    while datetime.now().timestamp() < end_time:
        raw_data = read_data(ser)
        if raw_data:
            parsed_data = parse_data(raw_data)
            new_row = pd.DataFrame([parsed_data])
            df = pd.concat([df, new_row], ignore_index=True)
            
            df.to_csv(output_file, mode='a', header=not pd.io.common.file_exists(output_file), index=False)
    
    return df
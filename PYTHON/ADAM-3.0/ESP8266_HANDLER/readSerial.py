import pandas as pd # type: ignore
from datetime import datetime
import re

def read_serial(conn):
    data_list = []  # Store data before writing to DataFrame
    for _ in range(2):  # Read two lines
        try:
            line = conn.readline().decode('utf-8', errors='ignore').strip()
            if line:
                print(line)  # Debugging: print raw data

                # Extract GPS status
                gps_status = "No Signal" if "No GPS Signal" in line else "Signal Acquired"

                # Extract latitude & longitude if available
                gps_match = re.search(r"\[GPS\] Lat: ([0-9.-]+), Lon: ([0-9.-]+)", line)
                if gps_match:
                    latitude, longitude = map(float, gps_match.groups())
                else:
                    latitude, longitude = None, None

                # Extract accelerometer values
                accel_match = re.search(r"ACC \(m/s²\) X:\s*([-0-9.]+) Y:\s*([-0-9.]+) Z:\s*([-0-9.]+)", line)
                acc_x, acc_y, acc_z = map(float, accel_match.groups()) if accel_match else (None, None, None)

                # Extract gyroscope values
                gyro_match = re.search(r"GYRO \(°/s\) X:\s*([-0-9.]+) Y:\s*([-0-9.]+) Z:\s*([-0-9.]+)", line)
                gyro_x, gyro_y, gyro_z = map(float, gyro_match.groups()) if gyro_match else (None, None, None)

                # Extract vibration status
                vibration_match = re.search(r"VIBRATION:\s*(DETECTED|NO)", line)
                vibration_status = vibration_match.group(1) if vibration_match else None

                # Get timestamp
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                data_list.append([timestamp, gps_status, latitude, longitude, acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z, vibration_status])
            
            else:
                print("No data received.")
                return None
        except Exception as e:
            print(f"Error reading serial data: {e}")
            return None

    df = pd.DataFrame(data_list, columns=["Timestamp", "GPS_Status", "Latitude", "Longitude", "Acc_X", "Acc_Y", "Acc_Z",
                                        "Gyro_X", "Gyro_Y", "Gyro_Z", "Vibration_Status"])
    return df


# #ESP8266_HANDLER/readSerial.py
# import pandas as pd # type: ignore
# from datetime import datetime
# import re

# def read_serial(conn):
#     data_list = []  # Store data before writing to DataFrame
#     try:
#         line = conn.readline().decode('utf-8', errors='ignore').strip()
#         if line:
#             print(line)  # Debugging: print raw data

#             # Extract GPS status
#             gps_status = "No Signal" if "No GPS Signal" in line else "Signal Acquired"

#             # Extract latitude & longitude if available
#             gps_match = re.search(r"\[GPS\] Lat: ([0-9.-]+), Lon: ([0-9.-]+)", line)
#             if gps_match:
#                 latitude, longitude = map(float, gps_match.groups())
#             else:
#                 latitude, longitude = None, None

#             # Extract accelerometer values
#             accel_match = re.search(r"ACC \(m/s²\) X:\s*([-0-9.]+) Y:\s*([-0-9.]+) Z:\s*([-0-9.]+)", line)
#             acc_x, acc_y, acc_z = map(float, accel_match.groups()) if accel_match else (None, None, None)

#             # Extract gyroscope values
#             gyro_match = re.search(r"GYRO \(°/s\) X:\s*([-0-9.]+) Y:\s*([-0-9.]+) Z:\s*([-0-9.]+)", line)
#             gyro_x, gyro_y, gyro_z = map(float, gyro_match.groups()) if gyro_match else (None, None, None)

#             # Extract vibration status
#             vibration_match = re.search(r"VIBRATION:\s*(DETECTED|NO)", line)
#             vibration_status = vibration_match.group(1) if vibration_match else None

#             # Get timestamp
#             timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
#             data_list.append([timestamp, gps_status, latitude, longitude, acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z, vibration_status])
            
#             df = pd.DataFrame(data_list, columns=["Timestamp", "GPS_Status", "Latitude", "Longitude", "Acc_X", "Acc_Y", "Acc_Z",
#                                         "Gyro_X", "Gyro_Y", "Gyro_Z", "Vibration_Status"])
#             return df

#     except Exception as e:
#         print(f"Error reading serial data: {e}")
#         return None
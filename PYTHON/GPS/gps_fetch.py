import serial
import time
import re

# COM7 and baud rate setup (adjust as needed)
port = 'COM7'
baud_rate = 115200  # Match the baud rate of the NodeMCU
timeout = 1         # Timeout in seconds

# Initialize serial connection
ser = serial.Serial(port, baud_rate, timeout=timeout)

def read_gps_data():
    # Read data from the serial port
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            return data

def extract_coordinates(gps_data):
    # Regular expression to match the location format
    match = re.search(r'Location:\s*([-\d.]+),\s*([-\d.]+)', gps_data)
    if match:
        lat = match.group(1)
        lon = match.group(2)
        return lat, lon
    return None, None

try:
    print("Reading GPS data from NodeMCU...")
    while True:
        gps_raw_data = read_gps_data()
        lat, lon = extract_coordinates(gps_raw_data)
        if lat and lon:
            print(f"Latitude: {lat}, Longitude: {lon}")
        else:
            print("Invalid GPS data received.")

        time.sleep(5)  # 5-second interval
except KeyboardInterrupt:
    print("GPS reading stopped.")
finally:
    if ser.is_open:
        ser.close()

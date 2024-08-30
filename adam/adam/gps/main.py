import csv
import time
import serial
import pynmea2
import requests
import os
import threading

# GPS serial port configuration
ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)

# CSV file configuration
csv_filename = 'gps_data.csv'
csv_headers = ['timestamp', 'latitude', 'longitude', 'altitude']

# REST API configuration
api_url = 'http://192.168.0.106:3000/insert'

# Flag to control the main loop
running = True

def write_to_csv(data):
    file_exists = os.path.isfile(csv_filename)
    with open(csv_filename, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

def upload_to_api(data):
    try:
        print(f"Attempting to upload data: {data}")
        response = requests.post(api_url, data=data)
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.text}")
        return response.status_code == 200
    except requests.RequestException as e:
        print(f"Request exception: {e}")
        return False

def exit_program():
    global running
    input("Press Enter to exit the program...")
    running = False

# Start the exit thread
exit_thread = threading.Thread(target=exit_program)
exit_thread.start()

while running:
    try:
        line = ser.readline().decode('ascii', errors='replace')
        if line.startswith('$GPGGA'):
            msg = pynmea2.parse(line)
            data = {
                'timestamp': time.time(),
                'latitude': msg.latitude,
                'longitude': msg.longitude,
                'altitude': msg.altitude
            }
            write_to_csv(data)
            print("Data written to CSV")
            if upload_to_api(data):
                print("Data uploaded successfully")
            else:
                print("Failed to upload data")
    except (pynmea2.ParseError, serial.SerialException) as e:
        print(f"Error: {e}")
    time.sleep(1)

# Clean up
ser.close()
print("Program terminated.")

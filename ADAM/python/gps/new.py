import csv
import time
import serial
import pynmea2
import socket
import os
import threading
import json
# GPS serial port configuration
ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)

# CSV file configuration
csv_filename = 'gps_data.csv'
csv_headers = ['timestamp', 'latitude', 'longitude', 'altitude']

# UDP socket configuration
udp_host = '192.168.0.106'
udp_port = 3000

# Flag to control the main loop
running = True

def write_to_csv(data):
    file_exists = os.path.isfile(csv_filename)
    with open(csv_filename, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

def send_to_udp(data):
    try:
        print(f"Attempting to send data: {data}")
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.sendto(json.dumps(data).encode('utf-8'), (udp_host, udp_port))
        print("Data sent to UDP socket")
    except socket.error as e:
        print(f"Socket error: {e}")

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
                    'timestamp': str(time.time()),
                'latitude': msg.latitude,
                'longitude': msg.longitude,
                'altitude': msg.altitude
            }
            write_to_csv(data)
            print("Data written to CSV")
            send_to_udp(data)
    except (pynmea2.ParseError, serial.SerialException) as e:
        print(f"Error: {e}")
    time.sleep(1)

# Clean up
ser.close()
print("Program terminated.")

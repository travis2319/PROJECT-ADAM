from serial import Serial
import time
import re
# port = 'COM7' #for windows
port = '/dev/ttyUSB0' #for linux
# Function to read GPS data from the serial port
def read_gps_data():
    with Serial(port, 115200, timeout=1) as ser:  # Replace with your correct port
        while True:
            if ser.in_waiting > 0:
                data = ser.readline().decode('utf-8', errors='ignore').strip()  # Ignore invalid characters
                return data

# Main loop to fetch GPS data
print("Reading GPS data from NodeMCU...")
try:
    while True:
        gps_raw_data = read_gps_data()
        print(gps_raw_data)  # Debugging: print the raw GPS data
        # Extract latitude and longitude from the GPS output
        match = re.search(r'Location:\s*([-\d.]+),\s*([-\d.]+)', gps_raw_data)
        if match:
            lat = match.group(1)
            lon = match.group(2)
            print("http://maps.google.com/?q="+ lat+","+lon)
            # print(f"Latitude: {lat}, Longitude: {lon}")
        else:
            print("No valid location data received.")
        time.sleep(0.5)  # Fetch every 0.5 seconds
except KeyboardInterrupt:
    print("GPS reading stopped.")

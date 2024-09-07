import obd
import time

# Connect to OBD-II interface
obd_connector = "/dev/ttyACM0"  # Replace with your OBD-II port
connection = obd.Async(obd_connector)

# Global variable to store supported PIDs
supported_pids = []

# Function to map binary strings to supported PIDs
def map_binary_to_pids(binary_string, start_pid):
    supported_pids = []
    for i, bit in enumerate(binary_string):
        if bit == '1':
            pid = start_pid + i
            supported_pids.append(f"{pid:02X}")
    return supported_pids

# Callback function to store supported PIDs
def handle_supported_pids(response):
    if not response.is_null():
        pids = response.value.bits
        global supported_pids
        supported_pids = map_binary_to_pids(pids, 0x01)  # Adjust the starting PID based on mode

# Function to determine supported PIDs
def determine_supported_pids():
    # Watch supported PID commands
    connection.watch(obd.commands.PIDS_A, callback=handle_supported_pids)
    connection.watch(obd.commands.PIDS_B, callback=handle_supported_pids)
    connection.watch(obd.commands.PIDS_C, callback=handle_supported_pids)

    # Start the connection
    connection.start()

    # Wait for a while to receive data
    time.sleep(10)

    # Stop the connection
    connection.stop()

    # Print the supported PIDs
    print(f"Supported PIDs: {supported_pids}")

# Function to print the values of supported PIDs with a delay
def query_pids():
    for pid in supported_pids:
        cmd = obd.commands.get(int(pid, 16))
        if cmd:
            response = connection.query(cmd)
            print(f"PID {pid}: {response.value}")
            time.sleep(0.5)  # Wait for 0.5 seconds between queries

# Run the process
determine_supported_pids()
query_pids()

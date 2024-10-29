import serial

def gps_connection(port, baud_rate):
    try:
        ser = serial.Serial(port, baud_rate, timeout=1)
        print(f"GPS connection established on {port}")
        return ser
    except Exception as e:
        print(f"Error connecting to GPS: {e}")
        return None
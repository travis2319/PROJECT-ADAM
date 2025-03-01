import serial

def nodemcu_connection(port='/dev/ttyUSB0', baud_rate=115200):
    try:
        ser = serial.Serial(port, baud_rate, timeout=1)
        print(f"Connection established on {port}")
        return ser
    except serial.SerialException as e:
        print(f"Error connecting to NodeMCU: {e}")
        return None
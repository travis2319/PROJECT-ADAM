import serial # type: ignore
import re
import pandas as pd # type: ignore
from datetime import datetime

def Esp8266_conn(portstr, baudrate):
    try:
        conn = serial.Serial(portstr, baudrate, timeout=1)
        print("Connected to Esp8266")
        return conn
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
        print("Esp8266 not Connected")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        print("Esp8266 not Connected")
        return None
    
def Esp8266_close_conn(conn):
    if conn is not None and conn.is_open:
        conn.close()
        print("Connection to ESP8266 closed")
    else:
        print("No active connection to close")
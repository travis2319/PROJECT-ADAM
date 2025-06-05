import serial
import pynmea2
import time

class Neo6M:
    def __init__(self, port='/dev/ttyAMA0', baudrate=9600, timeout=1):
        """Initialize GPS module with serial connection"""
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_connection = None
        self.latitude = None
        self.longitude = None
        self.altitude = None
        self.speed = None
        self.satellites = None
        self.timestamp = None
        self.valid_fix = False
    
    def connect(self):
        """Establish connection to the GPS module"""
        try:
            self.serial_connection = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout
            )
            print(f"Connected to GPS module at {self.port}")
            return True
        except serial.SerialException as e:
            print(f"Error connecting to GPS: {e}")
            return False
    
    def disconnect(self):
        """Close the serial connection"""
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            print("GPS connection closed")
    
    def read_gps_data(self):
        """Read and parse GPS data"""
        if not self.serial_connection or not self.serial_connection.is_open:
            if not self.connect():
                return False
                
        try:
            while True:
                line = self.serial_connection.readline().decode('ascii', errors='replace').strip()
                if line.startswith('$'):
                    try:
                        msg = pynmea2.parse(line)
                        
                        # Process GGA message (Global Positioning System Fix Data)
                        if isinstance(msg, pynmea2.GGA):
                            self.latitude = msg.latitude
                            self.longitude = msg.longitude
                            self.altitude = msg.altitude
                            self.satellites = msg.num_sats
                            self.timestamp = msg.timestamp
                            
                            # Check if we have a valid fix
                            if msg.gps_qual > 0:
                                self.valid_fix = True
                            else:
                                self.valid_fix = False
                                
                            return True
                            
                        # Process RMC message (Recommended Minimum Navigation Information)
                        elif isinstance(msg, pynmea2.RMC):
                            if msg.status == 'A':  # A=active, V=void
                                self.valid_fix = True
                                self.speed = msg.spd_over_grnd
                            else:
                                self.valid_fix = False
                                
                    except pynmea2.ParseError:
                        pass
                        
        except serial.SerialException as e:
            print(f"Serial error: {e}")
            return False
        except Exception as e:
            print(f"Error reading GPS data: {e}")
            return False
    
    def get_position(self):
        """Return current position as a dictionary"""
        if self.read_gps_data():
            return {
                'latitude': self.latitude,
                'longitude': self.longitude,
                'altitude': self.altitude,
                'speed': self.speed,
                'satellites': self.satellites,
                'timestamp': self.timestamp,
                'valid_fix': self.valid_fix
            }
        return None
    
    def display_position(self):
        """Display current position information"""
        position = self.get_position()
        if position and position['valid_fix']:
            print(f"Timestamp: {position['timestamp']}")
            print(f"Latitude: {position['latitude']}")
            print(f"Longitude: {position['longitude']}")
            print(f"Altitude: {position['altitude']} meters")
            if position['speed']:
                print(f"Speed: {position['speed']} knots")
            print(f"Satellites: {position['satellites']}")
            return position
        elif position:
            print("Waiting for valid GPS fix...")
            return None
        else:
            print("Unable to read GPS data")
            return None

# Example usage if run directly
# if __name__ == "__main__":
#     gps = Neo6M()
    
#     try:
#         print("GPS Monitoring - Press Ctrl+C to exit")
#         while True:
#             gps.display_position()
#             time.sleep(1)
#     except KeyboardInterrupt:
#         print("\nExiting...")
#     finally:
#         gps.disconnect()

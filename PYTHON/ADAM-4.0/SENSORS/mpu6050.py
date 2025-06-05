import smbus2 as smbus
import time

# MPU6050 Registers and their Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47

class MPU6050:
    def __init__(self, bus_num=1, device_address=0x68):
        """Initialize MPU6050 accelerometer and gyroscope sensor"""
        self.device_address = device_address
        self.bus_num = bus_num
        self.bus = None
        self.is_connected = False
        
        # Sensor data
        self.acc_x = 0
        self.acc_y = 0
        self.acc_z = 0
        self.gyro_x = 0
        self.gyro_y = 0
        self.gyro_z = 0
        
    def connect(self):
        """Establish connection to the I2C bus and initialize the sensor"""
        try:
            self.bus = smbus.SMBus(self.bus_num)
            self.initialize()
            self.is_connected = True
            print(f"Connected to MPU6050 at address 0x{self.device_address:02X}")
            return True
        except Exception as e:
            print(f"Error connecting to MPU6050: {e}")
            return False
    
    def disconnect(self):
        """Close the I2C connection"""
        if self.bus and self.is_connected:
            # Nothing specific needed to disconnect I2C
            self.is_connected = False
            print("MPU6050 connection closed")
    
    def initialize(self):
        """Initialize the MPU6050 with default settings"""
        # Write to sample rate register
        self.bus.write_byte_data(self.device_address, SMPLRT_DIV, 7)
        
        # Write to power management register
        self.bus.write_byte_data(self.device_address, PWR_MGMT_1, 1)
        
        # Write to Configuration register
        self.bus.write_byte_data(self.device_address, CONFIG, 0)
        
        # Write to Gyro configuration register
        self.bus.write_byte_data(self.device_address, GYRO_CONFIG, 24)
        
        # Write to interrupt enable register
        self.bus.write_byte_data(self.device_address, INT_ENABLE, 1)
    
    def read_raw_data(self, addr):
        """Read raw 16-bit data from the sensor registers"""
        if not self.is_connected:
            if not self.connect():
                return 0
                
        try:
            # Accelero and Gyro value are 16-bit
            high = self.bus.read_byte_data(self.device_address, addr)
            low = self.bus.read_byte_data(self.device_address, addr+1)
            
            # Concatenate higher and lower value
            value = ((high << 8) | low)
            
            # To get signed value from MPU6050
            if value > 32768:
                value = value - 65536
            return value
        except Exception as e:
            print(f"Error reading MPU6050 data: {e}")
            return 0
    
    def read_sensor_data(self):
        """Read and process sensor data"""
        if not self.is_connected:
            if not self.connect():
                return False
                
        try:
            # Read Accelerometer raw values
            self.acc_x = self.read_raw_data(ACCEL_XOUT_H)
            self.acc_y = self.read_raw_data(ACCEL_YOUT_H)
            self.acc_z = self.read_raw_data(ACCEL_ZOUT_H)
            
            # Read Gyroscope raw values
            self.gyro_x = self.read_raw_data(GYRO_XOUT_H)
            self.gyro_y = self.read_raw_data(GYRO_YOUT_H)
            self.gyro_z = self.read_raw_data(GYRO_ZOUT_H)
            
            return True
        except Exception as e:
            print(f"Error reading MPU6050 data: {e}")
            return False
    
    def get_motion_data(self):
        """Return processed motion data as a dictionary"""
        if self.read_sensor_data():
            # Full scale range +/- 250 degree/C as per sensitivity scale factor
            ax = self.acc_x/16384.0  # Convert to g
            ay = self.acc_y/16384.0
            az = self.acc_z/16384.0
            
            gx = self.gyro_x/131.0  # Convert to degrees/sec
            gy = self.gyro_y/131.0
            gz = self.gyro_z/131.0
            
            return {
                'accelerometer': {'x': ax, 'y': ay, 'z': az},
                'gyroscope': {'x': gx, 'y': gy, 'z': gz},
                'timestamp': time.time()
            }
        return None
    
    def display_motion_data(self):
        """Display current motion data"""
        data = self.get_motion_data()
        if data:
            ax = data['accelerometer']['x']
            ay = data['accelerometer']['y']
            az = data['accelerometer']['z']
            gx = data['gyroscope']['x']
            gy = data['gyroscope']['y']
            gz = data['gyroscope']['z']
            
            print(f"Gx={gx:.2f} °/s, Gy={gy:.2f} °/s, Gz={gz:.2f} °/s, Ax={ax:.2f} g, Ay={ay:.2f} g, Az={az:.2f} g")
            return data
        else:
            print("Unable to read motion data")
            return None

# # Example usage if run directly
# if __name__ == "__main__":
#     motion_sensor = MPU6050()
    
#     try:
#         print("MPU6050 Motion Monitoring - Press Ctrl+C to exit")
#         while True:
#             motion_sensor.display_motion_data()
#             time.sleep(0.2)
#     except KeyboardInterrupt:
#         print("\nExiting...")
#     finally:
#         motion_sensor.disconnect()

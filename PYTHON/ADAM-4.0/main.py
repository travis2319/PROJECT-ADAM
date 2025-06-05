#!/usr/bin/env python3
"""
Main program to interface with NEO-6M GPS, MPU6050, and SW420 sensors on Raspberry Pi
"""

import time
import signal
import sys

# Import sensor classes from their respective modules
from SENSORS.neo6m import Neo6M
from SENSORS.mpu6050 import MPU6050
from SENSORS.sw420 import SW420

# Global flag for graceful shutdown
running = True

def signal_handler(sig, frame):
    """Handle Ctrl+C for graceful shutdown"""
    global running
    print("\nShutting down...")
    running = False

def initialize_sensors():
    """Initialize all sensors and establish connections"""
    try:
        # Create sensor instances
        print("Initializing sensors...")
        gps = Neo6M(port='/dev/ttyAMA0', baudrate=9600, timeout=1)
        mpu = MPU6050(bus_num=1, device_address=0x68)
        vibration = SW420(sensor_pin=17)
        
        # Connect to all sensors
        gps_connected = gps.connect()
        mpu_connected = mpu.connect()
        vibration_connected = vibration.connect()
        
        if gps_connected and mpu_connected and vibration_connected:
            print("All sensors connected successfully!")
        else:
            print("Warning: Some sensors failed to connect")
            
        return gps, mpu, vibration
        
    except Exception as e:
        print(f"Error initializing sensors: {e}")
        sys.exit(1)

def main():
    """Main function to read and display sensor data"""
    global running
    
    # Setup signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    # Initialize sensors
    gps, mpu, vibration = initialize_sensors()
    
    print("\nStarting sensor readings. Press Ctrl+C to exit.")
    
    try:
        while running:
            print("\n----- Sensor Readings -----")
            
            # Get and display GPS data
            gps_data = gps.get_position()
            if gps_data and gps_data['valid_fix']:
                print(f"GPS: Lat={gps_data['latitude']:.6f}, Lon={gps_data['longitude']:.6f}, " + 
                      f"Alt={gps_data['altitude']}m, Satellites={gps_data['satellites']}")
            else:
                print("GPS: Waiting for valid fix...")
            
            # Get and display MPU6050 data
            motion_data = mpu.get_motion_data()
            if motion_data:
                accel = motion_data['accelerometer']
                gyro = motion_data['gyroscope']
                print(f"MPU6050 Accelerometer: X={accel['x']:.2f}g, Y={accel['y']:.2f}g, Z={accel['z']:.2f}g")
                print(f"MPU6050 Gyroscope: X={gyro['x']:.2f}°/s, Y={gyro['y']:.2f}°/s, Z={gyro['z']:.2f}°/s")
            else:
                print("MPU6050: Unable to read data")
            
            # Get and display vibration data
            vibration_data = vibration.get_status()
            if vibration_data:
                vibration_status = "Detected!" if vibration_data['vibration_detected'] else "None"
                print(f"Vibration: {vibration_status}")
            else:
                print("Vibration sensor: Unable to read data")
            
            # Wait before next reading
            time.sleep(1)
    
    except Exception as e:
        print(f"Error in main loop: {e}")
    
    finally:
        # Clean up and disconnect all sensors
        print("\nDisconnecting sensors...")
        gps.disconnect()
        mpu.disconnect()
        vibration.disconnect()
        print("Program ended")

if __name__ == "__main__":
    main()

# #!/usr/bin/env python3
# """
# Raspberry Pi Sensor Integration
# Main program that integrates GPS, Motion, and Vibration sensors
# """

# import time
# import sys
# import os
# import signal
# import json
# from datetime import datetime

# # Add the project root to the path to import modules
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# # Import sensor modules
# from SENSORS.neo6m import Neo6M
# from SENSORS.mpu6050 import MPU6050
# from SENSORS.sw420 import SW420

# # Import utility modules
# from UTILS.logger import Logger
# from UTILS.data_manager import DataManager

# class SensorSystem:
#     def __init__(self):
#         """Initialize the integrated sensor system"""
#         # Set up logger
#         self.logger = Logger(log_dir="logs")
#         self.logger.info("Starting sensor system...")
        
#         # Set up data manager
#         self.data_manager = DataManager(data_dir="data")
        
#         # Initialize sensors
#         self.gps = Neo6M(port='/dev/ttyAMA0', baudrate=9600)
#         self.motion_sensor = MPU6050(bus_num=1, device_address=0x68)
#         self.vibration_sensor = SW420(sensor_pin=17)
        
#         # Initialize flags
#         self.running = False
        
#         # Set up signal handlers for graceful shutdown
#         signal.signal(signal.SIGINT, self.signal_handler)
#         signal.signal(signal.SIGTERM, self.signal_handler)
    
#     def initialize_sensors(self):
#         """Connect to all sensors"""
#         self.logger.info("Initializing sensors...")
        
#         # Connect GPS
#         if self.gps.connect():
#             self.logger.info("GPS module initialized")
#         else:
#             self.logger.error("Failed to initialize GPS module")
        
#         # Connect motion sensor
#         if self.motion_sensor.connect():
#             self.logger.info("Motion sensor initialized")
#         else:
#             self.logger.error("Failed to initialize motion sensor")
        
#         # Connect vibration sensor
#         if self.vibration_sensor.connect():
#             self.logger.info("Vibration sensor initialized")
#         else:
#             self.logger.error("Failed to initialize vibration sensor")
    
#     def read_all_sensors(self):
#         """Read data from all sensors"""
#         # Read GPS data
#         gps_data = self.gps.get_position()
#         if gps_data and gps_data.get('valid_fix'):
#             self.logger.info(f"GPS: {gps_data['latitude']:.6f}, {gps_data['longitude']:.6f}, Alt: {gps_data['altitude']}")
#         else:
#             self.logger.debug("Waiting for valid GPS fix...")
        
#         # Read motion sensor data
#         motion_data = self.motion_sensor.get_motion_data()
#         if motion_data:
#             acc = motion_data['accelerometer']
#             gyro = motion_data['gyroscope']
#             self.logger.debug(f"Motion: Acc(x,y,z): {acc['x']:.2f}, {acc['y']:.2f}, {acc['z']:.2f} g, " +
#                             f"Gyro(x,y,z): {gyro['x']:.2f}, {gyro['y']:.2f}, {gyro['z']:.2f} deg/s")
        
#         # Read vibration sensor data
#         vibration_data = self.vibration_sensor.get_status()
#         if vibration_data:
#             if vibration_data['vibration_detected']:
#                 self.logger.info("Vibration detected!")
#             else:
#                 self.logger.debug("No vibration")
        
#         # Save combined data
#         combined_data = self.data_manager.save_combined_data(
#             gps_data=gps_data,
#             motion_data=motion_data,
#             vibration_data=vibration_data
#         )
        
#         return combined_data
    
#     def start(self, interval=1.0):
#         """Start the sensor monitoring loop"""
#         self.running = True
#         self.initialize_sensors()
        
#         self.logger.info(f"Sensor monitoring started with {interval}s interval")
#         print(f"\nSensor System Running - Press Ctrl+C to exit\n")
        
#         try:
#             while self.running:
#                 start_time = time.time()
                
#                 # Read all sensors
#                 data = self.read_all_sensors()
                
#                 # Calculate time to sleep to maintain consistent interval
#                 elapsed = time.time() - start_time
#                 sleep_time = max(0, interval - elapsed)
                
#                 if sleep_time > 0:
#                     time.sleep(sleep_time)
                    
#         except Exception as e:
#             self.logger.error(f"Error in sensor monitoring loop: {e}")
#         finally:
#             self.stop()
    
#     def stop(self):
#         """Stop the sensor system and close all connections"""
#         self.running = False
#         self.logger.info("Shutting down sensor system...")
        
#         # Disconnect from all sensors
#         self.gps.disconnect()
#         self.motion_sensor.disconnect()
#         self.vibration_sensor.disconnect()
        
#         self.logger.info("Sensor system shutdown complete")
    
#     def signal_handler(self, sig, frame):
#         """Handle termination signals for graceful shutdown"""
#         print("\nShutting down...")
#         self.stop()
#         sys.exit(0)

# if __name__ == "__main__":
#     # Create and start the sensor system
#     system = SensorSystem()
    
#     # Parse command line arguments for sampling interval
#     interval = 1.0  # Default interval in seconds
#     if len(sys.argv) > 1:
#         try:
#             interval = float(sys.argv[1])
#             if interval < 0.1:
#                 print("Warning: Very small intervals may cause system instability")
#                 interval = max(0.1, interval)
#         except ValueError:
#             print(f"Invalid interval: {sys.argv[1]}. Using default: 1.0s")
    
#     # Start the system with the specified interval
#     system.start(interval)

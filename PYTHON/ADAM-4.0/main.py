#!/usr/bin/env python3

import time
import signal
import sys
from SENSORS.neo6m import Neo6M
from SENSORS.mpu6050 import MPU6050
from SENSORS.sw420 import SW420
from UTILS.config_loader import load_config
from UTILS.data_manager import CSVDataManager


running = True

def signal_handler(sig, frame):
    global running
    print("\nShutting down...")
    running = False

def initialize_sensors(config):
    sensor_names = []
    try:
        print("Initializing sensors...")

        # Initialize NEO-6M GPS
        gps = Neo6M(
            port=config['PORTS']['GPS_PORT'],
            baudrate=int(config['PORTS']['GPS_BAUDRATE']),
            timeout=1
        )
        if gps.connect():
            print("[✓] NEO-6M GPS connected")
            sensor_names.append("NEO-6M GPS")
        else:
            print("[✗] NEO-6M GPS failed to connect")

        # Initialize MPU6050
        mpu = MPU6050(
            bus_num=int(config['PORTS']['MPU6050_BUS']),
            device_address=int(config['PORTS']['MPU6050_ADDRESS'], 16)
        )
        if mpu.connect():
            print("[✓] MPU6050 connected")
            sensor_names.append("MPU6050")
        else:
            print("[✗] MPU6050 failed to connect")

        # Initialize SW420 Vibration Sensor
        vibration = SW420(sensor_pin=int(config['PORTS']['SW420_PIN']))
        if vibration.connect():
            print("[✓] SW420 Vibration Sensor connected")
            sensor_names.append("SW420 Vibration Sensor")
        else:
            print("[✗] SW420 Vibration Sensor failed to connect")

        if not sensor_names:
            print("No sensors connected successfully. Exiting.")
            sys.exit(1)

        return gps, mpu, vibration, sensor_names

    except Exception as e:
        print(f"Error initializing sensors: {e}")
        sys.exit(1)


def main():
    global running
    signal.signal(signal.SIGINT, signal_handler)

    config = load_config()
    gps, mpu, vibration, sensor_names = initialize_sensors(config)

    print("\nStarting sensor readings. Press Ctrl+C to exit.")

    last_gps_time = time.time()
    last_mpu_time = time.time()
    last_vibration_time = time.time()

    gps_interval = 0.3          # seconds
    mpu_interval = 0.1
    vibration_interval = 0.03

    data_logger = CSVDataManager("sensor_data.csv")

    try:
        # Initialize variables before loop
        gps_data = None
        motion_data = None
        vibration_data = None  

        while running:
            current_time = time.time()

            if current_time - last_gps_time >= gps_interval:
                gps_data = gps.get_position()
                if gps_data and gps_data['valid_fix']:
                    print(f"GPS: Lat={gps_data['latitude']:.6f}, Lon={gps_data['longitude']:.6f}, Alt={gps_data['altitude']}m, Satellites={gps_data['satellites']}")
                else:
                    print("GPS: Waiting for valid fix...")
                last_gps_time = current_time

            if current_time - last_mpu_time >= mpu_interval:
                motion_data = mpu.get_motion_data()
                if motion_data:
                    accel = motion_data['accelerometer']
                    gyro = motion_data['gyroscope']
                    print(f"MPU6050 Accelerometer: X={accel['x']:.2f}g, Y={accel['y']:.2f}g, Z={accel['z']:.2f}g")
                    print(f"MPU6050 Gyroscope: X={gyro['x']:.2f}°/s, Y={gyro['y']:.2f}°/s, Z={gyro['z']:.2f}°/s")
                else:
                    print("MPU6050: Unable to read data")
                last_mpu_time = current_time

            if current_time - last_vibration_time >= vibration_interval:
                vibration_data = vibration.get_status()
                if vibration_data:
                    status = "Detected!" if vibration_data['vibration_detected'] else "None"
                    print(f"Vibration: {status}")
                else:
                    print("Vibration sensor: Unable to read data")
                last_vibration_time = current_time

            # Safe to use vibration_data now because it's initialized before the loop
            data_logger.log_data(
                gps_data, 
                motion_data, 
                vibration_data['vibration_detected'] if vibration_data else None
            )

            time.sleep(0.01)


    except Exception as e:
        print(f"Error in main loop: {e}")

    finally:
        print("\nDisconnecting sensors...")
        gps.disconnect()
        mpu.disconnect()
        vibration.disconnect()
        print("Program ended")

if __name__ == "__main__":
    main()

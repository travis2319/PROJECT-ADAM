import csv
import os
from datetime import datetime

class CSVDataManager:
    def __init__(self, filename):
        self.filename = filename
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Create file and headers if not present"""
        if not os.path.isfile(self.filename):
            with open(self.filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    "Timestamp",
                    "Latitude", "Longitude", "Altitude", "Satellites",
                    "Accel_X", "Accel_Y", "Accel_Z",
                    "Gyro_X", "Gyro_Y", "Gyro_Z",
                    "Vibration"
                ])

    def log_data(self, gps_data, motion_data, vibration_status):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(self.filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                timestamp,
                gps_data.get('latitude') if gps_data and gps_data['valid_fix'] else "",
                gps_data.get('longitude') if gps_data and gps_data['valid_fix'] else "",
                gps_data.get('altitude') if gps_data and gps_data['valid_fix'] else "",
                gps_data.get('satellites') if gps_data and gps_data['valid_fix'] else "",
                motion_data['accelerometer']['x'] if motion_data else "",
                motion_data['accelerometer']['y'] if motion_data else "",
                motion_data['accelerometer']['z'] if motion_data else "",
                motion_data['gyroscope']['x'] if motion_data else "",
                motion_data['gyroscope']['y'] if motion_data else "",
                motion_data['gyroscope']['z'] if motion_data else "",
                "Detected" if vibration_status else "None"
            ])
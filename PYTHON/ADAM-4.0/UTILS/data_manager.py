import os
import json
from datetime import datetime

class DataManager:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        
        # Create data directory if it doesn't exist
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        
        # Create daily directory
        self.daily_dir = os.path.join(data_dir, datetime.now().strftime('%Y%m%d'))
        if not os.path.exists(self.daily_dir):
            os.makedirs(self.daily_dir)
    
    def save_combined_data(self, gps_data=None, motion_data=None, vibration_data=None):
        """Save combined sensor data to JSON file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Prepare data dict
        data = {
            'timestamp': timestamp,
            'gps': gps_data if gps_data else {},
            'motion': motion_data if motion_data else {},
            'vibration': vibration_data if vibration_data else {}
        }
        
        # Save to file
        filename = os.path.join(self.daily_dir, f"data_{timestamp}.json")
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        return data

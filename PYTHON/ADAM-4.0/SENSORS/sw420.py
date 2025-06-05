import lgpio
import time

class SW420:
    def __init__(self, sensor_pin=17):
        """Initialize SW420 vibration sensor with GPIO pin"""
        self.sensor_pin = sensor_pin
        self.gpio_handle = None
        self.is_connected = False
        self.vibration_detected = False
        self.last_state = 1  # Assuming idle/high at startup
        
    def connect(self):
        """Establish connection to the GPIO"""
        try:
            self.gpio_handle = lgpio.gpiochip_open(0)
            lgpio.gpio_claim_input(self.gpio_handle, self.sensor_pin)
            self.is_connected = True
            print(f"Connected to SW420 on pin {self.sensor_pin}")
            return True
        except Exception as e:
            print(f"Error connecting to SW420: {e}")
            return False
    
    def disconnect(self):
        """Close the GPIO connection"""
        if self.gpio_handle and self.is_connected:
            lgpio.gpiochip_close(self.gpio_handle)
            self.is_connected = False
            print("SW420 connection closed")
    
    def read_vibration(self):
        """Read vibration status from the sensor"""
        if not self.is_connected:
            if not self.connect():
                return None                
        try:
            current_state = lgpio.gpio_read(self.gpio_handle, self.sensor_pin)
            vibration_event = self.last_state == 1 and current_state == 0
            self.vibration_detected = vibration_event
            self.last_state = current_state
            return self.vibration_detected
        except Exception as e:
            print(f"Error reading SW420 data: {e}")
            return None
    
    def get_status(self):
        """Return current vibration status as a dictionary"""
        vibration = self.read_vibration()
        if vibration is not None:
            return {
                'vibration_detected': vibration,
                'timestamp': time.time()
            }
        return None
    
    def display_status(self):
        """Display current vibration status"""
        status = self.get_status()
        if status:
            if status['vibration_detected']:
                print("Vibration detected!")
            else:
                print("No vibration")
            return status
        else:
            print("Unable to read vibration data")
            return None

# Example usage if run directly
# if __name__ == "__main__":
#     vibration_sensor = SW420()
    
#     try:
#         print("SW420 Vibration Monitoring - Press Ctrl+C to exit")
#         while True:
#             vibration_sensor.display_status()
#             time.sleep(0.5)
#     except KeyboardInterrupt:
#         print("\nExiting...")
#     finally:
#         vibration_sensor.disconnect()

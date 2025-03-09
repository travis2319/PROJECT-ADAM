import time
import sys
def signal_handler(sig, frame,Async_conn,esp_conn):
    """Handle keyboard interrupt (Ctrl+C)"""
    global running
    print("\nCtrl+C detected. Stopping data collection...")
    running = False
    
    # Allow time for threads to finish current iterations
    time.sleep(1)
    
    # Close connections if they exist
    if Async_conn:
        print("Closing OBD connection...")
        Async_conn.close()
    
    if esp_conn:
        print("Closing ESP8266 connection...")
        esp_conn.close()
    
    print("Exiting ADAM")
    sys.exit(0)

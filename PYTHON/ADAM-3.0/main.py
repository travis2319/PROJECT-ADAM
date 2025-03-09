import time
import threading
import pandas as pd # type: ignore
import signal
import sys
import os
from datetime import datetime
from OBD_HANDLER import (
    Async_connection,
    get_supported_commands,
    start_data_collection,
) # type: ignore

from TRANSMISSION import (
    sendToServer,
)
from ESP8266_HANDLER import (
    Esp8266_conn,
    read_serial,
) # type: ignore

from Utils.config import read_config

# Global flag to control the main loop
running = True
# Global variables for connections to properly close them on exit
Async_conn = None
esp_conn = None

def signal_handler(sig, frame):
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

def collect_obd_data(conn, interval, sensor_file, result_dict):
    print("Starting OBD data collection thread")
    try:
        obd_df = start_data_collection(conn, interval, sensor_file)
        result_dict['obd_df'] = obd_df
    except Exception as e:
        print(f"Error in OBD data collection: {e}")
        result_dict['obd_df'] = pd.DataFrame()

def collect_serial_data(conn, result_dict):
    print("Starting ESP8266 data collection thread")
    try:
        start_time = time.time()
        serial_df = read_serial(conn)
        end_time = time.time()
        result_dict['serial_df'] = serial_df
        result_dict['serial_time'] = end_time - start_time
        print(f"Serial data collection completed in {result_dict['serial_time']} seconds")
    except Exception as e:
        print(f"Error in ESP8266 data collection: {e}")
        result_dict['serial_df'] = pd.DataFrame()
        result_dict['serial_time'] = 0

def merge_dataframes(obd_df, serial_df):
    # Reset indexes to ensure alignment
    obd_df = obd_df.reset_index(drop=True)
    serial_df = serial_df.reset_index(drop=True)
    
    # Add timestamp columns
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    obd_df["timestamp_obd"] = timestamp
    serial_df["timestamp_esp8266"] = timestamp
    
    # Concatenate DataFrames horizontally
    combined_df = pd.concat([obd_df, serial_df], axis=1)

    return combined_df

def append_to_data_csv(temp_csv_path, data_csv_path):
    """Append temp.csv data to data.csv"""
    try:
        # Read the temp CSV file
        temp_df = pd.read_csv(temp_csv_path)
        
        # Check if the data.csv file exists
        file_exists = os.path.isfile(data_csv_path)
        
        if file_exists:
            # Append without headers
            temp_df.to_csv(data_csv_path, mode='a', header=False, index=False)
            print(f"Data appended to {data_csv_path}")
        else:
            # Create new file with headers
            temp_df.to_csv(data_csv_path, index=False)
            print(f"Created new file {data_csv_path}")
            
        return True
    except Exception as e:
        print(f"Error appending data: {e}")
        return False

def main():
    global Async_conn, esp_conn, running
    
    # Register signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    print("Initializing ADAM")
    
    # Define file paths
    # temp_csv_path = "temp.csv"
    # data_csv_path = "data.csv"
    
    # Read parameters from config file
    obd_port, esp8266_port, esp8266_baud, sensor_file,temp_csv_path,data_csv_path,server_url = read_config()
    print(f"OBD Port: {obd_port} | ESP8266 Port: {esp8266_port}")
    
    try:
        Async_conn = Async_connection(obd_port)
        print("Connected to OBD")
        print(Async_conn.status())
        
        commands_names = get_supported_commands(Async_conn, sensor_file)
        print(f"Supported commands: {commands_names}")
        
        esp_conn = Esp8266_conn(esp8266_port, esp8266_baud)
        
        # Main loop
        iteration = 1
        while running:
            print(f"\n--- Starting iteration {iteration} ---")
            
            # Create a dictionary to store results from threads
            results = {}
            
            # Create threads for parallel data collection
            obd_thread = threading.Thread(
                target=collect_obd_data, 
                args=(Async_conn, 1, sensor_file, results)
            )
            
            esp_thread = threading.Thread(
                target=collect_serial_data,
                args=(esp_conn, results)
            )
            
            # Start both threads
            print("Starting parallel data collection")
            obd_thread.start()
            esp_thread.start()
            
            # Wait for both threads to complete
            obd_thread.join()
            esp_thread.join()
            print("Parallel data collection completed")
            
            # Display results
            print(f"OBD data collection time: {results.get('obd_time', 'N/A')} seconds")
            print(f"Serial data collection time: {results.get('serial_time', 'N/A')} seconds")
            
            # Merge dataframes if both exist
            if 'obd_df' in results and 'serial_df' in results:
                combined_df = merge_dataframes(results['obd_df'], results['serial_df'])
                
                # Save to temp CSV first
                combined_df.to_csv(temp_csv_path, index=False)
                print(f"Combined data saved to {temp_csv_path}")
                
                # Append temp data to main data file
                append_result = append_to_data_csv(temp_csv_path, data_csv_path)
                if append_result:
                    print(f"Data successfully appended to {data_csv_path}")
                
                # Upload temp.csv to remote server
                upload_result = sendToServer(temp_csv_path, server_url)
                if upload_result:
                    print("File successfully uploaded to server")
                
                # Display the combined dataframe
                print("Combined DataFrame preview:")
                print(combined_df.head())
            else:
                print("Could not create combined dataframe - missing data from one or both sources")
            
            iteration += 1
            print(f"Completed iteration {iteration-1}. Press Ctrl+C to exit.")
            
            # Optional: Add a delay between iterations
            time.sleep(1)
            
    except Exception as e:
        print(f"Error in main process: {e}")
    finally:
        # Ensure connections are closed
        if Async_conn:
            Async_conn.close()
        print("Exiting ADAM")

if __name__ == "__main__":
    main()

# import time
# import threading
# import pandas as pd # type: ignore
# import signal
# import sys
# from datetime import datetime
# from OBD_HANDLER import (
#     Async_connection,
#     get_supported_commands,
#     start_data_collection,
# ) # type: ignore

# from ESP8266_HANDLER import (
#     Esp8266_conn,
#     read_serial,
# ) # type: ignore

# from Utils.config import read_config

# # Global flag to control the main loop
# running = True
# # Global variables for connections to properly close them on exit
# Async_conn = None
# esp_conn = None

# def signal_handler(sig, frame):
#     """Handle keyboard interrupt (Ctrl+C)"""
#     global running
#     print("\nCtrl+C detected. Stopping data collection...")
#     running = False
    
#     # Allow time for threads to finish current iterations
#     time.sleep(1)
    
#     # Close connections if they exist
#     if Async_conn:
#         print("Closing OBD connection...")
#         Async_conn.close()
    
#     if esp_conn:
#         print("Closing ESP8266 connection...")
#         esp_conn.close()
    
#     print("Exiting ADAM")
#     sys.exit(0)

# def collect_obd_data(conn, interval, sensor_file, result_dict):
#     print("Starting OBD data collection thread")
#     try:
#         obd_df = start_data_collection(conn, interval, sensor_file)
#         result_dict['obd_df'] = obd_df
#     except Exception as e:
#         print(f"Error in OBD data collection: {e}")
#         result_dict['obd_df'] = pd.DataFrame()

# def collect_serial_data(conn, result_dict):
#     print("Starting ESP8266 data collection thread")
#     try:
#         start_time = time.time()
#         serial_df = read_serial(conn)
#         end_time = time.time()
#         result_dict['serial_df'] = serial_df
#         result_dict['serial_time'] = end_time - start_time
#         print(f"Serial data collection completed in {result_dict['serial_time']} seconds")
#     except Exception as e:
#         print(f"Error in ESP8266 data collection: {e}")
#         result_dict['serial_df'] = pd.DataFrame()
#         result_dict['serial_time'] = 0

# def merge_dataframes(obd_df, serial_df):
#     # Reset indexes to ensure alignment
#     obd_df = obd_df.reset_index(drop=True)
#     serial_df = serial_df.reset_index(drop=True)
    
#     # Add timestamp columns
#     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     obd_df["timestamp_obd"] = timestamp
#     serial_df["timestamp_esp8266"] = timestamp
    
#     # Concatenate DataFrames horizontally
#     combined_df = pd.concat([obd_df, serial_df], axis=1)

#     return combined_df

# def main():
#     global Async_conn, esp_conn, running
    
#     # Register signal handler for Ctrl+C
#     signal.signal(signal.SIGINT, signal_handler)
    
#     print("Initializing ADAM")
    
#     # Read parameters from config file
#     obd_port, esp8266_port, esp8266_baud, sensor_file = read_config()
#     print(f"OBD Port: {obd_port} | ESP8266 Port: {esp8266_port}")
    
#     try:
#         Async_conn = Async_connection(obd_port)
#         print("Connected to OBD")
#         print(Async_conn.status())
        
#         commands_names = get_supported_commands(Async_conn, sensor_file)
#         print(f"Supported commands: {commands_names}")
        
#         esp_conn = Esp8266_conn(esp8266_port, esp8266_baud)
        
#         # Main loop
#         iteration = 1
#         while running:
#             print(f"\n--- Starting iteration {iteration} ---")
            
#             # Create a dictionary to store results from threads
#             results = {}
            
#             # Create threads for parallel data collection
#             obd_thread = threading.Thread(
#                 target=collect_obd_data, 
#                 args=(Async_conn, 1, sensor_file, results)
#             )
            
#             esp_thread = threading.Thread(
#                 target=collect_serial_data,
#                 args=(esp_conn, results)
#             )
            
#             # Start both threads
#             print("Starting parallel data collection")
#             obd_thread.start()
#             esp_thread.start()
            
#             # Wait for both threads to complete
#             obd_thread.join()
#             esp_thread.join()
#             print("Parallel data collection completed")
            
#             # Display results
#             print(f"OBD data collection time: {results.get('obd_time', 'N/A')} seconds")
#             print(f"Serial data collection time: {results.get('serial_time', 'N/A')} seconds")
            
#             # Merge dataframes if both exist
#             if 'obd_df' in results and 'serial_df' in results:
#                 combined_df = merge_dataframes(results['obd_df'], results['serial_df'])
                
#                 # Generate filename with timestamp
#                 # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#                 filename = "temp.csv"
                
#                 # Save to CSV
#                 combined_df.to_csv(filename, index=False)
#                 print(f"Combined data saved to {filename}")
                
#                 # Display the combined dataframe
#                 print("Combined DataFrame preview:")
#                 print(combined_df.head())
#             else:
#                 print("Could not create combined dataframe - missing data from one or both sources")
            
#             iteration += 1
#             print(f"Completed iteration {iteration-1}. Press Ctrl+C to exit.")
            
#             # Optional: Add a delay between iterations
#             time.sleep(1)
            
#     except Exception as e:
#         print(f"Error in main process: {e}")
#     finally:
#         # Ensure connections are closed
#         if Async_conn:
#             Async_conn.close()
#         print("Exiting ADAM")

# if __name__ == "__main__":
#     main()


# import time
# import threading
# import pandas as pd # type: ignore
# from datetime import datetime
# from OBD_HANDLER import (
#     Async_connection,
#     get_supported_commands,
#     start_data_collection,
# ) # type: ignore

# from ESP8266_HANDLER import (
#     Esp8266_conn,
#     read_serial,
# ) # type: ignore

# from Utils.config import read_config

# def collect_obd_data(conn, interval, sensor_file, result_dict):
#     print("Starting OBD data collection thread")
#     # start_time = time.time()
#     obd_df = start_data_collection(conn, interval, sensor_file)
#     # end_time = time.time()
#     result_dict['obd_df'] = obd_df
#     # result_dict['obd_time'] = end_time - start_time
#     # print(f"OBD data collection completed in {result_dict['obd_time']} seconds")

# def collect_serial_data(conn, result_dict):
#     print("Starting ESP8266 data collection thread")
#     start_time = time.time()
#     serial_df = read_serial(conn)
#     end_time = time.time()
#     result_dict['serial_df'] = serial_df
#     result_dict['serial_time'] = end_time - start_time
#     print(f"Serial data collection completed in {result_dict['serial_time']} seconds")

# def merge_dataframes(obd_df, serial_df):
#     # Reset indexes to ensure alignment
#     obd_df = obd_df.reset_index(drop=True)
#     serial_df = serial_df.reset_index(drop=True)
    
#     # Add timestamp columns
#     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     obd_df["timestamp_obd"] = timestamp
#     serial_df["timestamp_esp8266"] = timestamp
    
#     # Concatenate DataFrames horizontally
#     combined_df = pd.concat([obd_df, serial_df], axis=1)

#     return combined_df

# def main():
#     print("Initializing ADAM")
    
#     # Read parameters from config file
#     obd_port, esp8266_port, esp8266_baud, sensor_file = read_config()
#     print(f"OBD Port: {obd_port} | ESP8266 Port: {esp8266_port}")
    
#     Async_conn = Async_connection(obd_port)
#     print("Connected to OBD")
#     print(Async_conn.status())
    
#     commands_names = get_supported_commands(Async_conn, sensor_file)
#     print(f"Supported commands: {commands_names}")
    
#     esp_conn = Esp8266_conn(esp8266_port, esp8266_baud)
    
#     # Create a dictionary to store results from threads
#     results = {}
    
#     # Create threads for parallel data collection
#     obd_thread = threading.Thread(
#         target=collect_obd_data, 
#         args=(Async_conn, 1, sensor_file, results)
#     )
    
#     esp_thread = threading.Thread(
#         target=collect_serial_data,
#         args=(esp_conn, results)
#     )
    
#     # Start both threads
#     print("Starting parallel data collection")
#     obd_thread.start()
#     esp_thread.start()
    
#     # Wait for both threads to complete
#     obd_thread.join()
#     esp_thread.join()
#     print("Parallel data collection completed")
    
#     # Display results
#     print(f"OBD data collection time: {results.get('obd_time', 'N/A')} seconds")
#     print(f"Serial data collection time: {results.get('serial_time', 'N/A')} seconds")
    
#     # Merge dataframes if both exist
#     if 'obd_df' in results and 'serial_df' in results:
#         combined_df = merge_dataframes(results['obd_df'], results['serial_df'])
        
#         # Generate filename with timestamp
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#         filename = f"combined_data_{timestamp}.csv"
        
#         # Save to CSV
#         combined_df.to_csv(filename, index=False)
#         print(f"Combined data saved to {filename}")
        
#         # Display the combined dataframe
#         print("Combined DataFrame:")
#         print(combined_df)
#     else:
#         print("Could not create combined dataframe - missing data from one or both sources")
    
#     Async_conn.close()
#     print("Connection closed")
#     print("Exiting ADAM")

# if __name__ == "__main__":
#     main()

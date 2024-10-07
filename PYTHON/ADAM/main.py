import time
from OBD_HANDLER import (
    obd_connection, async_connection, initialize_supported_pids,
    get_pid_names, setup_data_collection, start_data_collection,
    supported_pids, supported_mids
)
from GPS_HANDLER import gps_connection, collect_gps_data
from DATA_PROCESSING import data_processing

def main(obd_connector, sleep_interval):
    print("Starting OBD-II data collection cycle...")
    
    # Use OBD connection to initialize supported PIDs and MIDs
    obd_conn = obd_connection(obd_connector)
    if not obd_conn:
        print("Unable to establish OBD connection. Exiting...")
        return

    initialize_supported_pids(obd_conn)
    supported_pid_names = get_pid_names(supported_pids)
    
    # # Close the OBD connection
    # obd_conn.close()

    # Now use Async connection for data collection
    async_conn = async_connection(obd_connector)
    if not async_conn:
        print("Unable to establish asynchronous connection. Exiting...")
        return
    
    gps_ser = gps_connection(gps_port)
    if not gps_ser:
        print("Unable to establish GPS connection. Exiting...")
        return

    try:
        while True:
            if supported_pid_names:
                setup_data_collection(async_conn, supported_pid_names)
                
                obd_df = start_data_collection(async_conn, 5)  # Data collection period of 25 seconds
                
                gps_df = collect_gps_data(gps_ser, 25)  # 25 seconds of data collection
                
                combined_df = pd.merge(obd_df, gps_df, on='Timestamp', how='outer')
                
                if not combined_df.empty:
                    print(combined_df)
                    save_data_to_csv(combined_df, 'check.csv')
                    print(f"DataFrame saved to check.csv")
                else:
                    print("No data collected in this cycle.")
            else:
                print("No supported PIDs found.")

            print(f"Waiting for {sleep_interval} seconds before the next cycle...")
            time.sleep(sleep_interval)

    except KeyboardInterrupt:
        print("\nData collection stopped by user.")
        if async_conn:
            async_conn.stop()  # Ensure the OBD connection is closed
        if gps_ser:
            gps_ser.close()
        print("Program terminated.")

if __name__ == "__main__":
    obd_connector = "/dev/pts/3"  # Replace with your actual OBD-II port
    gps_connector = '/dev/ttyUSB0'  # Replace with your actual GPS port
    main(obd_connector,gps_connector, sleep_interval=10)  # 10-second interval between cycles
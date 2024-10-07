import time
from OBD_HANDLER import (
    obd_connection, async_connection, initialize_supported_pids,
    get_pid_names, setup_data_collection, start_data_collection,
    save_data_to_csv, supported_pids, supported_mids
)

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

    try:
        while True:
            if supported_pid_names:
                setup_data_collection(async_conn, supported_pid_names)
                collected_df = start_data_collection(async_conn, 5)  # Data collection period of 25 seconds
                
                if not collected_df.empty:
                    print(collected_df)
                    save_data_to_csv(collected_df, 'check.csv')
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
        print("Program terminated.")

if __name__ == "__main__":
    obd_connector = "/dev/pts/3"  # Replace with your actual OBD-II port
    main(obd_connector, sleep_interval=10)  # 10-second interval between cycles
import time
import pandas as pd
from OBD_HANDLER import (
    obd_connection, async_connection, initialize_supported_pids,
    get_pid_names, setup_data_collection, start_data_collection,
    supported_pids, supported_mids
)
from GPS_HANDLER import gps_connection, read_gps_data, parse_gps_data, collect_gps_data
from DATA_PROCESSING import save_data_to_csv
from DATA_TRANSMISSION import send_data_to_server, send_csv_to_server


def main(obd_connector, gps_connector, baud_rate, sleep_interval):
    print("Starting OBD-II data collection cycle...")

    # OBD Connection setup
    obd_conn = obd_connection(obd_connector)
    if not obd_conn:
        print("Unable to establish OBD connection. Exiting...")
        return

    initialize_supported_pids(obd_conn)
    supported_pid_names = get_pid_names(supported_pids)

    # Async OBD connection setup
    async_conn = async_connection(obd_connector)
    if not async_conn:
        print("Unable to establish asynchronous OBD connection. Exiting...")
        return

    # GPS Connection setup - now optional
    gps_serial = None
    try:
        gps_serial = gps_connection(gps_connector, baud_rate)
        if not gps_serial:
            print("GPS connection failed. Continuing with OBD data only...")
    except Exception as e:
        print(f"GPS connection error: {e}. Continuing with OBD data only...")

    try:
        while True:
            if supported_pid_names:
                setup_data_collection(async_conn, supported_pid_names)
                obd_df = start_data_collection(async_conn, 0.5)

                gps_df = None
                if gps_serial:
                    try:
                        gps_df = collect_gps_data(gps_serial, 0.2)
                        if not gps_df.empty:
                            print("GPS Data:", gps_df)
                    except Exception as e:
                        print(f"Error collecting GPS data: {e}")

                if not obd_df.empty:
                    print("OBD Data:", obd_df)

                    if gps_df is not None and not gps_df.empty:
                        # Both OBD and GPS data available
                        save_data_to_csv(obd_df, gps_df, 'check.csv')
                        # send_data_to_server(obd_df, gps_df)
                        send_csv_to_server('temp.csv')
                    else:
                        # Only OBD data available
                        save_data_to_csv(obd_df, pd.DataFrame(), 'check.csv')
                        # send_data_to_server(obd_df, None)
                        send_csv_to_server('temp.csv')
                else:
                    print("No OBD data collected in this cycle.")
            else:
                print("No supported PIDs found.")

            print(f"Waiting for {sleep_interval} seconds before the next cycle...")
            time.sleep(sleep_interval)

    except KeyboardInterrupt:
        print("\nData collection stopped by user.")
    finally:
        if async_conn:
            async_conn.stop()
        if gps_serial:
            gps_serial.close()
        print("Program terminated.")

if __name__ == "__main__":
    obd_connector = "/dev/ttyACM0"  # Replace with your actual OBD-II port
    gps_connector = '/dev/ttyUSB0'  # Replace with your actual GPS port
    baud_rate = 115200
    main(obd_connector, gps_connector, baud_rate, sleep_interval=1)

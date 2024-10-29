import os
import pandas as pd
from DATA_TRANSMISSION import send_data_to_server

def save_data_to_csv(obd_df, gps_df, file_path):
    try:
        # Convert OBD data to DataFrame and reset index
        obd_df = pd.DataFrame(obd_df).reset_index(drop=True)

        # Initialize merged_df as obd_df
        merged_df = obd_df

        # Only try to merge if gps_df is not None and not empty
        if gps_df is not None and not isinstance(gps_df, str):
            try:
                gps_df = pd.DataFrame(gps_df).reset_index(drop=True)
                if not gps_df.empty:
                    # Merge OBD and GPS dataframes on index
                    merged_df = pd.concat([obd_df, gps_df], axis=1)
                    # send_data_to_server(merged_df)
            except Exception as e:
                print(f"Error processing GPS data: {e}. Saving OBD data only.")

        # Check if file exists
        file_exists = os.path.isfile(file_path)

        # Save merged dataframe to CSV
        merged_df.to_csv(file_path, mode='a', index=False, header=not file_exists)
        merged_df.to_csv('temp.csv', index=False, header=not file_exists)
        print(f"DataFrame saved to {file_path}")

    except Exception as e:
        print(f"Error saving data to CSV: {e}")

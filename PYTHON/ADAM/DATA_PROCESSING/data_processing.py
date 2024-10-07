import os
import pandas as pd

def save_data_to_csv(df, file_path):
    file_exists = os.path.isfile(file_path)
    df.to_csv(file_path, mode='a', index=False, header=not file_exists)
    print(f"DataFrame saved to {file_path}")
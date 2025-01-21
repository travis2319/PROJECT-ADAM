import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def preprocess_data(df):
    """
    Preprocess data from the database for predictive maintenance.
    """
    logging.info("Starting preprocessing of data.")
    try:
        # Standardize column names
        df.columns = [col.lower().replace(' ', '_') for col in df.columns]

        # Select required columns
        required_columns = [
            "timestamp_obd", "engine_load", "coolant_temp", "short_fuel_trim_1",
            "long_fuel_trim_1", "intake_pressure", "rpm", "speed",
            "throttle_pos", "control_module_voltage", "fuel_level", "ambiant_air_temp",
            "o2_sensors", "catalyst_temp_b1s1", "distance_w_mil", "run_time"
        ]

        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")

        # Clean and preprocess each column
        for col in required_columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            df[col].fillna(df[col].median(), inplace=True)

        # Add derived columns
        df["time_in_years"] = (df["timestamp_obd"].max() - df["timestamp_obd"]) / (365 * 24 * 60 * 60)
        df["time_in_years"].fillna(1, inplace=True)

        logging.info("Preprocessing completed successfully.")
        return df
    except Exception as e:
        logging.error(f"Error during preprocessing: {e}")
        raise

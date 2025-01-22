from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from utils.database import connect_to_db
from utils.dtc_summary import DTCAnalyzer, summarize_dtc_columns, DTCAnalyzerConfig
from utils.nlp_handler import safe_analyze_with_retries, APIConfig
from models.predictive_maintenance import VehicleMaintenance
import pandas as pd
import numpy as np
import json
import logging
from datetime import datetime
from typing import Dict, Any, Union, List

# Configure logging with user context
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - User: %(user)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)
logger = logging.LoggerAdapter(logger, {'user': 'VOID-001'})

router = APIRouter(
    prefix="/chatbot",
    tags=["Chatbot"]
)


def safe_convert_to_python_type(obj: Any) -> Any:
    """Safely convert numpy types to Python native types."""
    if isinstance(obj, dict):
        return {key: safe_convert_to_python_type(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [safe_convert_to_python_type(item) for item in obj]
    elif isinstance(obj, (np.int8, np.int16, np.int32, np.int64,
                          np.uint8, np.uint16, np.uint32, np.uint64)):
        return int(obj)
    elif isinstance(obj, (np.float16, np.float32, np.float64)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, (np.bool_)):
        return bool(obj)
    return obj


class CustomJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder for numpy types."""

    def default(self, obj):
        try:
            return safe_convert_to_python_type(obj)
        except:
            return super().default(obj)


def fetch_predictive_maintenance_summary():
    """Fetch predictive maintenance reports and calculate summaries."""
    try:
        conn = connect_to_db()
        query = "SELECT * FROM obdtest;"
        df = pd.read_sql(query, conn)
        conn.close()

        if df.empty:
            raise ValueError("No data found in the database.")

        # Convert timestamp to numeric first and handle errors
        df['timestamp_obd'] = pd.to_numeric(df['timestamp_obd'], errors='coerce')

        reports = []
        for _, row in df.iterrows():
            try:
                # Clean and convert the data
                vehicle_data = {}

                # Handle numeric conversions with error checking
                numeric_fields = {
                    'distance_w_mil': 0,
                    'speed': 0,
                    'engine_load': 50,
                    'coolant_temp': 90,
                    'run_time': 0,
                    'throttle_pos': 0,
                    'control_module_voltage': 12.5,
                    'fuel_level': 50,
                    'short_fuel_trim_1': 0,
                    'long_fuel_trim_1': 0,
                    'ambiant_air_temp': 25,
                    'catalyst_temp_b1s1': 350,
                    'o2_sensors': 0.5
                }

                for field, default in numeric_fields.items():
                    try:
                        value = row.get(field)
                        if isinstance(value, str) and value.strip():
                            vehicle_data[field] = float(value)
                        else:
                            vehicle_data[field] = float(default)
                    except (ValueError, TypeError):
                        vehicle_data[field] = float(default)

                # Special handling for timestamp conversion
                try:
                    timestamp = float(row.get("timestamp_obd", 31536000))
                    vehicle_data['time_in_years'] = timestamp / (365 * 24 * 60 * 60)
                except (ValueError, TypeError):
                    vehicle_data['time_in_years'] = 1.0

                vehicle = VehicleMaintenance(**vehicle_data)
                report = vehicle.generate_report()
                if report:
                    reports.append(report)

            except Exception as e:
                logger.error(f"Error processing row data: {e}\nRow data: {row.to_dict()}")
                continue

        if not reports:
            default_report = {
                'Distance Traveled': 0.0,
                'Time in Years': 0.0,
                'Speed': 0.0,
                'Engine Load': 50.0,
                'Coolant Temperature': 90.0,
                'Engine Runtime': 0.0,
                'Fuel Level': 50.0,
                'Battery Status': 'Unknown',
                'Spark Plug Status': 'Unknown',
                'Coolant Status': 'Unknown',
                'Oil Change Needed': 'Unknown',
                'Brake Pad Wear': 0.0,
                'Air Filter Status': 'Unknown',
                'Exhaust System Status': 'Unknown',
                'Suspension Status': 'Unknown',
                'Wheel Alignment Status': 'Unknown',
                'Fuel Economy': 'Unknown',
                'Evaporative Emission System Status': 'Unknown'
            }
            return pd.DataFrame([default_report]), df

        return pd.DataFrame(reports), df

    except Exception as e:
        logger.error(f"Error fetching predictive maintenance summary: {e}")
        raise


@router.get("/ask")
async def ask_mechanic(
        query: str,
        user_id: str = "VOID-001",
        current_time: str = "2025-01-18 11:43:30"
):
    """Enhanced chatbot endpoint that incorporates maintenance report DataFrame and DTC analysis."""
    try:
        maintenance_df, raw_df = fetch_predictive_maintenance_summary()

        numerical_summary = maintenance_df.select_dtypes(include=['int64', 'float64']).agg(['mean', 'min', 'max'])
        numerical_summary_dict = safe_convert_to_python_type(numerical_summary.to_dict())

        status_counts = {
            col: safe_convert_to_python_type(maintenance_df[col].value_counts().to_dict())
            for col in maintenance_df.select_dtypes(include=['object']).columns
        }

        dtc_analysis = safe_convert_to_python_type(summarize_dtc_columns(raw_df, user_id))

        context = f"""
        Vehicle Maintenance Analysis Summary:
        Timestamp: {current_time}
        User ID: {user_id}

        1. Key Metrics (averages):
        - Distance Traveled: {numerical_summary_dict.get('Distance Traveled', {}).get('mean', 'N/A')} miles
        - Engine Load: {numerical_summary_dict.get('Engine Load', {}).get('mean', 'N/A')}%
        - Coolant Temperature: {numerical_summary_dict.get('Coolant Temperature', {}).get('mean', 'N/A')}°C
        - Fuel Level: {numerical_summary_dict.get('Fuel Level', {}).get('mean', 'N/A')}%

        2. DTC Information:
        - Health Score: {dtc_analysis.get('overall_health_score', 'N/A')}/100
        - Number of DTCs: {len(dtc_analysis.get('categorical_analysis', {}))}
        - System Status: {json.dumps(dtc_analysis.get('metadata', {}), indent=2)}

        3. Maintenance Status:
        {json.dumps(status_counts, indent=2)}

        4. Additional Vehicle Metrics:
        - Maximum Engine Load: {numerical_summary_dict.get('Engine Load', {}).get('max', 'N/A')}%
        - Minimum Fuel Level: {numerical_summary_dict.get('Fuel Level', {}).get('min', 'N/A')}%
        - Maximum Speed: {numerical_summary_dict.get('Speed', {}).get('max', 'N/A')} km/h

        User Query: {query}
        """

        logger.info(f"Sending context to GPT for user {user_id}")

        gpt_response = safe_analyze_with_retries(context, user_id)

        if not gpt_response["success"]:
            logger.error(f"GPT analysis failed for user {user_id}")
            gpt_response["analysis"] = (
                "I apologize, but I'm having trouble analyzing the data right now. Here's a basic summary:\n\n"
                f"- Vehicle Health Score: {dtc_analysis.get('overall_health_score', 'N/A')}/100\n"
                "Please check the maintenance metrics directly or try again later for a more detailed analysis."
            )

        response_data = {
            "timestamp": current_time,
            "user_id": user_id,
            "query": query,
            "response": gpt_response["analysis"],
            "maintenance_summary": {
                "numerical_metrics": numerical_summary_dict,
                "status_distribution": status_counts,
                "dtc_analysis": dtc_analysis
            },
            "gpt_metadata": {
                "success": gpt_response["success"],
                "attempt": gpt_response["attempt"]
            }
        }

        response_json = json.dumps(response_data, cls=CustomJSONEncoder)

        return JSONResponse(
            content=json.loads(response_json),
            status_code=200
        )

    except Exception as e:
        error_message = f"Unexpected error: {str(e)}"
        logger.error(f"Error in chatbot endpoint for user {user_id}: {error_message}")
        response_data = {
            "timestamp": current_time,
            "user_id": user_id,
            "success": False,
            "error": error_message,
            "query": query
        }
        return JSONResponse(
            content=json.loads(json.dumps(response_data)),
            status_code=500
        )

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from utils.database import connect_to_db
from utils.preprocessing import preprocess_data
from models.predictive_maintenance import VehicleMaintenance
import pandas as pd
import matplotlib.pyplot as plt
import logging
import io

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

router = APIRouter(
    prefix="/predictive-maintenance",
    tags=["Predictive Maintenance"]
)

# Global variables to store processed data and results
maintenance_reports = None
visualization_image = None
predictive_report = None


@router.get("/data")
def fetch_maintenance_data():
    """
    Fetch raw maintenance data from the database.
    """
    try:
        logging.info("Connecting to the database to fetch maintenance data.")
        conn = connect_to_db()
        query = "SELECT * FROM obdtest;"  # Table name
        df = pd.read_sql(query, conn)
        conn.close()

        logging.info("Successfully fetched maintenance data. Sample:\n%s", df.head().to_string())
        return {"columns": df.columns.tolist(), "rows": df.to_dict(orient="records")}
    except Exception as e:
        logging.error(f"Error fetching maintenance data: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching maintenance data: {e}")


@router.get("/preprocess")
def preprocess_maintenance_data():
    """
    Preprocess maintenance data and generate reports.
    """
    global maintenance_reports

    try:
        logging.info("Fetching data for preprocessing.")
        conn = connect_to_db()
        query = "SELECT * FROM obdtest;"  # Table name
        df = pd.read_sql(query, conn)
        conn.close()

        if df.empty:
            raise ValueError("No data found in the database.")

        logging.info("Starting preprocessing.")
        df = preprocess_data(df)

        # Generate maintenance reports
        reports = []
        for _, row in df.iterrows():
            try:
                vehicle = VehicleMaintenance(
                    distance_w_mil=row["distance_w_mil"],
                    time_in_years=row["time_in_years"],
                    speed=row["speed"],
                    engine_load=row["engine_load"],
                    coolant_temp=row["coolant_temp"],
                    run_time=row["run_time"],
                    throttle_pos=row["throttle_pos"],
                    control_module_voltage=row["control_module_voltage"],
                    fuel_level=row["fuel_level"],
                    short_fuel_trim_1=row["short_fuel_trim_1"],
                    long_fuel_trim_1=row["long_fuel_trim_1"],
                    ambiant_air_temp=row["ambiant_air_temp"],
                    o2_sensors=row["o2_sensors"],
                    catalyst_temp_b1s1=row["catalyst_temp_b1s1"]
                )
                reports.append(vehicle.generate_report())
            except Exception as e:
                logging.error(f"Error processing row: {e}")

        if not reports:
            raise ValueError("No reports were generated. Check preprocessing logic.")

        maintenance_reports = pd.DataFrame(reports)
        logging.info("Preprocessing completed successfully.")
        return {"message": "Preprocessing completed successfully.", "sample_reports": maintenance_reports.head().to_dict(orient="records")}
    except Exception as e:
        logging.error(f"Error during preprocessing: {e}")
        raise HTTPException(status_code=500, detail=f"Error preprocessing maintenance data: {e}")


def visualize_vehicle_maintenance(maintenance_df, counts):
    """
    Visualize vehicle maintenance metrics.
    """
    plt.figure(figsize=(20, 15))
    cols = 3
    rows = (len(counts) + cols - 1) // cols

    for i, (title, data) in enumerate(counts.items(), start=1):
        plt.subplot(rows, cols, i)
        plt.bar(data.keys(), data.values(), color="skyblue")
        plt.title(title)
        plt.xticks(rotation=45)
        plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format="png", dpi=100, bbox_inches="tight")
    img.seek(0)
    plt.close()
    return img


from collections import defaultdict

@router.get("/reports")
def get_maintenance_reports():
    """
    Retrieve the generated maintenance reports with averages and counts.
    """
    global maintenance_reports

    if maintenance_reports is None or maintenance_reports.empty:
        raise HTTPException(status_code=400, detail="No reports available. Run preprocessing first.")

    try:
        # Initialize sums and counts
        sums = {
            "Distance Traveled": 0,
            "Time in Years": 0,
            "Speed": 0,
            "Engine Load": 0,
            "Coolant Temperature": 0,
            "Engine Runtime": 0,
            "Fuel Level": 0,
            "Brake Pad Wear": 0,
            "Count": len(maintenance_reports)  # Total counts for averaging
        }

        # Initialize status tracking
        status_counts = {
            "Spark Plug Status": defaultdict(int),
            "Coolant Status": defaultdict(int),
            "Oil Change Needed": defaultdict(int),
            "Battery Status": defaultdict(int),
            "Fuel System Status": defaultdict(int),
            "Air Filter Status": defaultdict(int),
            "Exhaust System Status": defaultdict(int),
            "Suspension Status": defaultdict(int),
            "Wheel Alignment Status": defaultdict(int),
            "Fuel Economy": defaultdict(int),
            "Evaporative Emission System Status": defaultdict(int),
        }

        # Calculate sums and counts
        for index, row in maintenance_reports.iterrows():
            report_dict = row.to_dict()
            for key in sums.keys():
                if key in report_dict and isinstance(report_dict[key], (int, float)):
                    sums[key] += report_dict[key]

            # Count statuses
            for key in status_counts.keys():
                if key in report_dict:
                    status_counts[key][report_dict[key]] += 1

        # Calculate averages
        averages = {key: (value / sums["Count"]) if key != "Count" else value for key, value in sums.items()}

        # Prepare final summary with status counts
        final_summary = {**averages}

        # Add status counts to final summary
        for key, counts in status_counts.items():
            final_summary[key] = dict(counts)

        logging.info("Returning a summarized maintenance report.")
        return final_summary
    except Exception as e:
        logging.error(f"Error retrieving reports: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving reports: {e}")


@router.get("/diagnose")
def generate_predictive_diagnosis():
    """
    Comprehensive endpoint that runs all maintenance diagnostics and generates a detailed report.
    """
    global maintenance_reports, predictive_report

    try:
        # Step 1: Fetch Data
        print("\n[1/4] Fetching maintenance data...")
        conn = connect_to_db()
        query = "SELECT * FROM obdtest;"
        df = pd.read_sql(query, conn)
        conn.close()
        print("✓ Data fetched successfully")

        # Step 2: Preprocess
        print("\n[2/4] Preprocessing maintenance data...")
        processed_df = preprocess_data(df)
        print("✓ Preprocessing complete")

        # Step 3: Generate Vehicle Reports
        print("\n[3/4] Analyzing vehicle conditions...")
        reports = []
        maintenance_statuses = {
            'Critical': 0,
            'Warning': 0,
            'Good': 0
        }

        for idx, row in processed_df.iterrows():
            try:
                vehicle = VehicleMaintenance(
                    distance_w_mil=row["distance_w_mil"],
                    time_in_years=row["time_in_years"],
                    speed=row["speed"],
                    engine_load=row["engine_load"],
                    coolant_temp=row["coolant_temp"],
                    run_time=row["run_time"],
                    throttle_pos=row["throttle_pos"],
                    control_module_voltage=row["control_module_voltage"],
                    fuel_level=row["fuel_level"],
                    short_fuel_trim_1=row["short_fuel_trim_1"],
                    long_fuel_trim_1=row["long_fuel_trim_1"],
                    ambiant_air_temp=row["ambiant_air_temp"],
                    o2_sensors=row["o2_sensors"],
                    catalyst_temp_b1s1=row["catalyst_temp_b1s1"]
                )

                report = vehicle.generate_report()

                # Determine vehicle status based on conditions
                critical_conditions = [
                    "immediately" in str(status).lower()
                    for status in report.values()
                    if isinstance(status, str)
                ]
                warning_conditions = [
                    "soon" in str(status).lower()
                    for status in report.values()
                    if isinstance(status, str)
                ]

                if any(critical_conditions):
                    report['overall_status'] = 'Critical'
                    maintenance_statuses['Critical'] += 1
                elif any(warning_conditions):
                    report['overall_status'] = 'Warning'
                    maintenance_statuses['Warning'] += 1
                else:
                    report['overall_status'] = 'Good'
                    maintenance_statuses['Good'] += 1

                reports.append(report)

            except Exception as e:
                logging.error(f"Error processing vehicle {idx}: {str(e)}")
                continue

        if not reports:
            raise ValueError("No valid reports were generated")

        maintenance_reports = pd.DataFrame(reports)

        # Step 4: Generate Summary Report
        print("\n[4/4] Generating comprehensive maintenance report...")

        summary_stats = {
            "timestamp": "2025-01-19 09:21:26",
            "total_vehicles": len(reports),
            "status_distribution": maintenance_statuses,
            "critical_systems": {
                "engine": maintenance_reports['Engine Load'].mean() if 'Engine Load' in maintenance_reports else 0,
                "coolant": maintenance_reports[
                    'Coolant Temperature'].mean() if 'Coolant Temperature' in maintenance_reports else 0,
                "fuel": maintenance_reports['Fuel Level'].mean() if 'Fuel Level' in maintenance_reports else 0,
                "brake_wear": maintenance_reports[
                    'Brake Pad Wear'].mean() if 'Brake Pad Wear' in maintenance_reports else 0
            },
            "maintenance_required": {
                "immediate_attention": maintenance_statuses['Critical'],
                "soon_attention": maintenance_statuses['Warning'],
                "good_condition": maintenance_statuses['Good']
            }
        }

        # Store the full report
        predictive_report = maintenance_reports.copy()
        predictive_report['analysis_timestamp'] = "2025-01-19 09:21:26"

        print("\nMaintenance Analysis Summary:")
        print(f"Total Vehicles Analyzed: {summary_stats['total_vehicles']}")
        print(f"Critical Issues: {maintenance_statuses['Critical']}")
        print(f"Warnings: {maintenance_statuses['Warning']}")
        print(f"Good Condition: {maintenance_statuses['Good']}")

        return {
            "summary": summary_stats,
            "report_preview": predictive_report.head(10).to_dict(orient="records"),
            "timestamp": "2025-01-19 09:21:26"
        }

    except Exception as e:
        logging.error(f"Error in predictive diagnosis: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating predictive maintenance report: {str(e)}"
        )
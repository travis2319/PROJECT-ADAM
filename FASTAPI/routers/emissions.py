from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from utils.database import connect_to_db
from models.emissions import EnhancedCarEmissionsMLModel
import pandas as pd
import numpy as np

router = APIRouter(
    prefix="/emissions",
    tags=["Emissions Compliance"]
)

emissions_model = None  # To store the trained model
compliance_report = None  # To store the compliance report DataFrame

@router.get("/data")
def fetch_emissions_data():
    """
    Fetch emissions data from the database.
    """
    try:
        conn = connect_to_db()
        query = "SELECT * FROM obdtest;"
        df = pd.read_sql(query, conn)
        conn.close()

        print("Raw Data:")
        print(df.head())  # Log data to console
        return {"columns": df.columns.tolist(), "rows": df.to_dict(orient="records")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching emissions data: {e}")

@router.get("/preprocess")
def preprocess_emissions_data():
    """
    Preprocess emissions data and log the results.
    """
    global emissions_model
    try:
        conn = connect_to_db()
        query = "SELECT * FROM obdtest;"
        df = pd.read_sql(query, conn)
        conn.close()

        emissions_model = EnhancedCarEmissionsMLModel(df)
        emissions_model.advanced_preprocessing()

        print("Preprocessed Data:")
        print(emissions_model.X[:5])  # Log features
        print("Compliance Labels:", emissions_model.y[:5])  # Log labels
        return {"message": "Data preprocessing successful."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error preprocessing emissions data: {e}")

@router.post("/train")
def train_emissions_model():
    """
    Train the emissions model.
    """
    global emissions_model
    if emissions_model is None:
        raise HTTPException(status_code=400, detail="Preprocessing must be completed before training.")

    try:
        emissions_model.train_optimized_model()
        print("Model Training Complete")
        return {"message": "Model training successful."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error training emissions model: {e}")

@router.get("/results")
def get_model_results():
    """
    Get test results and serve the confusion matrix as an image.
    """
    global emissions_model
    if emissions_model is None:
        raise HTTPException(status_code=400, detail="No trained model available.")
    try:
        # Generate the visualization
        img = emissions_model.generate_visualization()
        return StreamingResponse(img, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching model results: {e}")


@router.get("/compliance")
def generate_compliance_report():
    """
    Automated endpoint that runs all steps and generates a compliance report.
    Returns the report as a DataFrame and stores it for future access.
    """
    global emissions_model, compliance_report

    try:
        # Step 1: Fetch Data
        print("\n[1/4] Fetching emissions data...")
        conn = connect_to_db()
        query = "SELECT * FROM obdtest;"
        df = pd.read_sql(query, conn)
        conn.close()
        print("✓ Data fetched successfully")

        # Step 2: Preprocess
        print("\n[2/4] Preprocessing data...")
        emissions_model = EnhancedCarEmissionsMLModel(df)
        emissions_model.advanced_preprocessing()
        print("✓ Preprocessing complete")

        # Step 3: Train Model
        print("\n[3/4] Training model...")
        emissions_model.train_optimized_model()
        print("✓ Model training complete")

        # Step 4: Generate Report
        print("\n[4/4] Generating compliance report...")

        # Get predictions for all data
        predictions = emissions_model.model.predict(emissions_model.X)
        probabilities = emissions_model.model.predict_proba(emissions_model.X)

        # Create compliance report DataFrame
        compliance_report = pd.DataFrame({
            'Timestamp': df['timestamp_obd'] if 'timestamp_obd' in df.columns else range(len(df)),
            'Compliance_Status': ['Compliant' if p == 1 else 'Non-Compliant' for p in predictions],
            'Compliance_Probability': probabilities[:, 1],  # Probability of being compliant
            'Engine_Load': df['engine_load'],
            'Coolant_Temp': df['coolant_temp'],
            'O2_Sensor': df['o2_s1_wr_current'],
            'Short_Fuel_Trim': df['short_fuel_trim_1'],
            'Long_Fuel_Trim': df['long_fuel_trim_1']
        })

        # Add overall metrics
        total_vehicles_values = len(compliance_report)
        compliant_vehicles = sum(predictions)
        compliance_rate = (compliant_vehicles / total_vehicles_values) * 100

        print("\nCompliance Report Summary:")
        print(f"Total Vehicles values Analyzed: {total_vehicles_values}")
        print(f"Compliant Vehicle values: {compliant_vehicles}")
        print(f"Non-Compliant Vehicles values: {total_vehicles_values - compliant_vehicles}")
        print(f"Overall Compliance Rate: {compliance_rate:.2f}%")

        # Return the first few rows and summary statistics
        return {
            "summary": {
                "total_vehicle_values": total_vehicles_values,
                "compliant_vehicle_values": int(compliant_vehicles),
                "non_compliant_vehicle_values": int(total_vehicles_values - compliant_vehicles),
                "compliance_rate": float(compliance_rate)
            },
            "report_preview": compliance_report.head(10).to_dict(orient="records"),
            "timestamp": "2025-01-19 07:39:50",
            # "user": "VOID-001"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating compliance report: {str(e)}"
        )

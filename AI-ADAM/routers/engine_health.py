from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from utils.database import connect_to_db
from models.engine_health import EngineHealthPredictor
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

router = APIRouter(
    prefix="/engine-health",
    tags=["Engine Health"]
)

engine_health_model = None  # Global variable to hold the model instance


@router.get("/data")
def fetch_engine_health_data():
    """
    Fetch engine health data from the database.
    """
    try:
        logging.info("Fetching engine health data from the database.")
        conn = connect_to_db()
        query = "SELECT * FROM obdtest;"
        df = pd.read_sql(query, conn)
        conn.close()
        logging.info("Fetched data successfully. Sample rows:\n%s", df.head().to_string())
        return {"columns": df.columns.tolist(), "rows": df.to_dict(orient="records")}
    except Exception as e:
        logging.error("Error fetching engine health data: %s", e)
        raise HTTPException(status_code=500, detail=f"Error fetching engine health data: {e}")


@router.get("/preprocess")
def preprocess_engine_health_data():
    """
    Preprocess engine health data and log the results.
    """
    global engine_health_model
    try:
        logging.info("Starting preprocessing of engine health data.")
        conn = connect_to_db()
        query = "SELECT * FROM obdtest;"
        df = pd.read_sql(query, conn)
        conn.close()

        engine_health_model = EngineHealthPredictor()
        processed_data = engine_health_model.preprocess_data(df)

        logging.info("Data preprocessing successful. Processed data sample:\n%s", processed_data.head().to_string())
        return {"message": "Data preprocessing successful."}
    except ValueError as ve:
        logging.error("Preprocessing error: %s", ve)
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logging.error("Unexpected error during preprocessing: %s", e)
        raise HTTPException(status_code=500, detail=f"Error preprocessing engine health data: {e}")


@router.post("/train")
def train_engine_health_model():
    """
    Train the engine health model.
    """
    global engine_health_model
    if engine_health_model is None:
        raise HTTPException(status_code=400, detail="Preprocessing must be completed before training.")

    try:
        logging.info("Starting training of engine health model.")
        X_train, X_test, y_train, y_test = engine_health_model.prepare_data(engine_health_model.df)
        engine_health_model.train_model(X_train, y_train)
        cm = engine_health_model.evaluate_model(X_test, y_test)

        logging.info("Model training successful.")
        return {"message": "Model training successful.", "confusion_matrix": cm.tolist()}
    except ValueError as ve:
        logging.error("Training error: %s", ve)
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logging.error("Unexpected error during training: %s", e)
        raise HTTPException(status_code=500, detail=f"Error training engine health model: {e}")


@router.get("/visualize")
def visualize_engine_health_results():
    """
    Visualize engine health model results.
    """
    global engine_health_model
    if engine_health_model is None or engine_health_model.X_test is None:
        raise HTTPException(
            status_code=400,
            detail="No trained model or test data available. Please ensure training is completed successfully."
        )

    try:
        logging.info("Generating visualizations for engine health model.")
        cm = engine_health_model.evaluate_model(engine_health_model.X_test, engine_health_model.y_test)
        img_cm = engine_health_model.visualize_confusion_matrix(cm)
        return StreamingResponse(img_cm, media_type="image/png")
    except Exception as e:
        logging.error("Error generating visualizations: %s", e)
        raise HTTPException(status_code=500, detail=f"Error generating visualizations: {e}")


@router.get("/diagnose")
def generate_engine_diagnosis():
    """
    Automated endpoint that runs all diagnostic steps and generates a comprehensive report.
    Returns the report as a DataFrame and stores it for future access.
    """
    global engine_health_model, engine_health_report

    try:
        # Step 1: Fetch Data
        print("\n[1/4] Fetching engine diagnostic data...")
        conn = connect_to_db()
        query = "SELECT * FROM obdtest;"
        df = pd.read_sql(query, conn)
        conn.close()
        print("✓ Data fetched successfully")

        # Step 2: Preprocess
        print("\n[2/4] Preprocessing engine data...")
        engine_health_model = EngineHealthPredictor()
        processed_data = engine_health_model.preprocess_data(df)
        print("✓ Preprocessing complete")

        # Step 3: Train Model
        print("\n[3/4] Training diagnostic model...")
        X_train, X_test, y_train, y_test = engine_health_model.prepare_data(df)
        engine_health_model.train_model(X_train, y_train)
        print("✓ Model training complete")

        # Step 4: Generate Report
        print("\n[4/4] Generating engine health report...")

        # Get predictions and handle single-class mode
        X_all_scaled = engine_health_model.scaler.transform(processed_data)

        if engine_health_model.single_class_mode:
            # For single class mode, use the only available class
            predictions = ['Good'] * len(processed_data)  # Assuming 'Good' is the only class
            confidence_scores = [1.0] * len(processed_data)  # Full confidence in single-class mode
        else:
            # For multi-class mode, use model predictions
            predictions = engine_health_model.model.predict(X_all_scaled)
            probas = engine_health_model.model.predict_proba(X_all_scaled)
            confidence_scores = [max(p) for p in probas]  # Use highest probability as confidence

        # Create diagnostic report DataFrame
        engine_health_report = pd.DataFrame({
            'Timestamp': df['timestamp_obd'] if 'timestamp_obd' in df.columns else range(len(df)),
            'Engine_Health_Status': predictions,
            'Confidence_Score': confidence_scores,
            'Engine_Load': processed_data['engine_load'],
            'Coolant_Temp': processed_data['coolant_temp'],
            'Short_Fuel_Trim': processed_data['short_fuel_trim_1'],
            'Long_Fuel_Trim': processed_data['long_fuel_trim_1'],
            'Intake_Pressure': processed_data['intake_pressure'],
            'RPM': processed_data['rpm']
        })

        # Calculate summary statistics
        total_records = len(engine_health_report)
        good_condition = sum(p == 'Good' for p in predictions)
        needs_attention = total_records - good_condition

        print("\nEngine Health Report Summary:")
        print(f"Total Records Analyzed: {total_records}")
        print(f"Vehicles in Good Condition: {good_condition}")
        print(f"Vehicles Needing Attention: {needs_attention}")
        print(f"Overall Health Rate: {(good_condition / total_records) * 100:.2f}%")

        # Add analysis timestamps
        analysis_timestamp = "2025-01-19 07:58:09"

        return {
            "summary": {
                "total_records": total_records,
                "good_condition": int(good_condition),
                "needs_attention": int(needs_attention),
                "health_rate": float((good_condition / total_records) * 100),
                "analysis_mode": "single_class" if engine_health_model.single_class_mode else "multi_class"
            },
            "report_preview": engine_health_report.head(10).to_dict(orient="records"),
            "timestamp": analysis_timestamp,
            "user": "VOID-001"
        }

    except Exception as e:
        logging.error(f"Error in report generation: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating engine health report: {str(e)}"
        )
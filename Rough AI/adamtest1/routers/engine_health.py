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
        query = "SELECT * FROM obd_log;"
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
        query = "SELECT * FROM obd_log;"
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


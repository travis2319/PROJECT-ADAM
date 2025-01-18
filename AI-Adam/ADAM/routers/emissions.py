from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from utils.database import connect_to_db
from models.emissions import EnhancedCarEmissionsMLModel
import pandas as pd

router = APIRouter(
    prefix="/emissions",
    tags=["Emissions Compliance"]
)

emissions_model = None  # To store the trained model

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

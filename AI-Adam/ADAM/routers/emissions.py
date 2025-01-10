# routers/emissions.py
from fastapi import APIRouter, HTTPException
from utils.database import Database
from typing import List, Dict, Any
from datetime import datetime
import pandas as pd
from models.emissions import EnhancedCarEmissionsMLModel

router = APIRouter(prefix="/emissions", tags=["emissions"])

# Global variable to hold the trained emissions model
emissions_model: EnhancedCarEmissionsMLModel = None

@router.get("/data")
def fetch_emissions_data() -> List[Dict[str, Any]]:
    try:
        with Database.get_db() as conn:
            with conn.cursor() as cur:
                # Execute the query
                cur.execute("SELECT * FROM obd_log ORDER BY timestamp_obd DESC LIMIT 100")
                
                # Get column names from cursor description
                columns = [desc[0] for desc in cur.description]
                
                # Fetch all rows and convert to list of dictionaries
                results = []
                for row in cur.fetchall():
                    # Convert each row to a dictionary
                    row_dict = dict(zip(columns, row))
                    
                    # Convert datetime objects to string format if they exist
                    for key, value in row_dict.items():
                        if isinstance(value, datetime):
                            row_dict[key] = value.isoformat()
                            
                    results.append(row_dict)
                
                return results
                
    except Exception as e:
        print(f"Database error: {str(e)}")  # For debugging purposes
        raise HTTPException(
            status_code=500,
            detail="Error fetching emissions data from database"
        )

@router.post("/train")
def train_emissions_model():
    global emissions_model
    try:
        raw_data = fetch_emissions_data()  # Fetch raw data from the database
        
        if not raw_data:
            raise HTTPException(status_code=404, detail="No data found in the database.")

        # Convert raw data to a DataFrame for training
        raw_data_df = pd.DataFrame(raw_data)

        # Initialize and train the emissions model
        emissions_model = EnhancedCarEmissionsMLModel(raw_data_df)
        emissions_model.advanced_preprocessing()
        emissions_model.train_optimized_model()

        return {"message": "Emissions model trained successfully."}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")

@router.post("/predict")
def predict_emissions(data: List[Dict[str, Any]]):
    global emissions_model
    
    if emissions_model is None:
        raise HTTPException(status_code=400, detail="Model is not trained yet. Train the model first.")

    try:
        predictions = emissions_model.predict(data)
        return {"predictions": predictions.tolist()}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

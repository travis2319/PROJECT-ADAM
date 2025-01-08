from fastapi import APIRouter, HTTPException
from utils.database import Database
import pandas as pd

# Router setup
router = APIRouter(
    prefix="/emissions",
    tags=["Car Emissions"],
)

db_instance = Database("postgresql://postgres:mysecretpassword@db:5432/mydb")

@router.get("/data")
def fetch_emissions_data():
    """
    Fetch all data related to car emissions from the database.
    """
    try:
        data = db_instance.fetch_all_data("emissions_table")  # Replace with the actual table name
        return {"data": data.to_dict(orient="records")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
